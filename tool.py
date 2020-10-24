from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from threading import Thread
import EnterInSystem

mystem = Mystem()
russian_stopwords = stopwords.words("russian")


def preprocess_text(text): # функция от бога, буду молиться на человека, подарившего мне ее
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    text = " ".join(tokens)

    return text


class lemTread (Thread):
    def __init__(self,db, apId, tegs):
        Thread.__init__(self)
        self.db = db
        self.Ap = apId
        self.tegs = tegs

    def run(self):
        lem = preprocess_text(self.tegs)
        self.db.PushLemon(self.Ap, lem)


if __name__ == '__main__':
    db = EnterInSystem.createBd()
    list = db.PullLemon()
    treds = []
    for ap in list:
        treds.append(lemTread(db, ap[0], ap[1]))

    for t in treds:
        t.start()

    for t in treds:
        t.join()

    print("lem done")