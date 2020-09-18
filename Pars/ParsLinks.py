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

driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')

driver.get("https://www.cian.ru/snyat-kvartiru/")
driver.set_window_size(1920,1080)


j=2
costil = 7
while True:
        if j>2:
            costil=6
        i = 0
        for i in range(27):
            element_to_hover_over = driver.find_elements_by_xpath('//*[@data-name="TopOfferCard"]')[i]
            hover = ActionChains(driver).move_to_element(element_to_hover_over)
            hover.perform()

            time.sleep(0.05)
            href = driver.find_elements_by_xpath('//*[@class="c6e8ba5398--header--1fV2A"]')[i].get_attribute('href')
            print(href)
            print()

        element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div['+str(costil)+']/div/ul')
        hover = ActionChains(driver).move_to_element(element_to_hover_over)
        hover.perform()
        driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div['+str(costil)+']/div/ul/li[' + str(j) + ']/a').click()
        if j < 11:
            j += 1
        time.sleep(2)