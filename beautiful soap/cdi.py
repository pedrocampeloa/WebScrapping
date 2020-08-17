"""
Programa para pegar o CDI do site https://carteirarica.com.br/cdi-taxa/
"""

import bs4 as bs  # Pegar informacoes do HTML
import requests  # Fazer requisicoes

from pprint import pprint  # Imprimir bonitinho

html = requests.get("https://carteirarica.com.br/cdi-taxa/")

# Criando objeto BeautifulSoup a partir do HTML recuperado
soup = bs.BeautifulSoup(html.text, 'html5lib')
# Buscando todas as tags spans com classe = diano
spans = soup.findAll("span", {"class": "diano"})

pprint(spans)

# beautifulsoup retorna uma lista, por isso o for
for span in spans:
    cdi = span.text
    print(cdi)
