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

import EnterInSystem

driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')

driver.get("https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=2&region=1&type=4")

element_to_hover_over = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[4]/div[1]/div/div[1]')
hover = ActionChains(driver).move_to_element(element_to_hover_over)
hover.perform()

href = driver.find_element_by_xpath('//*[@id="frontend-serp"]/div/div[4]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/a').get_attribute('href')
print(href)
#driver.get(href)

