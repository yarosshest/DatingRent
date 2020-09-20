from idlelib import browser

import selenium
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
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

import EnterInSystem

db = EnterInSystem.createBd()



driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')

mini = 0
maxi = 27000

while maxi<7000000:
    driver.get("https://www.cian.ru/snyat-kvartiru/")
    driver.set_window_size(1920, 1080)

    element_to_hover_over = driver.find_element_by_name('min')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_id("min-0").click()
    driver.find_element_by_name('min').send_keys(mini)

    element_to_hover_over = driver.find_element_by_name('max')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_id("max-0").click()
    driver.find_element_by_name('max').send_keys(maxi)
    time.sleep(1)

    element_to_hover_over = driver.find_element_by_xpath('//button[contains(text(),"Показать")]')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element_by_xpath('//button[contains(text(),"Показать")]').click()

    if maxi<=200000:
        mini = maxi+1
        maxi += 1000
    elif maxi<=500000:
        mini = maxi + 1
        maxi += 50000
    else:
        mini = maxi+1
        maxi = 7000000
    j=2

    flag = True
    while flag:
        time.sleep(1)
        topcol = len(driver.find_elements_by_xpath('//*[contains(@data-name,"OfferCard")]'))
        print(topcol)
        for i in range(topcol-1):
            element_to_hover_over = driver.find_elements_by_xpath('//*[contains(@data-name,"OfferCard")]')[i]
            hover = ActionChains(driver).move_to_element(element_to_hover_over)
            try:
                driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i]
            except StaleElementReferenceException:
                pass
            else:
                href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
                db.addLink(href)
                print(href)
                print()
                time.sleep(0.02)

        cardcol = len(driver.find_elements_by_xpath('//*[@data-name="CardComponent"]'))
        for i in range(cardcol-1):
            element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="CardComponent"]')[i]
            hover = ActionChains(driver).move_to_element(element_to_hover_over)

            href = driver.find_elements_by_xpath('//*[@class="_93444fe79c--link--39cNw"]')[i].get_attribute('href')
            db.addLink(href)
            print(href)
            print()
        time.sleep(0.02)

        time.sleep(1)
        print(len(driver.find_elements_by_xpath('//*[@class ="_93444fe79c--list-itemLink--3o7_6"]')))
        if len(driver.find_elements_by_xpath('//*[@class ="_93444fe79c--list-itemLink--3o7_6"]'))+1<j:
            flag = False
        else:
            element_to_hover_over = driver.find_element_by_xpath('//*[@class="_93444fe79c--list--HEGFW"]/li['+str(j)+']')
            hover = ActionChains(driver).move_to_element(element_to_hover_over)
            driver.find_element_by_xpath('//*[@class="_93444fe79c--list--HEGFW"]/li['+str(j)+']/a').click()
            #                             //*[@id="frontend-serp"]/div/div[7]/div/ul/li[2]/a<ul class="_93444fe79c--list--HEGFW">
            if j < 11:
                j += 1
            time.sleep(1)