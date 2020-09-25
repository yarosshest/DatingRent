from scipy.sparse import lil_matrix
from sklearn.preprocessing import normalize
from scipy.sparse import spdiags
from scipy.sparse import vstack
import numpy as np
import EnterInSystem

db = EnterInSystem.createBd()
Rate = db.getAllRate()

# строим индекс user_id -> col_id, где col_id - идентификатор столбца в матрице
user_to_col = {}
for user in Rate:
    user_to_col[user.Users_id] = user.Users_id

# строим индекс obj_id -> row_id, где row_id - идентификатор строки в матрице
obj_to_row = {}
for Apart in Rate:
    obj_to_row[Apart.Apartments_id] = Apart.Apartments_id


# создаем матрицу нужных размеров
matrix = lil_matrix((len(obj_to_row), len(user_to_col)))

# заполняем матрицу
for rate in Rate:
    row_id = obj_to_row.get(rate.Apartments_id)
    col_id = user_to_col.get(rate.Users_id)
    if row_id is not None and col_id is not None:
        matrix[row_id, col_id] = min(rate.rate, 5)

# косинусная мера вычисляется как отношение скалярного произведения векторов(числитель)
# к произведению длины векторов(знаменатель)

# нормализуем исходную матрицу
# (данное действие соответствует приведению знаменателя в формуле косинусной меры к 1)
normalized_matrix = normalize(matrix.tocsr()).tocsr()
# вычисляем скалярное произведение
cosine_sim_matrix = normalized_matrix.dot(normalized_matrix.T)

# обнуляем диагональ, чтобы исключить ее из рекомендаций
# быстрое обнуление диагонали
diag = spdiags(-cosine_sim_matrix.diagonal(), [0], *cosine_sim_matrix.shape, format='csr')
cosine_sim_matrix = cosine_sim_matrix + diag

cosine_sim_matrix = cosine_sim_matrix.tocsr()
m = 30

# построим top-m матрицу в один поток
rows = []
for row_id in np.unique(cosine_sim_matrix.nonzero()[0]):
    row = cosine_sim_matrix[row_id]  # исходная строка матрицы
    if row.nnz > m:
        work_row = row.tolil()
        # заменяем все top-m элементов на 0, результат отнимаем от row
        # при большом количестве столбцов данная операция работает быстрее,
        # чем простое зануление всех элементов кроме top-m
        work_row[0, row.nonzero()[1][np.argsort(row.data)[-m:]]] = 0
        row = row - work_row.tocsr()
    rows.append(row)
topk_matrix = vstack(rows)
# нормализуем матрицу-результат
topk_matrix = normalize(topk_matrix)


# индекс для преобразования row_id -> obj_id, где row_id - идентификатор строки в матрице
row_to_obj = {row_id: obj_id for obj_id, row_id in obj_to_row.iteritems()}

#подготавливаем вектор рейтингов пользователя:
user_vector = lil_matrix((len(obj_to_row), 1))
user_vector = user_vector.tocsr()

# 1. перемножить матрицу item-item и вектор рейтингов пользователя A
x = topk_matrix.dot(user_vector).tolil()
# 2. занулить ячейки, соответствующие фильмам, которые пользователь A уже оценил
for i, j in zip(*user_vector.nonzero()):
    x[i, j] = 0

# превращаем столбец результата в вектор
x = x.T.tocsr()

# 3. отсортировать фильмы в порядке убывания значений и получить top-k рекомендаций (quorum = 10)
quorum = 10
data_ids = np.argsort(x.data)[-quorum:][::-1]

result = []
for arg_id in data_ids:
    row_id, p = x.indices[arg_id], x.data[arg_id]
    result.append({"obj_id": row_to_obj[row_id], "weight": p})

