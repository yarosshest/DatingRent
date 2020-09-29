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

def summaiz(lst):
    return [mean(x for x in t if x != 0) for t in zip_longest(*lst, fillvalue=0)]
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


tfidf = TfidfVectorizer(stop_words=None) #составление вектора

#Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
overview_matrix = tfidf.fit_transform(preprocess_text('список ярика')) #трансформация в кучу векторов эл питонячьего списка

similarity_matrix = linear_kernel(overview_matrix,overview_matrix) #МАтрица сходства

overview_matrix_polz = tfidf.fit_transform(preprocess_text('список пользователя')) #вектора квартир, положительно оцененных пользователем
vectorpolz = summaiz(overview_matrix_polz)#среднее арифметические векторов
#тут будет задаваться вектор пользователя
# movie_index = mapping[movie_input]


# получить значения сходства с другими квартирами
#similarity_score - это список индекса и матрицы скотства
similarity_score = list(enumerate(vectorpolz)) #d вместо индекса будем вводить функцию, отвечающую за вектор пользователя
similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True) # сортировать по убыванию показатель сходства кв, введенный со всеми другими кв
similarity_score = similarity_score[1:15] # список квартир, не совсем понятно, какойд длины, обсуждение приветствуется
movie_indices = [i[0] for i in similarity_score] #вывод куда-нибудь когда-нибудь
