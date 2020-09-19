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

mini = 27000
maxi = 27000

while maxi<7000000:
    driver.find_element_by_id('max-0').clear()
    driver.find_element_by_name('max').send_keys(maxi)
    driver.find_element_by_id('min-0').clear()
    driver.find_element_by_name('min').send_keys(mini)
    time.sleep(2)

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
            topcol = len(driver.find_elements_by_xpath('//*[@data-name="TopOfferCard"]'))
            for i in range(topcol-1):
                # element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="TopOfferCard"]')[i]
                # hover = ActionChains(driver).move_to_element(element_to_hover_over)
                # hover.perform()

                href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
                db.addLink(href)
                print(href)
                print()

            # offercol = len(driver.find_elements_by_xpath('//*[@data-name="OfferCard"]'))
            # for i in range(offercol-1):
            #     element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="OfferCard"]')[i]
            #     hover = ActionChains(driver).move_to_element(element_to_hover_over)
            #     hover.perform()
            #
            #     time.sleep(0.05)
            #     href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i+topcol].get_attribute('href')
            #     db.addLink(href)
            #     print(href)
            #     print()

            cardcol = len(driver.find_elements_by_xpath('//*[@data-name="CardComponent"]'))
            for i in range(cardcol-1):
                # element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="CardComponent"]')[i]
                # hover = ActionChains(driver).move_to_element(element_to_hover_over)
                # hover.perform()

                href = driver.find_elements_by_xpath('//*[@class="_93444fe79c--link--39cNw"]')[i].get_attribute('href')
                db.addLink(href)
                print(href)
                print()

            try:
                driver.find_element_by_link_text(str(j))
            except NoSuchElementException:
                flag = False
            else:
                element_to_hover_over = driver.find_element_by_link_text(str(j))
                hover = ActionChains(driver).move_to_element(element_to_hover_over)
                hover.perform()
                time.sleep(0.01)
                driver.find_element_by_link_text(str(j)).click()
                j += 1
                time.sleep(2)