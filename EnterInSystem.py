import datetime
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query
from sqlalchemy.sql import select
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy import func


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
    rate = Column(Integer)

    def __init__(self, idU, idA, rate):
        self.Users_id = idU
        self.Apartments_id = idA
        self.rate = rate


# Таблица апартаментов
class Apartments(Base):
    __tablename__ = 'Apartments'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    address = Column(String)
    undergrounds = Column(String)
    discription = Column(String)
    photo = Column(String)
    room = Column(String)
    area = Column(String)
    link = Column(String)
    items = Column(String)
    ucan = Column(String)


# Таблица ссылок
class Links(Base):
    __tablename__ = 'Links'
    id = Column(Integer, primary_key=True)
    link = Column(String)

    def __init__(self, link):
        self.link = link


# Логика работы с БД
class DatabaseFuction(object):
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    # Вход в сиситему пользователя
    def Login(self, Log, Pass):
        Exist = False
        session = self.Session()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if (instance.Login == Log) and (instance.Password == Pass):
                Exist = True
        session.close()
        return Exist

    # Регистрация ползователя
    def Register(self, Log, Pass):
        session = self.Session()
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
        session = self.Session()
        ab = Apartments()
        ab = session.query(Apartments).filter(Apartments.id == id).first()
        session.close()
        return ab

    # Оценка квартиры
    def Rate(self, idU, idA, rateScore):
        session = self.Session()
        rate = Rates(idU, idA, rateScore)
        session.add(rate)
        session.commit()
        session.close()

    # Получение id пользователя
    def UserId(self, Log):
        session = self.Session()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if (instance.Login == Log):
                id = instance.id
        session.close()
        return id

    # добавление квартиры
    def addRoomList(self, price, address, undergrounds, discription, photo, room, area, link):
        session = self.Session()
        NewRoom = Apartments(price, address, undergrounds, discription, photo, room, area, link)

        session.add(NewRoom)
        session.commit()
        session.close()

    def addRoom(self, room):
        session = self.Session()
        session.add(room)
        session.commit()
        session.close()

    # Добавление ссылки в таблицу
    def addLink(self, link):
        session = self.Session()

        NewLink = Links(link)

        session.add(NewLink)
        session.commit()
        session.close()

    # Получение всех ссылок
    def getAllLinks(self):
        session = self.Session()
        l =[]
        for instance in session.query(Links.link):
            l.append(instance.link)

        session.close()
        return l

    # Проверка дублирования ссылки
    def linkChek(self,link):
        session = self.Session()
        r = session.query(Links).filter(Links.link == link)
        if r.count() >= 1:
            session.close()
            return False
        else:
            session.close()
            return True

    # Проверка дублирования квартиры
    def RoomChek(self,link):
        session = self.Session()
        r = session.query(Apartments).filter(Apartments.link == link)
        A = r.count()
        if A >= 1:
            session.close()
            return False
        else:
            session.close()
            return True


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
