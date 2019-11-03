import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

url = 'http://dbl44.beuth-hochschule.de'

import urllib.request
response = urllib.request.urlopen(url)
html = response.read()
text = html.decode()
print(text)

with closing(get(url, stream=True)) as resp:
   html = BeautifulSoup(resp.content, 'html.parser')
   for p in html.select('p'):
      if p['id'] == 'client-ip':
         print(p.text)
