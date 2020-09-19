from idlelib import browser

import selenium
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

import EnterInSystem

db = EnterInSystem.createBd()



driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')

driver.get("https://www.cian.ru/snyat-kvartiru/")
driver.set_window_size(1920,1080)

mini = 0
maxi = 27000

while maxi<7000000:
    driver.find_element_by_name('max').clear()
    driver.find_element_by_name('max').send_keys(maxi)
    driver.find_element_by_name('min').clear()
    driver.find_element_by_name('min').send_keys(mini)
    time.sleep(2)

    element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[2]/div/div/div/div/div[2]/div[5]/div')
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
            i = 0
            k=0
            costil1 = 0
            costil2 = 0
            for i in range(27):
                try:
                    element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="TopOfferCard"]')
                except NoSuchElementException:
                    k+=1
                else:
                    element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="TopOfferCard"]')[i-costil2]
                    hover = ActionChains(driver).move_to_element(element_to_hover_over)
                    hover.perform()

                    time.sleep(0.05)
                    href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
                    db.addLink(href)
                    print(href)
                    print()
                    costil1+=1

                try:
                    element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="OfferCard"]')
                except NoSuchElementException:
                    k+=1
                else:
                    element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="OfferCard"]')[i-costil1]
                    hover = ActionChains(driver).move_to_element(element_to_hover_over)
                    hover.perform()

                    time.sleep(0.05)
                    href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
                    db.addLink(href)
                    print(href)
                    print()
                    costil2+=1

                try:
                    element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="CardComponent"]')
                except NoSuchElementException:
                    k+=1
                else:
                    element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="CardComponent"]')[i]
                    hover = ActionChains(driver).move_to_element(element_to_hover_over)
                    hover.perform()

                    time.sleep(0.05)
                    href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
                    db.addLink(href)
                    print(href)
                    print()

            if k == 3:
                break
            k = 0

            try:
                driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/div/ul/li[' + str(j) + ']/a')
            except NoSuchElementException:
                flag = False
            else:
                element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/div/ul')
                hover = ActionChains(driver).move_to_element(element_to_hover_over)
                hover.perform()
                driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[6]/div/ul/li[' + str(j) + ']/a').click()
                if j < 11:
                    j += 1
                time.sleep(2)