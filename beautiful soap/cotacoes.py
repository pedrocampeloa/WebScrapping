import requests
import bs4 as bs
import pandas as pd


columns = ['data', 'cotacao', 'minima', 'maxima', 'variacao', 'variacao_percent', 'volume']
df = pd.DataFrame(columns=columns)


url = 'http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html'
ticker = input('Digite o ticker da acao: ')
ticker = ticker.upper() + '.SA'
payload = {'codigo': ticker, 'beginDay': 16, 
           'beginMonth': 11, 'beginYear': 2006,
           'endDay': 16, 'endMonth': 11,
           'endYear': 2018, 'page': 1, 'size': 200}

while True:
    html = requests.get(url, params=payload)
    soup = bs.BeautifulSoup(html.text, 'html5lib')
    tables = soup.findAll('table', {'id': 'tblInterday', 'class': 'tblCotacoes'})

    if len(tables) == 0:
        if payload['page'] == 1:
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
    print('Page', payload['page'], 'OK')
    payload['page'] += 1

df.to_csv('saida.csv')
