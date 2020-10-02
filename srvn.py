import sqlite3
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
import pymystem3
nltk.download("stopwords")
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

from itertools import zip_longest
from statistics import mean
import EnterInSystem
import sparse

def summaiz(lst):
    # first create non-jagged numpy array
    leng = lst.shape[1]
    b = -np.ones([lst.shape[0], leng])

    for i, j in enumerate(lst):
        b[i][0:lst.shape[0]] = j

    # count negatives per column (for use later)
    neg_count = [np.sum(b[:, i] == 0) for i in range(b.shape[1])]

    # set negatives to 0
    b[b == 0] = 0

    # calculate means
    means = [np.sum(b[:, i]) / (b.shape[0] - neg_count[i]) \
                 if (b.shape[0] - neg_count[i]) != 0 else 0 \
             for i in range(b.shape[1])]
    return means

# Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")

def preprocess_text(text): # функция от бога, буду молиться на человека, подарившего мне ее
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text

#con = sqlite3.connect("links.db")#код таблицы нашей нужен нам
#df = pd.read_sql("SELECT tegs from Apartments", con)

def getRoom(pice, metro, userId):
    tfidf = TfidfVectorizer(stop_words=None) #составление вектора

    db = EnterInSystem.createBd()

    listScam = []
    for i in db.allRate(userId):
        listScam.append(i.data)

    # overview_matrix_polz = tfidf.fit_transform(np.array(listScam))  # вектора квартир, положительно оцененных пользователем

    vectorpolz = np.mean(np.array(listScam), axis=0)


    #Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
    listScam = []
    for i in db.allNotRate(pice,metro,userId):
        listScam.append(i.data)  # трансформация в кучу векторов эл питонячьего списка

    # overview_matrix = tfidf.fit_transform(np.array(listScam))  # трансформация в кучу векторов эл питонячьего списка
    overview_matrix = np.array(listScam)
    overview_matrix = overview_matrix.squeeze(1)
    similarity_matrix = linear_kernel(overview_matrix,vectorpolz) #МАтрица сходства
    # vectorpolz = summaiz(overview_matrix_polz)#среднее арифметические векторов
    #тут будет задаваться вектор пользователя
    # movie_index = mapping[movie_input]


    # получить значения сходства с другими квартирами
    #similarity_score - это список индекса и матрицы скотства
    similarity_score = list(enumerate(similarity_matrix)) #d вместо индекса будем вводить функцию, отвечающую за вектор пользователя
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True) # сортировать по убыванию показатель сходства кв, введенный со всеми другими кв
    similarity_score = similarity_score[0]# список квартир, не совсем понятно, какойд длины, обсуждение приветствуется
    # movie_indices = [i[0] for i in similarity_score] #вывод куда-нибудь когда-нибудь
    return listScam[similarity_score[0]]
