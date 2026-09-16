from curl_cffi import requests as c_requests
import json

# Test company name autocomplete / details
url = "https://iepf.gov.in/bin/payment/getIepfCompNameDetails"
params = {"term": "TATA"}

try:
    r = c_requests.get(url, params=params, impersonate="chrome120", verify=False)
    print("getIepfCompNameDetails status:", r.status_code)
    print("Response sample (first 300 chars):", r.text[:300])
except Exception as e:
    print("Error:", e)
