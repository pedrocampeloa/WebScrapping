"""
https://sisweb.tesouro.gov.br/apex/f?p=2031:2:::::
"""

import bs4 as bs
import requests
import re


url = 'https://sisweb.tesouro.gov.br/apex/f?p=2031:2:::::'
# Problemas de certificados com sites do governo
html = requests.get(url, verify=False)

# print(html.text)
soup = bs.BeautifulSoup(html.text, 'html5lib')
divs = soup.findAll('div', {'class': 'bl-body'})

urls = []

for div in divs:
    links = div.findAll('a')
    for link in links:
        urls.append(link['href'])

url_prefix = 'https://sisweb.tesouro.gov.br/apex/'
for link in urls:
    f = requests.get(url_prefix + link, verify=False)
    # pprint(f.headers)
    # Usando regex para pegar o nome do arquivo
    fname = re.findall('filename="(.+)"', f.headers['Content-Disposition'])[0]
    with open(fname, 'wb') as output:
        output.write(f.content)
    print('Downloaded file', fname)
