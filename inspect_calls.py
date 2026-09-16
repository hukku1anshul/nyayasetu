from curl_cffi import requests as c_requests
import re

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
js_text = r.text

# Find where getIepfCompNameDetails or getIepfSearchShares is invoked
matches = re.findall(r'.{0,100}getIepfCompNameDetails.{0,150}', js_text)
for m in matches[:3]:
    print("Match 1:", m)

matches2 = re.findall(r'.{0,100}getIepfSearchShares.{0,200}', js_text)
for m in matches2[:3]:
    print("\nMatch 2:", m)
