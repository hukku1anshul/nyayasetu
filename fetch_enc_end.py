from curl_cffi import requests as c_requests

url = "https://iepf.gov.in/etc.clientlibs/mca/clientlibs/clientlibs-encrptdecrypt.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
print("File length:", len(r.text))
print("End of file (last 1500 chars):")
print(r.text[-1500:])
