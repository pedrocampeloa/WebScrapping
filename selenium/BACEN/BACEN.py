#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 22:03:35 2020

@author: pedrocampelo
"""

import selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
import time
import os
import shutil
from datetime import date

######## ########  ########  ######## PREFERENCIAS DO WEBDRIVER ######## ########  ########  ########

chrome_options = Options()
#chrome_options.add_argument("--headless")

Initial_path = r"/Users/pedrocampelo/Projects/selenium/BACEN"
#os.chdir('/Users/pedrocampelo/Desktop/Work/Programming/Python/Scrapping BC')



prefs = {"download.default_directory" : Initial_path}
chrome_options.add_experimental_option("prefs",prefs)
chrome_path = which("./chromedriver")

#driver = webdriver.Chrome(executable_path=chrome_path, options = chrome_options)
driver = webdriver.Chrome(executable_path="/Users/pedrocampelo/Projects/selenium/chromedriver", options = chrome_options)

driver.get("https://www3.bcb.gov.br/expectativas/publico/consulta/serieestatisticas/")

######## ########  ###########  PARÂMETROS ######## ########  ########  ########

# 1) INDICADOR: OPCOES:
#  0=Bal.Com.,
#  1=BP,
#  2=Fiscal,
#  3= ÍndicesPreços,
#  4=Infl.Acumulada 12 meses;
#  5=Infl.Acumulada 12 meses suavizada, 
#  6=Meta para Taxa Over-selic,
#  7=PIB,
#  8=Preços Administrados por Contrato e Monitorados, 
#  9=Produção Industrial, 
#  10=Taxa de Câmbio,
#  11=Indicadores do Top 5;

indicador = 11

# 2) Tipo de índice:

    # if indicador in [3,4,5]: (0=IGP-DI, 1=IGP-M, 2=INPC, ...
    # ... , 3=IPA-DI, 4=IPA-M, 5=IPCA, 6=IPCA últimos 5 dias úteis, 7=IPCA-15, 8=IPC-Fipe)

    # if indicador == 11: (0=IGP-DI, 1=IGP-M, 2=IPCA, 3=Taxa de cambio, 4=Selic Meta)

    # if indicador == 7: (0=AGRIC, 1=IND, 2=SERV, 3= TOTAL)


indice_escolhido = 4

# 3) Estatística escolhida (0=Média, 1=Mediana, 2=DP, 3=var, 4=max, 5=min, 6=numero de respostas)

est = 3

# 3.1) Caso indicador=TOP 5, devemos ainda escolher o Ranking, onde 0 = de CP; 1 = de Médio; 2 = de Longo Prazo

rank = 1 # nao tem problema deixar visivel mesmo que indicador != TOP 5


# 4) Frequência dos dados 

    # if indicador in [0,1,2,8]: Esses indicadores só são disponiveis anualmente
    # if indicador in [3,6,9,10,11]: Esses indicadores são disponibilizados mensalmente (0) e anualmente (1)
    # if indicador == 7: PIB é disponibilizado trimensalmente (0) e anualmente (1)
    # if indicador in [4,5]: nao precisa fazer nada, pode deixar o numero que esta

freq = 0

# 4.1) Tipo de taxa 

    # if indicador in [6,10]: (0 = Final do período; 1 = Média do período)

tipo = 1 

# 5) Datas

# 5.1) Período no qual foram feitas as projeções: início

data_inicial = "01/01/2019"

# 5.2) Período no qual foram feitas as projeções: fim

data_final = "12/12/2019"

# 5.3) Período das projecoes (Depende do tipo de indicador): início

mes_inicio = 0 # (jan=0, dez=11)
tri_inicio = 0 # (jan-mar=0, out-dez=3)
ano_inicio = 21 # (1999=0, 2025=26)

# 5.4) Período das projecoes (Depende do tipo de indicador): fim

mes_fim = 3 # (jan=0, dez=11)
tri_fim = 1 # (jan-mar=0, out-dez=3)
ano_fim = 21 # (1999=0, 2025=26)

# 5.5) Data da coleta

vintage = date.today()

######## ########  ########  Período no qual foram feitas as projeções: início ######## ########  ######## 

d0 = driver.find_element_by_id("tfDataInicial1") 
d0.send_keys(data_inicial)

######## ########  ########   Período no qual foram feitas as projeções: fim ######## ########  ########  

d1 = driver.find_element_by_id("tfDataFinal2") 
d1.send_keys(data_final)


######## ########  ########  ######## Selecionando o indicador ######## ########  ########  ########


variavel = driver.find_element_by_xpath("//select[@id='indicador']//option[@value='{}']".format(indicador))
variavel.click()

######## ########  ########  ######## Escolhendo o tipo de índice: ######## ########  ########  ########

if indicador in [3,4,5]:

    indice = driver.find_element_by_xpath("(//input[@id='grupoIndicePreco:opcoes_{0}'])".format(indice_escolhido))
    indice.click()

else:
    pass

if indicador == 11:

    indice = driver.find_element_by_xpath("(//input[@id='opcoesd_{0}'])".format(indice_escolhido))
    indice.click()
    
else:
    pass

if indicador == 7:

    indice = driver.find_element_by_xpath("(//input[@id='grupoPib:opcoes_{0}'])".format(indice_escolhido))
    indice.click()
else: 
    pass


time.sleep(1)

######## ########  ########  ######## ESTATISTICA ######## ########  ########  ########

estatistica = driver.find_element_by_xpath("(//select[@id='calculo']/option[@value='{0}'])".format(est))
estatistica.click()
time.sleep(1)

if indicador == 11: 
    ranking = driver.find_element_by_xpath("(//select[@id='tipoRanking']/option[@value='{0}'])".format(rank))
    ranking.click()
    time.sleep(1)
else:
    pass


######## ########  ########  ########  Periodicidade ########  ########  ########  ######## 


if indicador in [0,1,2,8]:

# Esses indicadores só são disponiveis anualmente

    freq = 99

    period = driver.find_element_by_xpath('//select[@id="periodicidade"]//option[@value="0"]')
    period.click()

else:
    pass

if indicador in [3,6,9,10,11]:

# Esses indicadores são disponibilizados mensalmente (0) e anualmente (1)

    period = driver.find_element_by_xpath('//select[@id="periodicidade"]//option[@value="{0}"]'.format(freq))
    period.click()

    if freq == 1 & indicador in [6,10]:
        taxa = driver.find_element_by_xpath('//select[@id="tipoDeTaxa"]//@value="{0}"]'.format(tipo))
        taxa.click()
    else:
        pass   
else:
    pass

if indicador == 7:

# PIB é disponibilizado trimensalmente (0) e anualmente (1)
    
    period = driver.find_element_by_xpath('//select[@id="periodicidade"]//option[@value="{0}"]'.format(freq))
    period.click()
    
else:
    pass

if indicador in [4,5]:
    freq = 999
else:
    pass


time.sleep(1)

######### ########  ######## Período das projecoes:  ######## ########  ########  ########

# CASO MENSAL: MÊS 

if freq==0 and indicador != 7:

    mes_inicio_proj = driver.find_element_by_xpath("//select[@id='mesReferenciaInicial']//option[@value='{0}']".format(mes_inicio))
    mes_inicio_proj.click()
    time.sleep(1)

    mes_fim_proj = driver.find_element_by_xpath("//select[@id='mesReferenciaFinal']//option[@value='{0}']".format(mes_fim))
    mes_fim_proj.click()
    time.sleep(1)
else:
    pass

# CASO TRIMENSTRAL: TRIMESTRE

if freq==0 and indicador == 7:

    tri_inicio_proj = driver.find_element_by_xpath("//select[@id='triReferenciaInicial']//option[@value='{0}']".format(tri_inicio))
    tri_inicio_proj.click()
    time.sleep(1)

    tri_fim_proj = driver.find_element_by_xpath("//select[@id='triReferenciaFinal']//option[@value='{0}']".format(tri_fim))
    tri_fim_proj.click()
    time.sleep(1)
else:
    pass


# CASO MENSAL: ANO

if freq==0 and indicador != 7:

    ano_inicio_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoMesReferencia:anoMesReferenciaInicial']//option[@value='{0}']".format(ano_inicio))
    ano_inicio_proj.click()
    time.sleep(1)

    ano_fim_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoMesReferencia:anoMesReferenciaFinal']//option[@value='{0}']".format(ano_fim))
    ano_fim_proj.click()
    time.sleep(1)

else:
    pass

# CASO TRIMESTRAL: ANO 

if freq==0 and indicador == 7:

    ano_inicio_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoTrimestreReferencia:anoTrimestreReferenciaInicial']//option[@value='{0}']".format(ano_inicio))
    ano_inicio_proj.click()
    time.sleep(1)

    ano_fim_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoTrimestreReferencia:anoTrimestreReferenciaInicial']//option[@value='{0}']".format(ano_fim))
    ano_fim_proj.click()
    time.sleep(1)

else:
    pass

# CASO ANUAL (SEM MES): ANO

if freq==99:

    ano_inicio_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoAnoReferencia:anoReferenciaInicial']//option[@value='{0}']".format(ano_inicio))
    ano_inicio_proj.click()
    time.sleep(1)

    ano_fim_proj = driver.find_element_by_xpath("//select[@name='divPeriodoRefereEstatisticas:grupoAnoReferencia:anoReferenciaInicial']//option[@value='{0}']".format(ano_fim))
    ano_fim_proj.click()
    time.sleep(1)

else:
    pass

######### ########  ##########  #########  Fazendo o download: ######### ########  ##########  #########

arquivo = driver.find_element_by_id("btnCSV9").click()
csv_file = driver.page_source
time.sleep(5)

# consultar = driver.find_element_by_id('indiceConsultar8') # Caso queira trabalhar com a planilha no Selenium
# consultar.click()
# time.sleep(1)

#########  ########  ##########   Mudando o nome do download:  ######### ########  ##########  #########

filename = max([Initial_path + f for f in os.listdir(Initial_path)],key=os.path.getctime)

shutil.move(filename,os.path.join(Initial_path,r"{0}.{1}.{2}.csv".format(vintage,indicador,est)))

time.sleep(20)

driver.close()
