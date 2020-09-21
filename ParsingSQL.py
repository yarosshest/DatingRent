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
# driver = webdriver.Chrome()

for site in db.getAllLinks():
    if db.RoomChek(site):
        driver.get(site)
        driver.set_window_size(1920, 1080)
        try:
            obshplo = driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--info-value")]')[0].text
            opisanie = driver.find_element_by_xpath('//*[@id="description"]/div[2]/div/div/span/p').text
            price = driver.find_element_by_xpath('//*[contains(text(),"₽/мес")]').text
            #                                       //*[@id="frontend-offer-card"]/main/div[2]/div[1]/section/div/div[1]/div[2]/span
            # <a data-name="Link" href="https://www.cian.ru/snyat-2-komnatnuyu-kvartiru/" class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr">Москва</a>
            adrcol = len(
                driver.find_elements_by_xpath('//*[@class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr"]'))
            adress = ''
            for i in range(adrcol - 1):
                adress = adress + driver.find_elements_by_xpath(
                    '//*[@class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr"]')[i].text + ' '
            colcomn = driver.find_element_by_xpath('//*[@data-name="OfferTitle"]').text
            #
            metro = driver.find_element_by_xpath('//*[contains(@class,"underground_link")]').text
            metrotime = driver.find_element_by_xpath('//*[contains(@class,"underground_time")]').text

            fotoochka = ''
            # print(obshplo)
            # print(price, ' ', adress, ' ', colcomn[0])
            # print(metro, ' ', metrotime)

            ucan = ''  # можно с детьми / животными
            try:
                element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="Tenants"]')
            except NoSuchElementException:
                ucan = ''
            else:
                coll = len(driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]'))
                for i in range(coll):
                    ucan = ucan + \
                           driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]')[
                               i - 1].text + '/'
            # print(ucan)

            items = ''  # итемы квартиры
            try:
                element_to_hover_over = driver.find_element_by_xpath('//*[@data-name="Features"]')
            except NoSuchElementException:
                items = ''
            else:
                coll = len(driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]'))
                for i in range(coll - 1):
                    items = items + driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]')[i].text + '/'
            # print(items)

            colvo = driver.find_element_by_xpath('//*[@id="photos"]/div[2]/div/div[2]').text
            x = colvo.split()[0]
            try:
                x = int(x)
            except ValueError:
                colvo = driver.find_element_by_xpath('//*[@id="photos"]/div[2]/div[2]/div[2]').text
                x = int(colvo.split()[0])

            for i in range(x):
                url = driver.find_element_by_xpath("//div[contains(@class, 'fotorama__active')]/img").get_attribute(
                    'src')

                element_to_hover_over = driver.find_element_by_xpath(
                    '//*[@id="frontend-offer-card-fotorama"]/div/div[1]/div[1]')
                hover = ActionChains(driver).move_to_element(element_to_hover_over)
                hover.perform()

                driver.find_element_by_xpath('//div[@class="fotorama__arr fotorama__arr--next"]').click()
                fotoochka = fotoochka + url + ' '
                #    print(fotoochka)
                time.sleep(0.2)

            undergrounds = metro + " " + metrotime

            room = EnterInSystem.Apartments()
            room.undergrounds = undergrounds
            room.address = adress
            room.discription = opisanie
            room.photo = fotoochka
            room.room = colcomn
            room.link = site
            room.price = price
            room.area = obshplo
            room.items = items
            room.ucan = ucan

            db.addRoom(room)
        # except:
        #     pass
        except OSError as err:
            print("OS error: {0}".format(err))