from idlelib import browser
import selenium
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium import webdriver
import urllib                                                                                            #библиотечки
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver                                                #много библиотечек
import bs4
import re
from bs4 import BeautifulSoup
import EnterInSystem
import requests

import EnterInSystem
                                        #эскьюэлька
db = EnterInSystem.createBd()



driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe') #еще ода библиотечка, но специфичная, в анаконде такой нет

mini = 0
maxi = 27000 #рамки цен

while maxi<7000000:
    driver.get("https://www.cian.ru/snyat-kvartiru/") #открываем сайт
    driver.set_window_size(1920, 1080) #разворачиваем страницу

    element_to_hover_over = driver.find_element_by_name('min')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()                                          #вводим мин цену
    driver.find_element_by_id("min-0").click()
    driver.find_element_by_name('min').send_keys(mini)

    element_to_hover_over = driver.find_element_by_name('max')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()                                          #вводим макс цену
    driver.find_element_by_id("max-0").click()
    driver.find_element_by_name('max').send_keys(maxi)
    time.sleep(1) #ждем прогружения

    element_to_hover_over = driver.find_element_by_xpath('//button[contains(text(),"Показать")]')
    hover = ActionChains(driver).move_to_element(element_to_hover_over) #жмем на кнопку с результатами
    hover.perform()
    driver.find_element_by_xpath('//button[contains(text(),"Показать")]').click()

    if maxi<=100000:
        mini = maxi + 1    #шаг цены в 1000руб
        maxi += 1000
    elif maxi<=200000:
        mini = maxi + 1    #шаг цены в 20000руб
        maxi += 20000
    elif maxi<=500000:
        mini = maxi + 1    #шаг цены в 50000руб
        maxi += 50000
    else:
        mini = maxi+1    #финальная цена
        maxi = 7000000
    j=2

    flag = True
    while flag:
        time.sleep(1)  #спим
        topcol = len(driver.find_elements_by_xpath('//*[contains(@data-name,"OfferCard")]'))     #количество ссылок на квартиры на странице
        print(topcol)
        for i in range(topcol-1):
            element_to_hover_over = driver.find_elements_by_xpath('//*[contains(@data-name,"OfferCard")]')[i]
            hover = ActionChains(driver).move_to_element(element_to_hover_over)  #наводимся на квартиру, иначе работать не будет
            try:
                driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i]  #проверка на вшивость
            except StaleElementReferenceException:
                pass  #нет так нет
            else:
                href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')  #тырим ссылку
                db.addLink(href)
                print(href)
                print()
                time.sleep(0.02)  #спим

        cardcol = len(driver.find_elements_by_xpath('//*[@data-name="CardComponent"]'))  #хрень под названием вторая версия страницы
        for i in range(cardcol-1):
            element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="CardComponent"]')[i]  #все аналогично, но html страницы другой
            hover = ActionChains(driver).move_to_element(element_to_hover_over)

            href = driver.find_elements_by_xpath('//*[@class="_93444fe79c--link--39cNw"]')[i].get_attribute('href')  #довольно-таки бесячая хрень
            db.addLink(href)
            print(href)
            print()
        time.sleep(0.02)  #спим

        time.sleep(1)  #все еще спим
        print(len(driver.find_elements_by_xpath('//*[@class ="_93444fe79c--list-itemLink--3o7_6"]')))
        if len(driver.find_elements_by_xpath('//*[@class ="_93444fe79c--list-itemLink--3o7_6"]'))+1<j:  #проверка на количество кнопок
            flag = False
        else:
            element_to_hover_over = driver.find_element_by_xpath('//*[@class="_93444fe79c--list--HEGFW"]/li['+str(j)+']')
            hover = ActionChains(driver).move_to_element(element_to_hover_over)           #видим кнопку - нажимаем на кнопку
            driver.find_element_by_xpath('//*[@class="_93444fe79c--list--HEGFW"]/li['+str(j)+']/a').click()
            if j < 11:  #костыль
                j += 1
            time.sleep(1)  #спим