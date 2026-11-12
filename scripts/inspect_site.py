import urllib.request, re

req = urllib.request.Request('https://www.ebinreji.online', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as res:
    html = res.read().decode('utf-8', errors='ignore')

matches = set(re.findall(r'[\'"]([^\'"]+\.(?:png|jpg|jpeg|webp|svg|ico))[\'"]', html, re.I))
for m in sorted(matches):
    print(m)

