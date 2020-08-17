import requests
import bs4 as bs
import pandas as pd
import pickle
import sys

# Puxa o nome dos 1965 ativos que vieram do site da uol e estao no arquivo chamado ativos
with open('ativos', 'rb') as f:
    ativos = pickle.load(f)
########


# Lista de acoes que o programa vai puxar
acoes = ['PETR4.SA', 'ABEV3.SA', 'B3SA3.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBSE3.SA', 'VALE3.SA',
         'WEGE3.SA', 'USIM5.SA', 'TAEE11.SA', 'SUZB3.SA', 'MGLU3.SA', 'KROT3.SA', 'FLRY3.SA',
         'EGIE3.SA', 'CVCB3.SA', 'CIEL3.SA', 'BRFS3.SA', 'ITSA4.SA', 'LAME4.SA']
#########



# Nome base das colunas, na hora o codigo ja adiciona o ticker da acao no final
columns = ['data', 'cotacao', 'min', 'max', 'variacao', 'variacao_percent', 'volume']
#########

# URL que vai puxar o payload base. Se for mudar as datas tem que mudar aqui
url = 'http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html'
base_payload = {'codigo': '', 'beginDay': 16,
                'beginMonth': 11, 'beginYear': 2006,
                'endDay': 16, 'endMonth': 11,
                'endYear': 2018, 'page': 1, 'size': 200}
#########


# Funcao que recebe um payload e retorna um dataframe com os 
# dados da acao passado no codigo do payload
def get_data(payload):
    global url
    global columns
    stock_columns = [x + '_' + payload['codigo'][:-3] for x in columns]
    df = pd.DataFrame(columns=stock_columns)
    print('Pegando dados da acao ' + payload['codigo'] + ' (', end='', flush=True)
    while True:
        html = requests.get(url, params=payload)
        soup = bs.BeautifulSoup(html.text, 'html5lib')
        tables = soup.findAll('table', {'id': 'tblInterday', 'class': 'tblCotacoes'})

        if len(tables) == 0:
            if payload['page'] == 1:
                print('Acao nao encontrada')
            break

        for table in tables:
            table_values = table.findChildren('tbody')
            trs = table_values[0].findAll('tr')
            for tr in trs:
                values = [td.text for td in tr.findAll('td')]
                df.loc[len(df)] = values
        print('.', end='', flush=True)
        payload['page'] += 1
    print(') DONE')
    return df

# Rodando a funcao para todas as acoes da lista acoes e guarndando os resultados em dfs
dfs = []
for i in acoes:
    base_payload['codigo'] = i
    base_payload['page'] = 1
    a = get_data(base_payload)
    dfs.append(a)



# concatenando todos os dataframes em dfs e alvando em um arquivo chamado dataframe_acoes
result = pd.concat(dfs, axis=1)
print(result.head())

result.to_pickle('dataframe_acoes')

# O arquivo foi salvo no formato pickle pois nesse formato a leitura e escrita eh mais rapida
# se achar melhor pode salvar um csv tambem

# Pra ler do arquivo pickle basta usar
# df = pd.read_pickle('dataframe_acoes')
