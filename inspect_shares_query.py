from curl_cffi import requests as c_requests

url = "https://iepf.gov.in/etc.clientlibs/mca/components/content/foBoSearch/clientlibs.min.js"
r = c_requests.get(url, impersonate="chrome120", verify=False)
js_text = r.text

idx = js_text.find('getIepfSearchShares')
print("Snippet before getIepfSearchShares (where reqData is built):")
print(js_text[max(0, idx-800):idx+300])
