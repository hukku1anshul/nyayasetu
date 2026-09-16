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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
})

s.get('https://egazette.gov.in/Default.aspx', verify=False)
s.headers.update({'Referer': 'https://egazette.gov.in/Default.aspx'})
r2 = s.get('https://egazette.gov.in/RecentUploads.aspx?Category=4', verify=False)

# Parse gvGazetteList rows
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', r2.text, re.DOTALL)
print(f"Total table rows found in Category 4 (Part-IV Name Change Gazette): {len(rows)}")

for idx, row in enumerate(rows[:6]):
    cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    if cells:
        clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', row)
        print(f"Row {idx}: {clean}")
        if links:
            print(f"  PDF Link: {links}")
