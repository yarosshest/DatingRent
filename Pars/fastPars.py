import requests      # Библиотека для отправки запросов
import numpy as np   # Библиотека для матриц, векторов и линала
import pandas as pd  # Библиотека для табличек
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
def get_data(page_link):
    Agent = UserAgent().chrome
    response = requests.get(page_link, headers={'User-Agent': Agent})

    html = response.content
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    # obj = soup.find('img')
    # print(obj)
    obj = soup.findAll(lambda tag: tag.name == 'img')
    
    print(obj)

get_data("https://www.cian.ru/rent/flat/242000880/")