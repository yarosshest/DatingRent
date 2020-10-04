import sqlite3
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

from itertools import zip_longest
from statistics import mean
import EnterInSystem
import sparse

# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")


def getRoom(pice, metro, userId):
    tfidf = TfidfVectorizer(stop_words=None) #составление вектора

    db = EnterInSystem.createBd()

    listScam = []
    for i in db.allRate(userId):
        listScam.append(i.data)


    vectorpolz = np.mean(np.array(listScam), axis=0)# вектора квартир, положительно оцененных пользователем


    #Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
    listScam = []
    for i in db.allNotRate(pice,metro,userId):
        listScam.append(i.data)  # трансформация в кучу векторов эл питонячьего списка

    overview_matrix = np.array(listScam)
    overview_matrix = overview_matrix.squeeze(1)
    similarity_matrix = linear_kernel(overview_matrix,vectorpolz) #МАтрица сходства



    # получить значения сходства с другими квартирами
    #similarity_score - это список индекса и матрицы скотства
    similarity_score = list(enumerate(similarity_matrix)) #d вместо индекса будем вводить функцию, отвечающую за вектор пользователя
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True) # сортировать по убыванию показатель сходства кв, введенный со всеми другими кв
    similarity_score = similarity_score[0]# список квартир, не совсем понятно, какойд длины, обсуждение приветствуется
    # movie_indices = [i[0] for i in similarity_score] #вывод куда-нибудь когда-нибудь
    return listScam[similarity_score[0]]
