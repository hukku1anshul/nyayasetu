from curl_cffi import requests as c_requests
import re
import urllib3
import requests, socket

urllib3.disable_warnings()

# Patch DNS for egazette
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'egazette.gov.in':
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('164.100.190.144', port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = custom_getaddrinfo

# Check IEPF input names
r = c_requests.get("https://iepf.gov.in/content/iepf/global/master/Home/Services/new-search-facility-beta.html", impersonate="chrome120", verify=False)
inputs = re.findall(r'<input[^>]*name=[\'"]([^\'"]+)[\'"][^>]*>', r.text)
buttons = re.findall(r'<button[^>]*>([^<]+)</button>', r.text)
print("IEPF input names:", inputs)
print("IEPF buttons:", buttons)

# Check Gazette SearchMenu form actions
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})
rg = s.get("https://egazette.gov.in/SearchMenu.aspx", verify=False)
gaz_inputs = re.findall(r'<input[^>]*name=[\'"]([^\'"]+)[\'"][^>]*>', rg.text)
print("\nGazette input names:", gaz_inputs[:10])
gaz_actions = re.findall(r'<a[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>([^<]+)</a>', rg.text)
print("Gazette links on SearchMenu:", [(u, t.strip()) for u, t in gaz_actions if t.strip()][:10])
