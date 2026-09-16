from curl_cffi import requests as c_requests

url = "https://iepf.gov.in/etc.clientlibs/mca/clientlibs/clientlibs-encrptdecrypt.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
print("Encrptdecrypt status:", r.status_code)
print("File contents sample (first 800 chars):")
print(r.text[:800])
