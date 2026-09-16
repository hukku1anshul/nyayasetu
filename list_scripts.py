from curl_cffi import requests as c_requests
import re

url = "https://iepf.gov.in/content/iepf/global/master/Home/Services/new-search-facility-beta.html"
r = c_requests.get(url, impersonate="chrome120", verify=False)
scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', r.text)
print("All script URLs on IEPF search page:")
for s in scripts:
    print(" ", s)
