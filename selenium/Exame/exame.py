from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import os.path
import pathlib
import pandas as pd
from datetime import date, datetime, timedelta
from pandas import DataFrame
from openpyxl.workbook import Workbook

chrome_options = Options()
#chrome_options.add_argument("--headless")

#chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path="/Users/pedrocampelo/Projects/selenium/chromedriver", options = chrome_options)
driver.get("https://exame.abril.com.br/?s=coronav%C3%ADrus")


i=1
j=1

titulos = []
subtitulos = []
datas = []
conteudos = []

while i < 11:

    xpath = "(//span[@class='list-item-title'])[{0}]//a".format(i)

    search_btn = driver.find_element_by_xpath(xpath)
    search_btn.click()

    time.sleep(2)

    
    titulo = driver.find_element_by_xpath("//h1[@class='article-title']").text
    titulos.append(str(titulo))

    subtitulo = driver.find_element_by_xpath("//h2[@class='article-subtitle']").text
    subtitulos.append(str(subtitulo))

    data = driver.find_element_by_xpath("//div[@class='article-date']//span").text
    datas.append(str(data))

    content = driver.find_elements_by_xpath("//section[@class='article-content']/p")

    texto_full = []

    for k in range(1, len(content)):

        xpath_texto = "//section[@class='article-content']/p[{0}]".format(k)

        texto = driver.find_element_by_xpath(xpath_texto).text

        time.sleep(.5)

        texto_full.append(str(texto))
    
    conteudos.append(str(texto_full))
    
    
    driver.back()


    if i==10 and j==1:

        next_btn = driver.find_element_by_xpath("//div[@class='pagination-releases']//a")
        next_btn.click()
        time.sleep(2)
        i=0
        j=2

        print(titulos)
        print(subtitulos)
        print(datas)
        print(conteudos)
    
    if i==10 and j==2:
    
        next_btn = driver.find_element_by_xpath("//div[@class='pagination-releases']//a[2]")
        next_btn.click()
        time.sleep(2)
        i=0
        print(titulos)
        print(subtitulos)
        print(datas)
        print(conteudos)

    i +=1
   


time.sleep(2)

#driver.close()

