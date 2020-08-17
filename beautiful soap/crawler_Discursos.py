# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:09:03 2018

@author: daniel
"""
  
    
import csv

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import requests
import os
import time
from numpy import random



cont=0
#https://dadosabertos.camara.leg.br/api/v2/deputados/74646/discursos?dataInicio=2002-01-01&dataFim=2018-12-31&pagina=1&itens=1000

thePage='https://dadosabertos.camara.leg.br/api/v2/deputados/'
complemento1='/discursos?dataInicio='
complemento2='&dataFim='
complemento3='&pagina='
complemento4='&itens=100'

# Problems: deputado 117,

theSubPage='https://dadosabertos.camara.leg.br/api/v2/deputados/'
if __name__=="__main__":

    for i in range(56,56+1):
        print(i)
        dfLegis=pd.read_csv("legislaturas.csv", header=0, sep=';')    
        dataInicio=list(dfLegis['dataInicio'][dfLegis.idLegis == i])[0]
        dataFim=list(dfLegis['dataFim'][dfLegis.idLegis == i])[0]
        dfDeputados=pd.read_csv("DeputadosPorLegislatura/deputados"+str(i)+".csv", header=0, sep=';')
        for index, row in dfDeputados.iterrows():
            print('deputadoCount',index)
            if(1<=index and index<10000): 
                time.sleep(int(3*random.random()))
                idDeputado=row['idDeputado']
                databaseItems=pd.DataFrame(columns=['idDeputado','idDisc','uriEvento',
                'dataHoraInicio','dataHoraFim','descricaoTipo','descricao','localCamara',
                'titulo','tipoDiscurso','keywords','sumario','transcricao'])
                thereArePages=True
                pageNumber=0
                numberOfDiscursos=0
                while(thereArePages):
                    pageNumber=pageNumber+1
                    print(pageNumber)
                    itemPage=thePage+str(idDeputado)+complemento1+str(dataInicio)+complemento2+str(dataFim)+complemento3+str(pageNumber)+complemento4
                    itemPage=str(itemPage)                
                    response = requests.get(itemPage, headers={"accept": "application/xml"})
                    soupItem=BeautifulSoup(response.text,'xml')
                    print(soupItem.prettify())
                    item=soupItem.findAll('discurso')
                    if(len(item)==0):
                        thereArePages=False
                        print('pageNumber',pageNumber)
                    #print(item)    
                    for subItem in item:
                        numberOfDiscursos=numberOfDiscursos+1
                        try:
                            uriEvento=subItem.find('uriEvento').get_text()                           
                        except:
                            uriEvento=''
                    #print(uriEvento)
                        try:
                            titulo=subItem.find('titulo').get_text()
                        except:
                            titulo=''
                        try:
                            tipoDiscurso=subItem.find('tipoDiscurso').get_text()
                        except:
                            tipoDiscurso=''
                        try:    
                            keywords=subItem.find('keywords').get_text()
                        except:
                            keywords=''
                        try:    
                            sumario=subItem.find('sumario').get_text()
                        except:
                            sumario=''
                        try:    
                            transcricao=subItem.find('transcricao').get_text()
                        except:
                            transcricao=''
                            
                        subItemPage=str(uriEvento)
                        if(subItemPage!=''):
                            responseSubItem = requests.get(subItemPage, headers={"accept": "application/xml"})                    
                            soupSubItem=BeautifulSoup(responseSubItem.text,'xml')
                            try:
                                idDisc=soupSubItem.find('id').get_text()
                            except:
                                idDisc=''
                            try:
                                dataHoraInicio=soupSubItem.find('dataHoraInicio').get_text()
                            except:
                                dataHoraInicio=''
                            try:
                                dataHoraFim=soupSubItem.find('dataHoraFim').get_text()                    
                            except:
                                dataHoraFim=''
                            try:
                                descricaoTipo=soupSubItem.find('descricaoTipo').get_text()
                            except:
                                descricaoTipo=''
                            try:
                                descricao=soupSubItem.find('descricao').get_text()
                            except:
                                descricao=''
                            try:
                                localCamara=soupSubItem.find('nome').get_text()
                            except:
                                localCamara=''
                            databaseItems=databaseItems.\
                            append({'idDisc':idDisc,
                                    'uriEvento':uriEvento,
                                    'dataHoraInicio':dataHoraInicio,
                                    'dataHoraFim':dataHoraFim,
                                    'descricaoTipo':descricaoTipo,
                                    'descricao':descricao,
                                    'localCamara':localCamara,
                                    'titulo':titulo,
                                    'tipoDiscurso':tipoDiscurso,
                                    'keywords':keywords,
                                    'sumario':sumario,
                                    'transcricao':transcricao},ignore_index=True)
                        else:
                            databaseItems=databaseItems.\
                            append({'idDisc':'',
                                    'uriEvento':'',
                                    'dataHoraInicio':'',
                                    'dataHoraFim': '',
                                    'descricaoTipo':'',
                                    'descricao':'',
                                    'localCamara':'',
                                    'titulo':titulo,
                                    'tipoDiscurso':tipoDiscurso,
                                    'keywords':keywords,
                                    'sumario':sumario,
                                    'transcricao':transcricao},ignore_index=True)                        
                print(numberOfDiscursos)                
                databaseItems.loc[:,'idDeputado']= str(idDeputado)
                databaseItems.to_csv('DiscursosPorLegislatura/'+str(i)+'/'+str(idDeputado)+'.csv',sep=';',index=False, header=True,encoding='utf-8-sig')
    
    
                
             


#                sizeNovo=os.path.getsize('DiscursosPorLegislatura/Novos/'+str(i)+'/'+str(idDeputado)+'.csv')
#                sizeVelho=os.path.getsize('DiscursosPorLegislatura/'+str(i)+'/'+str(idDeputado)+'.csv') 
#
#                if(sizeVelho>=sizeNovo):
#                    os.remove('DiscursosPorLegislatura/Novos/'+str(i)+'/'+str(idDeputado)+'.csv')
#                else:
#                    print(sizeVelho,sizeNovo)
                    