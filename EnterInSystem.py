from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sqlalchemy import create_engine, DateTime, func, Boolean, Float, PickleType
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query
import srvn
import random

# расположение БД
engine = create_engine('sqlite:///links.db', echo=False)
Base = declarative_base()
meta = MetaData()


# Таблица пользователей
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)

    def __init__(self, Login, Password):
        self.Login = Login
        self.Password = Password


# Таблица рейтингов
class Rates(Base):
    __tablename__ = 'Rates'
    id = Column(Integer, primary_key=True)
    Users_id = Column(Integer, ForeignKey('Users.id'))
    Apartments_id = Column(Integer, ForeignKey('Apartments.id'))
    rate = Column(Boolean)

    def __init__(self, idU, idA, rate):
        self.Users_id = idU
        self.Apartments_id = idA
        self.rate = rate


# Таблица апартаментов
class Apartments(Base):
    __tablename__ = 'Apartments'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    address = Column(String)
    undergrounds = Column(String)
    discription = Column(String)
    photo = Column(String)
    room = Column(String)
    area = Column(Float)
    link = Column(String)
    ren = Column(Boolean)
    furnitRoom = Column(Boolean, default=False)
    furnitKitch = Column(Boolean, default=False)
    fridge = Column(Boolean, default=False)
    dishwasher = Column(Boolean, default=False)
    washer = Column(Boolean, default=False)
    children = Column(Boolean, default=False)
    animals = Column(Boolean, default=False)
    internet = Column(Boolean, default=False)
    phone = Column(Boolean, default=False)
    conditioner = Column(Boolean, default=False)
    bath = Column(Boolean, default=False)
    shower = Column(Boolean, default=False)
    items = Column(String)
    ucan = Column(String)
    tegs = Column(String)
    tegLem = Column(String)
    vector = Column(PickleType)


# Таблица ссылок
class Links(Base):
    __tablename__ = 'Links'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    err = Column(Boolean)

    def __init__(self, link):
        self.link = link


# Логика работы с БД
class DatabaseFuction(object):
    # Вход в сиситему пользователя
    def Login(self, Log, Pass):
        Exist = False
        session = sessionmaker(bind=engine)()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if (instance.Login == Log) and (instance.Password == Pass):
                Exist = True
        session.close()
        return Exist

    # Регистрация ползователя
    def Register(self, Log, Pass):
        session = sessionmaker(bind=engine)()
        Exist = False
        for instance in session.query(Users.Login):
            if instance.Login == Log:
                Exist = True

        if Exist:
            session.close()
            return False
        else:
            NewUser = Users(Log, Pass)
            session.add(NewUser)
            session.commit()
            session.close()
            return True

    # Квартира по id
    def RoomForId(self, id):
        session = sessionmaker(bind=engine)()
        ab = Apartments()
        ab = session.query(Apartments).filter(Apartments.id == id).first()
        session.close()
        return ab

    # Оценка квартиры
    def Rate(self, idU, idA, rateScore):
        session = sessionmaker(bind=engine)()
        rate = Rates(idU, idA, rateScore)
        session.add(rate)
        session.commit()
        session.close()

    def re_rate(self, idU, idA, rateScore):
        session = sessionmaker(bind=engine)()
        rate = session.query(Rates).filter(Rates.Users_id == idU, Rates.Apartments_id == idA).first()
        rate.rate = rateScore
        session.add(rate)
        session.commit()
        session.close()

    # Получение id пользователя
    def UserId(self, Log):
        session = sessionmaker(bind=engine)()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if (instance.Login == Log):
                id = instance.id
        session.close()
        return id

    def dbUpd(self):
        session = sessionmaker(bind=engine)()
        for instance in session.query(Apartments):
            instance.tegs = instance.items + instance.ucan + instance.discription
            session.commit()
        session.close()

    # добавление квартиры
    def addRoomList(self, price, address, undergrounds, discription, photo, room, area, link):
        session = sessionmaker(bind=engine)()
        NewRoom = Apartments(price, address, undergrounds, discription, photo, room, area, link)

        session.add(NewRoom)
        session.commit()
        session.close()

    def addRoom(self, room):
        session = sessionmaker(bind=engine)()
        session.add(room)
        session.commit()
        session.close()

    # Добавление ссылки в таблицу
    def addLink(self, link):
        session = sessionmaker(bind=engine)()

        NewLink = Links(link)

        session.add(NewLink)
        session.commit()
        session.close()

    # Получение всех ссылок
    def getAllLinks(self):
        session = sessionmaker(bind=engine)()
        l = []
        for instance in session.query(Links.link):
            l.append(instance.link)

        session.close()
        return l

    # Получение всех пользователей
    def getAllRate(self):
        session = sessionmaker(bind=engine)()
        l = []
        for instance in session.query(Rates):
            l.append(instance)

        session.close()
        return l

    # Проверка дублирования ссылки
    def linkChek(self, link):
        session = sessionmaker(bind=engine)()
        r = session.query(Links).filter(Links.link == link)
        if r.count() >= 1:
            session.close()
            session.close()
            return False
        else:
            session.close()
            return True

        # Проверка дублирования ссылки

    def del_double_link(self):
        session = sessionmaker(bind=engine)()
        lst = session.query(Links).all()
        dct = []
        for i in lst:
            if i.link in dct:
                session.delete(i)
                print(i.id)
                session.commit()
            else:
                dct.append(i.link)
        session.close()

    # Проверка дублирования квартиры
    def RoomChek(self, link):
        session = sessionmaker(bind=engine)()
        r = session.query(Apartments).filter(Apartments.link == link)
        err = session.query(Links.err).filter(Links.link == link).first()

        if r.count() >= 1 or err == False:
            session.close()
            return False
        else:
            session.close()
            return True

    def add_par_err(self, link):
        session = sessionmaker(bind=engine)()
        r = session.query(Links).filter(Links.link == link).first()
        r.err = True
        session.commit()

    def allNotRate(self, pice, metro, userId, ren):
        session = sessionmaker(bind=engine)()
        response = []
        list = session.query(Apartments).filter(Apartments.price <= pice,
                                                Apartments.undergrounds.ilike("%" + metro + "%"),
                                                Apartments.ren == ren).all()
        rate = []
        rated = session.query(Rates.Apartments_id).filter(Rates.Users_id == userId).all()
        for ap in rated:
            rate.append(ap[0])
        for ap in list:
            if ap.id in rate:
                pass
            else:
                if ap.id == 1745:
                    print("AAAAA")
                response.append(ap)
        session.close()
        return response

    def allRate(self, userId):
        session = sessionmaker(bind=engine)()
        response = []
        list = session.query(Apartments).all()
        rate = []
        rated = session.query(Rates.Apartments_id).filter(Rates.Users_id == userId, Rates.rate == 1).all()
        for ap in rated:
            rate.append(ap[0])
        for ap in list:
            if ap.id in rate:
                response.append(ap.vector)
        session.close()
        return response

    def allApDislike(self, userId):
        session = sessionmaker(bind=engine)()
        response = []
        list = session.query(Apartments).all()
        rate = []
        rated = session.query(Rates.Apartments_id).filter(Rates.Users_id == userId, Rates.rate == 0).all()
        for ap in rated:
            rate.append(ap[0])
        for ap in list:
            if ap.id in rate:
                response.append(ap)
        session.close()
        return response

    def allAplike(self, userId):
        session = sessionmaker(bind=engine)()
        response = []
        list = session.query(Apartments).all()
        rate = []
        rated = session.query(Rates.Apartments_id).filter(Rates.Users_id == userId, Rates.rate == 1).all()
        for ap in rated:
            rate.append(ap[0])
        for ap in list:
            if ap.id in rate:
                response.append(ap)
        session.close()
        return response

    def getForVector(self, vector):
        session = sessionmaker(bind=engine)()
        list = session.query(Apartments).all()

        for i in list:
            c = (i.vector == vector)
            if c.all():
                responce = i
        session.close()
        return responce

    def PushLemon(self, apId, lem):
        session = sessionmaker(bind=engine)()
        list = session.query(Apartments).filter(Apartments.id == apId)
        ap = list.first()
        ap.tegLem = lem
        session.commit()
        session.close()

    def pull_ap_lem(self):
        session = sessionmaker(bind=engine)()
        list = session.query(Apartments).all()
        reply = []
        for ap in list:
            if ap.tegs != '' and ap.tegLem == None:
                reply.append([ap.id, ap.tegs])
            pass
        session.close()
        return reply

    def vectorize(self):
        session = sessionmaker(bind=engine)()
        tfidf = TfidfVectorizer(stop_words=None)
        list = session.query(Apartments).all()
        all = []
        for i in list:
            all.append(i.tegLem)
        overview_matrix = tfidf.fit_transform(np.array(all))
        for i, j in zip(overview_matrix, list):
            j.vector = i.toarray()
            session.commit()
        session.close()

    def getVector(self, id):
        session = sessionmaker(bind=engine)()
        ap = session.query(Apartments.vector).filter(Apartments.id == id)
        ap = ap.first()
        session.close()
        return ap

    def dellLink(self, link):
        session = sessionmaker(bind=engine)()
        lin = session.query(Links).filter(Links.link == link)
        lin = lin.first()
        session.delete(lin)
        session.commit()
        session.close()

    def colRate(self, userId):
        session = sessionmaker(bind=engine)()
        rated = session.query(Rates).filter(Rates.Users_id == userId, Rates.rate == 1)
        session.close()
        return rated.count()

    def randFiltAp(self, pice, metro, ren):
        session = sessionmaker(bind=engine)()
        list = session.query(Apartments).filter(Apartments.price <= pice,
                                                Apartments.undergrounds.ilike("%" + metro + "%"),
                                                Apartments.ren == ren).all()
        session.close()
        return random.choice(list)

    def colFilt(self, pice, metro, ren):
        session = sessionmaker(bind=engine)()
        lst = session.query(Apartments).filter(Apartments.price <= pice,
                                                Apartments.undergrounds.ilike("%" + metro + "%"),
                                                Apartments.ren == ren).all()
        session.close()
        return len(lst)

    def pull_ap_ren(self):
        session = sessionmaker(bind=engine)()
        lst = session.query(Apartments).all()
        reply = []
        for ap in lst:
            if ap.ren is None:
                reply.append([ap.id, ap.photo])
        session.close()
        return reply

    def push_ren(self, ap_id, ren):
        session = sessionmaker(bind=engine)()
        lst = session.query(Apartments).filter(Apartments.id == ap_id)
        ap = lst.first()
        ap.ren = ren
        session.commit()
        session.close()

    def get_col_not_rate(self, pice, metro, userId, ren):
        session = sessionmaker(bind=engine)()
        lst_flit = session.query(Apartments).filter(Apartments.price <= pice,
                                                    Apartments.undergrounds.ilike("%" + metro + "%"),
                                                    Apartments.ren == ren).all()
        list_rate = session.query(Rates.Apartments_id).filter(Rates.Users_id == userId).all()
        response = 0
        for ap in lst_flit:
            if not (ap.id in list_rate):
                response += 1

        session.close()
        return response


def getRec(DBase, pice, metro, userId, ren):
    if DBase.colFilt(pice, metro, ren) > 0:
        if DBase.colRate(userId) > 0:
            responce = DBase.RoomForId(srvn.getRoom(pice, metro, userId, ren))
        else:
            responce = DBase.randFiltAp(pice, metro, ren)
    else:
        responce = None
    return responce


# Вход в сиситему пользователя
def LoginUser(DBase, login, password):
    result = DBase.Login(login, password)
    if result:
        return "Login success"
    else:
        return "Wrong login password"


# Регистрация ползователя
def RegisterUser(DBase, login, password):
    result = DBase.Register(login, password)
    if result:
        return "Register success"
    else:
        return "User already exists"


# Создание обьекта для работы с БД
def createBd():
    Base.metadata.create_all(engine)
    return DatabaseFuction()


if __name__ == '__main__':
    db = createBd()
    # db.vectorize()
    db.del_double_link()
