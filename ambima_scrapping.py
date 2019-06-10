#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 20:12:05 2019

@author: pedrocampelo
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup



def set_data(hoje='s'):
    
    """"
    Esta função trás a data que vai ser consultada
    Lembrando que o site da AMBIMA trás os valores somente para os últimos 5 dias úteis
    Caso nao queria o dia de hoje mudar no código
    O formato da data tem que ser em ddmmmaaaa (ex: 01jan2015)    
    """
    if hoje=='s':
	data=ts.hoje - 1 	#Verificar como deixar a data no formato certo
	
    else:
    	data=input('Insira o data a ser consultada: ')
    
    return data


def set_request(data, indicador):
    
    """"
    Esta função trás acha o site e verifica se os dados são possiveis de serem extraídos
        Caso seja possível, aparecerá 'Requisição bem sucedida!'.
        Caso contrário, aparecerá 'Falha na requisição'
        
    Além disso, essa função devolve um dataframe bagunçado
    """
    
    req = requests.get('http://www.anbima.com.br/merc_sec_debentures/resultados/mdeb_'+data+'_'+indicador+'.asp')

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content
    else:
        print('Falha na requisição')
        
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(name='table')
    
    table_str = str(table)
    df_aux = pd.read_html(table_str)[0]


    return df_aux



def set_dataframe(df_aux, indicador):
    """"
    Esta organiza o df para o formato que queremos
    """
    
    columns=['Código', 'Nome', 'Repac./Venc.', 'Índice/Correção', 'Taxa de Compra',
    'Taxa de Venda','Taxa Indicativa','Desvio Padrão','Intervalo Indicativo', 'PU',
	'% PU Par',	'Duration', '% Reune', 'X']

    
        
    df=df_aux[[x for x in range (14)]][7:-3]
    
    df.columns=columns
    
    return df
        


def save_df(df, indicador, data):

    """"
    Essa função abre o arquivo xlxs, appenda os novos dados e salva o df
    """    
 
    
#    writer = pd.ExcelWriter('dados_lag'+str(forecastHorizon)+'v2.xlsx')
#    coef_sum_df.to_excel(writer,'coeficientes_lag'+str(forecastHorizon))
#    previsao.set_index('Modelos')
#    previsao.to_excel(writer,'previsao_lag'+str(forecastHorizon))
#    writer.save()
    
    return None



if __name__== "__main__":
  
    
    """"
    Em cima eu desenvolvi todas as funções, aqui em baixo eu rodo cada uma termino o código.
    """"
    
    indicador_lista = ['di_spread', 'di_percentual', 'ipca_spread']
    
    for indicador in indicador_lista:
        
        data=set_data()
        df_aux=set_request(data, indicador)
        df=set_dataframe(df_aux, indicador)
        save_df(df, indicador, data)
        
        
        
        
    
    
    
