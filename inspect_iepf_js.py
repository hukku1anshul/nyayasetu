from curl_cffi import requests as c_requests
import re

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
print("Clientlib JS status:", r.status_code, "Length:", len(r.text))

# Search for endpoints or urls in the JS
urls = re.findall(r'[\'"](/bin/[^\'"]+|/content/[^\'"]+|https?://[^\'"]+)[\'"]', r.text)
print("Endpoints found in IEPF search JS:")
for u in set(urls):
    if any(k in u.lower() for k in ['search', 'data', 'iepf', 'servlet', 'bin', 'api']):
        print(" ", u)
