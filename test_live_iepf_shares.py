import hashlib
import base64
import urllib.parse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from curl_cffi import requests as c_requests

# 1. MCA Constants
parts = ["d6163f0659", "cfe4196dc0", "3c2c29aab0", "6f10cb0a79", "cdfc74a45d", "a2d723587", "12e80"]
pass_text = "".join(parts).encode('utf-8')
salt_bytes = hashlib.md5("fc74a45dsalt".encode('utf-8')).digest()
iv_bytes = hashlib.md5("c29aab06iv".encode('utf-8')).digest()

def derive_key():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=16,
        salt=salt_bytes,
        iterations=100
    )
    return kdf.derive(pass_text)

key = derive_key()

def mca_encrypt(msg: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(msg.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv_bytes))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    b64 = base64.b64encode(ct).decode('utf-8')
    return urllib.parse.quote(b64, safe='')

def mca_decrypt(b64_quoted: str) -> str:
    b64 = urllib.parse.unquote(b64_quoted)
    ct = base64.b64decode(b64)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv_bytes))
    decryptor = cipher.decryptor()
    pt_padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(pt_padded) + unpadder.finalize()).decode('utf-8')

# Build query for a common Indian name e.g. "SHARMA"
firstname = "SHARMA"
fathersfirstname = ""
state = mca_encrypt("")
district = mca_encrypt("")
address = mca_encrypt("")
comp_name = mca_encrypt("TATA")

req_data = f"firstname={firstname}&fathersfirstname={fathersfirstname}&state={state}&district={district}&address={address}&compName={comp_name}"
outer_encrypted = mca_encrypt(req_data)

url = "https://iepf.gov.in/bin/payment/getIepfSearchShares"
headers = {
    "Referer": "https://iepf.gov.in/content/iepf/global/master/Home/Services/new-search-facility-beta.html",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

# In jQuery ajax: data: "data=" + encrypt(reqData) -> GET /bin/payment/getIepfSearchShares?data=...
params = {"data": outer_encrypted}

print("Calling IEPF Search Shares live...")
try:
    r = c_requests.get(url, params=params, headers=headers, impersonate="chrome120", verify=False, timeout=20)
    print("Status code:", r.status_code)
    print("Response headers:", dict(r.headers))
    print("Response sample (first 400 chars):", r.text[:400])
except Exception as e:
    print("Error:", e)
