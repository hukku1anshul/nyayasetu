from curl_cffi import requests as c_requests
import re

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
js_text = r.text

idx = js_text.find('/bin/payment/getIepfSearchShares')
if idx != -1:
    print("Code around getIepfSearchShares:")
    print(js_text[max(0, idx-200):min(len(js_text), idx+600)])

idx2 = js_text.find('/bin/payment/getIepfCompNameDetails')
if idx2 != -1:
    print("\nCode around getIepfCompNameDetails:")
    print(js_text[max(0, idx2-100):min(len(js_text), idx2+400)])
