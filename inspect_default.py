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
r = s.get('https://egazette.gov.in/Default.aspx', verify=False)
inputs = re.findall(r'<input[^>]*id=[\'"]([^\'"]+)[\'"]', r.text)
options = re.findall(r'<option[^>]*value=[\'"]([^\'"]+)[\'"][^>]*>([^<]+)</option>', r.text)
print("Default.aspx inputs:", inputs)
print("Default.aspx options:", options[:10])

# Also check any links to search pages
links = re.findall(r'href=[\'"]([^\'"]+\.aspx[^\'"]*)[\'"]', r.text)
print("All aspx links on Default:", set(links))
