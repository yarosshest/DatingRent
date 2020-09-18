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

db = EnterInSystem.createBd()

chrome_options = Options()
chrome_options.add_argument("--headless")

driver: WebDriver = webdriver.Chrome('D:\\chromedriver_win32\\chromedriver.exe')
#driver = webdriver.Chrome()

for site in db.getAllLinks():

    driver.get(site)

    obshplo = driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--info-value")]')[0].text
    opisanie = driver.find_element_by_xpath('//*[@id="description"]/div[2]/div/div/span/p').text
    price = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[3]/div/div[1]/div[1]/div[1]/div/div[1]/div/span/span[1]').text

    town = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/address/a[1]').text
    okreg = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/address/a[2]').text
    street = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/address/a[3]').text
    street2 = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/address/a[4]').text
    domnum = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/address/a[5]').text
    adress = town + ' ' + okreg + ' ' + street + ' ' + street2 + ' ' + domnum

    colcomn = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/h1').text

    metro = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/ul[1]/li[1]/a').text
    metrotime = driver.find_element_by_xpath(
        '//*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/ul[1]/li[1]/span').text

    colvo = driver.find_element_by_xpath('//*[@id="photos"]/div[2]/div/div[2]').text
    x = int(colvo.split()[0])

    fotoochka = ''
    print(obshplo)
    print(price, ' ', adress)
    print(metro, ' ', metrotime)

    ucan = ''  # можно с детьми / животными
    try:
        element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="Tenants"]')
    except NoSuchElementException:
        ucan = ''
    else:
        coll = len(driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]'))
        for i in range(coll):
            ucan = ucan + driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]')[
                i - 1].text + '/'
    print(ucan)

    items = ''  # итемы квартиры
    try:
        element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="Features"]')
    except NoSuchElementException:
        items = ''
    else:
        coll = len(driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]'))
        for i in range(coll - 1):
            items = items + driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]')[i].text + '/'
    print(items)

    for i in range(x):
        url = driver.find_element_by_xpath("//div[contains(@class, 'fotorama__active')]/img").get_attribute('src')

        element_to_hover_over = driver.find_element_by_xpath(
            '//*[@id="frontend-offer-card-fotorama"]/div/div[1]/div[1]')
        hover = ActionChains(driver).move_to_element(element_to_hover_over)
        hover.perform()

        driver.find_element_by_xpath('//div[@class="fotorama__arr fotorama__arr--next"]').click()
        fotoochka = fotoochka + url + ' '
        #    print(fotoochka)
        time.sleep(0.03)

    undergrounds = metro + " " + metrotime
    if db.RoomChek(site):
        EnterInSystem.createRoom(db, price, adress, undergrounds, opisanie, fotoochka, colcomn, obshplo, site)