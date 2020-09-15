from idlelib import browser
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import urllib
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
import bs4
import re
from bs4 import BeautifulSoup
import EnterInSystem
import requests

driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')

driver.get("https://www.cian.ru/snyat-kvartiru/")
heig = 500
heig1 = 0
driver.execute_script("window.scrollTo(" + str(heig1) + ", " + str(heig) +")")
for i in range(28):
    #if i==3:
    #    i=4
    #element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/div['+str(i+1)+']/div/div[1]')
    element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/article['+str(i+1)+']')
    hover = ActionChains(driver).move_to_element(element_to_hover_over) #//*[@id="frontend-serp"]/div/div[6]/div[1]/div/div[1] //*[@id="frontend-serp"]/div/div[6]/article[1]/div
    hover.perform()
    heig+=500
    heig1+=500
    time.sleep(1)
    #href = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/a').get_attribute('href')
    href = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/article['+str(i+1)+']/div/div[2]/div[1]/div/a').get_attribute('href')
    print(href)
    driver.execute_script("window.scrollTo(" + str(heig1) + ", " + str(heig) +")")
    print()
#driver.get(href)

