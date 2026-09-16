import requests
import re
import urllib3
import socket
from curl_cffi import requests as c_requests

urllib3.disable_warnings()

# Patch DNS for egazette.gov.in
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'egazette.gov.in':
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('164.100.190.144', port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = custom_getaddrinfo

def inspect_iepf_search():
    print("--- Inspecting IEPF Search Facility ---")
    url = "https://iepf.gov.in/content/iepf/global/master/Home/Services/new-search-facility-beta.html"
    try:
        r = c_requests.get(url, impersonate="chrome120", timeout=15, verify=False)
        print("Status:", r.status_code)
        # Look for iframes, api calls, form action
        forms = re.findall(r'<form.*?>', r.text, re.IGNORECASE)
        inputs = re.findall(r'<input.*?>', r.text, re.IGNORECASE)
        iframes = re.findall(r'<iframe.*?src=[\'"](.*?)[\'"].*?>', r.text, re.IGNORECASE)
        scripts = re.findall(r'src=[\'"](.*?)[\'"]', r.text, re.IGNORECASE)
        apis = [s for s in scripts if 'search' in s.lower() or 'api' in s.lower()]
        print("Forms found:", len(forms))
        print("Inputs found:", len(inputs))
        print("Iframes found:", iframes)
        print("Search scripts:", apis)
    except Exception as e:
        print("IEPF error:", e)

def inspect_egazette_search():
    print("\n--- Inspecting e-Gazette SearchMenu.aspx ---")
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        r = s.get("https://egazette.gov.in/SearchMenu.aspx", verify=False, timeout=15)
        print("Status:", r.status_code)
        # Find links on SearchMenu
        links = re.findall(r'href=[\'"](.*?)[\'"]', r.text)
        search_links = [l for l in links if 'aspx' in l]
        print("Search sub-pages:", set(search_links))
    except Exception as e:
        print("Gazette error:", e)

if __name__ == "__main__":
    inspect_iepf_search()
    inspect_egazette_search()
