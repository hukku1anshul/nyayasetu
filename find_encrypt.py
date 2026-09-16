from curl_cffi import requests as c_requests
import re

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
js_text = r.text

idx = js_text.find('function encrypt(')
if idx != -1:
    print("Found function encrypt:")
    print(js_text[idx:idx+500])
else:
    # Look for encrypt =
    m = re.findall(r'encrypt\s*=\s*function.*?\n', js_text)
    print("Matches for encrypt:", m)
    # Check for CryptoJS or key
    keys = re.findall(r'[\'"][A-Za-z0-9+/=]{16,32}[\'"]', js_text)
    print("Potential keys:", keys[:5])
