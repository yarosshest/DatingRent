#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
#putting movies data on 'movies' dataframe
movies = pd.read_csv('movies_metadata.csv')


mapping = pd.Series(movies.index,index = movies['title'])
movie_index = mapping[movie_input]
# получить значения сходства с другими фильмами
#similarity_score - это список индекса и матрицы сходства
similarity_score = list(enumerate(similarity_matrix[movie_index]))
# сортировать по убыванию показатель сходства фильма, введенный со всеми другими фильмами
similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
# возвращать названия фильмов с помощью серии сопоставлений
similarity_score = similarity_score[1:15]
#return movie names using the mapping series
movie_indices = [i[0] for i in similarity_score]
