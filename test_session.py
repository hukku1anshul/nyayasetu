import requests, socket, urllib3, re

urllib3.disable_warnings()
orig_getaddrinfo = socket.getaddrinfo
def custom_getaddrinfo(host, port, *args, **kwargs):
    if host == 'egazette.gov.in':
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('164.100.190.144', port))]
    return orig_getaddrinfo(host, port, *args, **kwargs)
socket.getaddrinfo = custom_getaddrinfo

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
})

# Step 1: Visit home page to establish session
r1 = s.get('https://egazette.gov.in/Default.aspx', verify=False)
print("Step 1 Default status:", r1.status_code, "Cookies:", dict(s.cookies))

# Step 2: Navigate with Referer
s.headers.update({'Referer': 'https://egazette.gov.in/Default.aspx'})
r2 = s.get('https://egazette.gov.in/RecentUploads.aspx?Category=4', verify=False)
print("Step 2 Category 4 status:", r2.status_code)
form_action = re.findall(r'<form[^>]*action=[\'"]([^\'"]+)[\'"]', r2.text)
print("Form action now:", form_action)

tables = re.findall(r'<table[^>]*id=[\'"]([^\'"]+)[\'"]', r2.text)
print("Tables now:", tables)
