"""
MCA IEPF Cryptographic & Unclaimed Asset Integration Client (Zero-Cost / Free Connection)
Implements Ministry of Corporate Affairs' proprietary encryption scheme in Python,
enabling direct connection to IEPF & MCA21 without paid API aggregators.
"""

import hashlib
import base64
import urllib.parse
from typing import Dict, List, Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from curl_cffi import requests as c_requests

class MCACryptoEngine:
    """
    Reverse-engineered from MCA clientlibs-encrptdecrypt.min.js.
    Key derivation: PBKDF2 (SHA-1, 100 iterations) with MD5 salt.
    Cipher: AES-128-CBC with PKCS7 padding.
    """
    PARTS = ["d6163f0659", "cfe4196dc0", "3c2c29aab0", "6f10cb0a79", "cdfc74a45d", "a2d723587", "12e80"]
    PASS_TEXT = "".join(PARTS).encode('utf-8')
    SALT = hashlib.md5("fc74a45dsalt".encode('utf-8')).digest()
    IV = hashlib.md5("c29aab06iv".encode('utf-8')).digest()

    @classmethod
    def get_key(cls) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=16,
            salt=cls.SALT,
            iterations=100
        )
        return kdf.derive(cls.PASS_TEXT)

    @classmethod
    def encrypt(cls, plaintext: str) -> str:
        key = cls.get_key()
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(cls.IV))
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded) + encryptor.finalize()
        b64 = base64.b64encode(ct).decode('utf-8')
        return urllib.parse.quote(b64, safe='')

    @classmethod
    def decrypt(cls, b64_quoted: str) -> str:
        key = cls.get_key()
        b64 = urllib.parse.unquote(b64_quoted)
        ct = base64.b64decode(b64)
        cipher = Cipher(algorithms.AES(key), modes.CBC(cls.IV))
        decryptor = cipher.decryptor()
        pt_padded = decryptor.update(ct) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return (unpadder.update(pt_padded) + unpadder.finalize()).decode('utf-8')


class IEPFUnclaimedAssetClient:
    """
    Direct zero-cost client for querying IEPF and compiling SEBI statutory transmission dossiers.
    """
    IEPF_BASE = "https://iepf.gov.in"
    SEARCH_PAGE = f"{IEPF_BASE}/content/iepf/global/master/Home/Services/new-search-facility-beta.html"

    def __init__(self):
        self.session = c_requests.Session()

    def check_portal_liveness(self) -> Dict[str, Any]:
        """
        Verifies direct connection to official MCA & IEPF portals without paid proxies.
        """
        try:
            r = self.session.get(self.IEPF_BASE, impersonate="chrome120", verify=False, timeout=10)
            return {
                "portal": "Investor Education and Protection Fund Authority (iepf.gov.in)",
                "status_code": r.status_code,
                "connection": "ONLINE" if r.status_code == 200 else "DEGRADED",
                "bytes_received": len(r.text),
                "mca_encryption_engine": "INITIALIZED"
            }
        except Exception as e:
            return {
                "portal": "iepf.gov.in",
                "connection": "OFFLINE",
                "error": str(e)
            }

    def prepare_unclaimed_search_query(self, investor_name: str, company_name: str, state: str = "") -> Dict[str, Any]:
        """
        Builds the encrypted query payload compliant with MCA's /bin/payment/getIepfSearchShares.
        """
        enc_state = MCACryptoEngine.encrypt(state)
        enc_district = MCACryptoEngine.encrypt("")
        enc_address = MCACryptoEngine.encrypt("")
        enc_comp = MCACryptoEngine.encrypt(company_name)

        inner_query = f"firstname={investor_name}&fathersfirstname=&state={enc_state}&district={enc_district}&address={enc_address}&compName={enc_comp}"
        outer_payload = MCACryptoEngine.encrypt(inner_query)

        return {
            "investor_name": investor_name,
            "company_name": company_name,
            "inner_query_raw": inner_query,
            "mca_encrypted_payload": outer_payload,
            "mca_target_endpoint": f"{self.IEPF_BASE}/bin/payment/getIepfSearchShares"
        }

    def generate_complete_sebi_dossier(
        self,
        claimant_name: str,
        deceased_name: str,
        company_name: str,
        folio_number: str,
        share_count: int,
        estimated_share_price: float,
        bank_name: str,
        bank_account_no: str,
        ifsc_code: str
    ) -> Dict[str, Any]:
        """
        Generates the complete, zero-cost statutory paperwork bundle mandated by SEBI & MCA.
        """
        total_market_value = share_count * estimated_share_price

        # Form ISR-1 Data
        isr1 = {
            "form_title": "Form ISR-1 (Request for Registering PAN, KYC Details or Changes/Updation)",
            "investor_name": claimant_name,
            "folio_no": folio_number,
            "company_name": company_name,
            "demat_account_type": "NSDL / CDSL",
            "bank_details": {
                "bank": bank_name,
                "account_no": bank_account_no,
                "ifsc": ifsc_code
            }
        }

        # Form ISR-2 (Banker Attestation Format)
        isr2 = {
            "form_title": "Form ISR-2 (Confirmation of Signature of Securities Holder by Banker)",
            "instructions": "To be signed and stamped with Bank Branch Seal, Employee Code, and Signature of Branch Manager"
        }

        # Form-A Legal Heir Affidavit
        form_a_affidavit = f"""BEFORE THE EXECUTIVE MAGISTRATE / NOTARY PUBLIC
FORM-A: AFFIDAVIT FOR TRANSMISSION OF SECURITIES WHERE SHAREHOLDER IS DECEASED

I/We, {claimant_name}, residing at ____________________________________, do solemnly state and affirm as under:
1. That Shri/Smt. {deceased_name} was holding {share_count} equity shares in {company_name} under Folio No. {folio_number}.
2. That the said shareholder expired on __/__/____ at ________________.
3. That the deponent is the surviving legal heir / successor entitled to the said securities under Hindu Succession Act / Indian Succession Act.
4. Total current estimated valuation is Rs. {total_market_value:,.2f}.

DEPONENT: {claimant_name}
"""

        # Form-B Indemnity Bond
        form_b_indemnity = f"""FORM-B: INDEMNITY BOND ON NON-JUDICIAL / NeSL STAMP PAPER (RS. 500)
IN FAVOUR OF {company_name.upper()} AND ITS REGISTRAR & TRANSFER AGENT

WHEREAS {deceased_name} was the registered holder of {share_count} shares in {company_name};
AND WHEREAS {claimant_name} has requested the transmission of shares without production of a formal Probate/Succession Certificate;
NOW THIS DEED WITNESSETH that in consideration of the company acceding to the transmission request, I/We the claimant along with two independent sureties hereby agree to indemnify and hold harmless the Company, its Directors, Officers, and RTA against any and all losses, claims, and actions.

PRINCIPAL OBLIGOR (Claimant): {claimant_name}
SURETY 1: __________________________
SURETY 2: __________________________
"""

        # Form IEPF-5 Spec
        iepf5 = {
            "form_title": "Form IEPF-5 (Application to the Authority for Claiming Unpaid Amounts and Shares)",
            "authority": "Investor Education and Protection Fund Authority, Ministry of Corporate Affairs",
            "fees_payable_to_mca": "Rs. 0 (Free Government e-form filing)",
            "claimant_pan": "Required",
            "aadhaar_verification": "Required",
            "demat_client_master_list_cml": "Mandatory attachment"
        }

        return {
            "case_summary": {
                "claimant": claimant_name,
                "deceased_holder": deceased_name,
                "company": company_name,
                "shares": share_count,
                "total_estimated_value_inr": total_market_value
            },
            "statutory_forms": {
                "form_isr_1": isr1,
                "form_isr_2": isr2,
                "form_a_affidavit": form_a_affidavit,
                "form_b_indemnity": form_b_indemnity,
                "form_iepf_5": iepf5
            }
        }
