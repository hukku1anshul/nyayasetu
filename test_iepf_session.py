from curl_cffi import requests as c_requests
import hashlib, base64, urllib.parse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

parts = ["d6163f0659", "cfe4196dc0", "3c2c29aab0", "6f10cb0a79", "cdfc74a45d", "a2d723587", "12e80"]
pass_text = "".join(parts).encode('utf-8')
salt_bytes = hashlib.md5("fc74a45dsalt".encode('utf-8')).digest()
iv_bytes = hashlib.md5("c29aab06iv".encode('utf-8')).digest()

kdf = PBKDF2HMAC(algorithm=hashes.SHA1(), length=16, salt=salt_bytes, iterations=100)
key = kdf.derive(pass_text)

def mca_encrypt(msg: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(msg.encode('utf-8')) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv_bytes))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    b64 = base64.b64encode(ct).decode('utf-8')
    return urllib.parse.quote(b64, safe='')

s = c_requests.Session()
search_page = "https://iepf.gov.in/content/iepf/global/master/Home/Services/new-search-facility-beta.html"
r_init = s.get(search_page, impersonate="chrome120", verify=False)
print("Init page status:", r_init.status_code)

firstname = "RAMESH"
req_data = f"firstname={firstname}&fathersfirstname=&state={mca_encrypt('')}&district={mca_encrypt('')}&address={mca_encrypt('')}&compName={mca_encrypt('')}"
outer_encrypted = mca_encrypt(req_data)

url = "https://iepf.gov.in/bin/payment/getIepfSearchShares"
headers = {
    "Referer": search_page,
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}
params = {"data": outer_encrypted}

r = s.get(url, params=params, headers=headers, impersonate="chrome120", verify=False)
print("Search status:", r.status_code)
print("Response text sample:", r.text[:300])
