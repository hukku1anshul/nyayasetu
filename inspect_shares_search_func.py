from curl_cffi import requests as c_requests

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
js_text = r.text

idx = js_text.find('function callSharesSearch(')
print("Snippet of callSharesSearch:")
print(js_text[idx:idx+800])
