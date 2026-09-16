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

for page in ['GazetteDirectory.aspx', 'Default.aspx', 'StateGazette.aspx']:
    try:
        r = s.get(f'https://egazette.gov.in/{page}', verify=False, timeout=10)
        print(f'{page}: status {r.status_code}, inputs: {len(re.findall(r"<input", r.text))}')
        # Check text or titles
        title = re.findall(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
        print(f'   Title: {title}')
        # Find any dropdown / select names
        selects = re.findall(r'<select[^>]*name=[\'"]([^\'"]+)[\'"]', r.text)
        print(f'   Selects: {selects}')
    except Exception as e:
        print(f'{page} error:', e)
