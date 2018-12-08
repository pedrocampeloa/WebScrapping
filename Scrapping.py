#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 18:42:29 2018

@author: pedrocampelo
"""
   import os
   
   os.chdir('/Users/pedrocampelo/Downloads')

   cwd = os.getcwd()
   cwd
    
#Exemplo CDI


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
    
    
    
    
    
#Pegar Dados de Títulos Públicos pelo site do Tesouro
    
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
    
    
#Pegar lista de ações:

import requests
import bs4 as bs
import pandas as pd
    
    
    
    
#Pegar dados de ações
  
#Criar lista com todos os ativos
import requests
import bs4 as bs
import pandas as pd

"http://cotacoes.economia.uol.com.br/acoes-bovespa.html?exchangeCode=.BVSP&page=2&size=20"

columns1 = ['nome', 'código']
lista = pd.DataFrame(columns=columns1)

url1 = 'http://cotacoes.economia.uol.com.br/acoes-bovespa.html'
payload1 = {'exchangeCode':'.BVSP', 'page': 1, 'size': 20}

while True:
    html = requests.get(url1, params=payload1)
    soup = bs.BeautifulSoup(html.text, 'html5lib')
    tables = soup.findAll('div', {'id': 'conteudo', 'class': 'box-conteudo', 'position':'relative;'})
 
    if len(tables) == 0:
        if payload1['page'] == 1:
            print('Acao nao encontrada')
        break
 
    for table in tables:
        # print(table)
        table_values = table.findChildren('ul')
        # print(values)
        trs = table_values[0].findAll('li')
        for tr in trs:
            values = [td.text for td in tr.findAll('span')]
            # print(values)
            # df.append(pd.Series(values, index=columns), ignore_index=True)
            lista.loc[len(df)] = values
    print('Page', payload1['page'], 'OK')
    payload1['page'] += 1
     
df.to_csv('lista.csv')




  
#Pegar os dados   
import requests
import bs4 as bs
import pandas as pd

from datetime import datetime
from dateutil.parser import parse
import pandas as pd
 
 
columns = ['data', 'cotacao', 'minima', 'maxima', 'variacao', 'variacao_percent', 'volume']
df = pd.DataFrame(columns=columns)
 

"http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=PETR4.SA&page=2&size=20"

 
url2 = 'http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html'
ticker = input('Digite o ticker da acao: ')
ticker = ticker.upper() + '.SA'
diainicial = input('Digite o dia de ínicio de sua série: ')
mesinicial = input('Digite o mês de ínicio de sua série: ')
anoinicial = input('Digite o ano de ínicio de sua série: ')
diafinal = input('Digite o dia do fim de sua série: ')
mesfinal= input('Digite o mês do fim de sua série: ')
anofinal = input('Digite o dia do fim de sua série: ')

payload2 = {'codigo': ticker, 'beginDay': diainicial, 
           'beginMonth': mesinicial, 'beginYear': anoinicial,
           'endDay': diafinal, 'endMonth': mesfinal,
           'endYear': anofinal, 'page': 1, 'size': 200}
 
while True:
    html = requests.get(url2, params=payload2)
    soup = bs.BeautifulSoup(html.text, 'html5lib')
    tables = soup.findAll('table', {'id': 'tblInterday', 'class': 'tblCotacoes'})
 
    if len(tables) == 0:
        if payload2['page'] == 1:
            print('Acao nao encontrada')
        break
 
    for table in tables:
        # print(table)
        table_values = table.findChildren('tbody')
        # print(values)
        trs = table_values[0].findAll('tr')
        for tr in trs:
            values = [td.text for td in tr.findAll('td')]
            # print(values)
            # df.append(pd.Series(values, index=columns), ignore_index=True)
            df.loc[len(df)] = values
    print('Page', payload2['page'], 'OK')
    payload2['page'] += 1
     
#df.to_csv('saida.csv')


df["volume"] = df["volume"].str.replace(".", "")
df=df.apply(lambda x: x.str.replace(",","."))


lista = list(df['data'])

lista1=[]
for i in range(0,len(lista)):
    lista1.append(datetime.strptime(lista[i], '%d/%m/%Y'))
print(len(lista1))

lista=[]
lista=lista1
df['index']=lista
df=df.set_index('index')                                      #colocando a data ajustada como index
df.sort_values(by=['index'], inplace=True, ascending=True)     #ordenando do menor para o maior
del df['data'], lista, lista1, i


#problema2: transformar o tempo em contínuo
datainicial_aux= diainicial+'/'+mesinicial+'/'+anoinicial
datainicial = datetime.strptime(datainicial_aux, '%d/%m/%Y')

datafinal_aux=diafinal+'/'+mesfinal+'/'+anofinal
datafinal = datetime.strptime(datafinal_aux, '%d/%m/%Y')
delta =  (datafinal - datainicial).days

df1 = pd.DataFrame(index=pd.date_range(datainicial, periods=delta))


#queria que os valores de df1 fossem iguais ao de df, quando o index é o mesmo. quando nao é, df1=0

#1tentativa
def dfajust(df_old, df_new):
    for i in range(0,len(df_new)):
        for j in range(0,len(df_old)):
            if (df_new.index[i]==df_old.index[j]):
                df_new['cotacao'][i]=df_old['cotacao'][j]
            else:   
                df_new['cotacao'][0]=0
    return df_new

#2tentativa
df1.insert(1, 'cotacao', df['cotacao']).map(df.index('MODEL'))


