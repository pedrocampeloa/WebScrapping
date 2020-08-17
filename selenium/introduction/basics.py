#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:51:26 2020

@author: pedrocampelo
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which


chrome_options = Options()
chrome_options.add_argument("--headless")         #to no open chrome

#chrome_path = which("chromedriver")
driver = webdriver.Chrome(executable_path="/Users/pedrocampelo/Projects/selenium/chromedriver", options = chrome_options)
driver.get("https://duckduckgo.com")

#insert search
#search_input= driver.find_element_by_id("search_form_input_homepage")
search_input= driver.find_element_by_xpath("(//input[contains(@class, 'js-search-input')])[1]")

search_input.send_keys("My User Agent")




##click search button
#search_btn = driver.find_element_by_id("search_button_homepage")
#search_btn.click()

#press enter
search_input.send_keys(Keys.ENTER)

##get page source
a = driver.page_source
print(a)

driver.close()

