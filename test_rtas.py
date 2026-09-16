import requests

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

for url in [
    'https://linkintime.co.in/initial_offerings/public-issues.html',
    'https://ris.kfintech.com/ipostatus/',
    'https://web.linkintime.co.in/InvestorServices/Search.aspx'
]:
    try:
        r = s.get(url, timeout=10, verify=False)
        print(f"{url} -> status: {r.status_code}, len: {len(r.text)}")
    except Exception as e:
        print(f"{url} -> error: {e}")
