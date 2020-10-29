import numpy as np
from sklearn.metrics.pairwise import linear_kernel
import EnterInSystem


def getRoom(pice, metro, userId, ren):
    db = EnterInSystem.createBd()

    listScam = []
    for i in db.allRate(userId):
        listScam.append(np.array(i.data))

    vectorpolz = np.mean(listScam, axis=0)  # вектора квартир, положительно оцененных пользователем

    # Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
    listAp = []
    for i in db.allNotRate(pice, metro, userId, ren):
        listAp.append([i.id, i.vector.data])  # трансформация в кучу векторов эл питонячьего списка

    for i in listAp:
        i[1] = float(linear_kernel(i[1], vectorpolz))

    listAp = sorted(listAp, key=lambda listAp: listAp[1], reverse=True)
    id = listAp[0][0]

    return id
