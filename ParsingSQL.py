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
from len import preprocess_text
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
            driver.find_element_by_xpath('//*[contains(text(),"Объявление снято с публикации")]')
            db.dellLink(site)
        except NoSuchElementException:
            try:
                obshplo = driver.find_elements_by_xpath('//*[contains(@class,"a10a3f92e9--info-value")]')[
                    0].text  # общая площадь квартиры
                opisanie = driver.find_element_by_xpath(
                    '//*[@id="description"]/div[2]/div/div/span/p').text  # описание квартиры
                price = driver.find_element_by_xpath('//span[contains(text(),"₽/мес")]').text  # цена

                adrcol = len(driver.find_elements_by_xpath(
                    '//*[@class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr"]'))  # количество элементов адреса
                adress = ''  # инициализация
                for i in range(adrcol - 1):
                    adress = adress + driver.find_elements_by_xpath(
                        '//*[@class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr"]')[
                        i].text + ' '  # сборка адресо в целостный вид
                colcomn = driver.find_element_by_xpath('//*[@data-name="OfferTitle"]').text  # кол-во комнат
                #
                metro = driver.find_element_by_xpath('//*[contains(@class,"underground_link")]').text  # метро
                metrotime = driver.find_element_by_xpath(
                    '//*[contains(@class,"underground_time")]').text  # время до метра

                fotoochka = ''  # инициализация
                # print(obshplo)
                # print(price, ' ', adress, ' ', colcomn[0])
                # print(metro, ' ', metrotime)

                ucan = ''  # можно с детьми / животными
                try:
                    element_to_hover_over = driver.find_element_by_xpath(
                        '//*[@data-name="Tenants"]')  # проверка на вшивость
                except NoSuchElementException:
                    ucan = ''  # нет такого на странице
                else:
                    coll = len(driver.find_elements_by_xpath(
                        '//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]'))  # кол-во эл
                    for i in range(coll):
                        ucan = ucan + \
                               driver.find_elements_by_xpath(
                                   '//*[contains(@class,"a10a3f92e9--item--21VpQ a10a3f92e9")]')[
                                   i - 1].text + '/'  # сборка эл
                # print(ucan)

                items = ''  # итемы квартиры
                try:
                    element_to_hover_over = driver.find_element_by_xpath(
                        '//*[@data-name="Features"]')  # проверка на вшивоть
                except NoSuchElementException:
                    items = ''  # нет такого на странице
                else:
                    coll = len(driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]'))  # кол-во эл
                    for i in range(coll - 1):
                        items = items + driver.find_elements_by_xpath('//*[@data-name="FeatureItem"]')[
                            i].text + '/'  # сборка эл
                # print(items)

                colvo = driver.find_element_by_xpath('//*[@id="photos"]/div[2]/div/div[2]').text  # кол-во фоточек
                x = colvo.split()[0]  # вычленяем из этого инт
                try:
                    x = int(x)  # проверка на вшивоть
                except ValueError:
                    colvo = driver.find_element_by_xpath(
                        '//*[@id="photos"]/div[2]/div[2]/div[2]').text  # тогда фоточки - другой элемент
                    x = int(colvo.split()[0])  # теперь это инт

                for i in range(x):
                    url = driver.find_element_by_xpath("//div[contains(@class, 'fotorama__active')]/img").get_attribute(
                        'src')  # тырим ссылки фоточек

                    element_to_hover_over = driver.find_element_by_xpath(
                        '//*[@id="frontend-offer-card-fotorama"]/div/div[1]/div[1]')  # видим элементы
                    hover = ActionChains(driver).move_to_element(element_to_hover_over)  # наводимся на фоточку
                    hover.perform()  # наводимся снова

                    driver.find_element_by_xpath(
                        '//div[@class="fotorama__arr fotorama__arr--next"]').click()  # видим кнопку переключения на след кнопку
                    fotoochka = fotoochka + url + ' '  # все будет нашим
                    # print(fotoochka)
                    time.sleep(0.2)  # прогрузиться, потом и поговорим

                undergrounds = metro + " " + metrotime

                room = EnterInSystem.Apartments()

                if "Мебель в комнатах" in items:
                    room.furnitRoom = True
                if "Мебель на кухне" in items:
                    room.furnitKitch = True
                if "Холодильник" in items:
                    room.fridge = True
                if "Посудомоечная машина" in items:
                    room.dishwasher = True
                if "Стиральная машина" in items:
                    room.washer = True
                if "Интернет" in items:
                    room.internet = True
                if "Телефон" in items:
                    room.phone = True
                if "Кондиционер" in items:
                    room.conditioner = True
                if "Ванна" in items:
                    room.bath = True
                if "Душевая кабина" in items:
                    room.shower = True

                if "Можно с детьми" in ucan:
                    room.children = True
                if "Можно с животными" in ucan:
                    room.animals = True

                room.undergrounds = undergrounds
                room.address = adress
                room.discription = opisanie
                room.photo = fotoochka

                colcomn = colcomn.split()
                colcomn[1] = colcomn[1][:len(colcomn[1]) - 1]
                room.room = colcomn[0] + colcomn[1]

                room.link = site

                price = price[:price.find("₽/мес.")]
                price = price.split()
                pri = ''
                for i in price:
                    pri = pri + i
                room.price = int(pri)
                obshplo= obshplo.split()[0].replace(',', '.')
                room.area = float(obshplo)
                room.items = items
                room.ucan = ucan
                tegs = items + ' ' + ucan + ' ' + opisanie
                room.tegs = tegs
                db.addRoom(room)
                print(site)
            except:
                pass
            # except OSError as err:
            #      print(err)
