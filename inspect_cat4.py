import requests, socket, urllib3, re

urllib3.disable_warnings()
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'egazette.gov.in':
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('164.100.190.144', port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = custom_getaddrinfo

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
r = s.get('https://egazette.gov.in/RecentUploads.aspx?Category=4', verify=False)

tables = re.findall(r'<table[^>]*id=[\'"]([^\'"]+)[\'"]', r.text)
grids = re.findall(r'<div[^>]*id=[\'"]([^\'"]+)[\'"]', r.text)
print("Tables:", tables)
print("Divs:", [g for g in grids if any(k in g.lower() for k in ['grid', 'content', 'upload', 'result'])])

# Find form action
forms = re.findall(r'<form[^>]*action=[\'"]([^\'"]+)[\'"]', r.text)
print("Form actions:", forms)
