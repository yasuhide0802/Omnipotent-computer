import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = "https://api.github.com/search/repositories?q=sustainable+development+biodiversity&per_page=3"

try:
    req = Request(API_URL, headers={"Accept": "application/vnd.github.v3+json"})
    with urlopen(req) as resp:
        data = json.load(resp)
except HTTPError as e:
    print(f"HTTP Error: {e.code}")
    sys.exit(1)
except URLError as e:
    print(f"URL Error: {e.reason}")
    sys.exit(1)

for item in data.get('items', []):
    name = item.get('full_name')
    description = (item.get('description') or '').replace('\n', ' ')
    stars = item.get('stargazers_count')
    html_url = item.get('html_url')
    print(f"- {name} ({stars} ⭐): {description}\n  {html_url}")
