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

def probe_egazette():
    print("--- Probing e-Gazette ---")
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    })
    try:
        r = s.get('https://egazette.gov.in/', verify=False, timeout=10)
        print("e-Gazette main page status:", r.status_code)
        links = re.findall(r'href=[\'"](.*?)[\'"]', r.text)
        interesting = [l for l in links if any(k in l.lower() for k in ['search', 'gazette', 'part', 'weekly', 'download', 'form'])]
        for l in set(interesting[:15]):
            print("  Link:", l)
    except Exception as e:
        print("e-Gazette probe error:", e)

def probe_iepf():
    print("\n--- Probing IEPF ---")
    try:
        r = c_requests.get('https://iepf.gov.in', impersonate='chrome120', timeout=10, verify=False)
        print("IEPF status:", r.status_code)
        links = re.findall(r'href=[\'"](.*?)[\'"]', r.text)
        interesting = [l for l in links if any(k in l.lower() for k in ['search', 'claim', 'refund', 'unclaimed', 'iepf-5', 'investor'])]
        for l in set(interesting[:15]):
            print("  Link:", l)
    except Exception as e:
        print("IEPF probe error:", e)

if __name__ == "__main__":
    probe_egazette()
    probe_iepf()
