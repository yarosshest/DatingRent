import datetime
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, DateTime, func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.dialects.sqlite import DATETIME

engine = create_engine('sqlite:///some.db', echo=False)
Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)

    def __init__(self, Login, Password):
        self.Login = Login
        self.Password = Password


class Sessions(Base):
    __tablename__ = 'Sessions'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)
    Users_id = Column(Integer, ForeignKey('Users.id'))
    Users = relationship(
        Users,
        backref=backref('Sessions',
                        uselist=True,
                        cascade='delete,all'))

    def __repr__(self):
        return "%s to %s" % (self.start_time, self.finish_time)


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


class Apartments(Base):
    __tablename__ = 'Apartments'
    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    address = Column(String)
    undergrounds = Column(String)
    discription = Column(String)
    photo = Column(String)
    room = Column(String)
    area = Column(String)
    link = Column(String)

    def __init__(self, price, address, undergrounds, discription, photo, room, area, link):
        self.price = price
        self.address = address
        self.undergrounds = undergrounds
        self.discription = discription
        self.photo = photo
        self.room = room
        self.area = area
        self.link = link

class Links(Base):
    __tablename__ = 'Apartments'
    id = Column(Integer, primary_key=True)
    link = Column(String)

    def __init__(self, link):
        self.link = link



class DatabaseFuction(object):
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def Insert(self, Log, Pass):
        NewUser = Users(Log, Pass)
        session = self.Session()
        session.add(NewUser)
        session.commit()
        session.close()

    def Drop(self):
        session = self.Session()
        session.query.delete()
        session.close()

    def LogOut(self, Log):
        session = self.Session()
        for instance in session.query(Sessions.start_time, Sessions.finish_time, Sessions.id):
            if (None == instance.finish_time):
                SesionUser = session.query(Sessions).filter_by(id=instance.id).first()
                SesionUser.finish_time = datetime.now()
                session.add(SesionUser)
                session.commit()
        session.close()

    def Login(self, Log, Pass):
        Exist = False
        data = datetime.now()
        session = self.Session()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if ((instance.Login == Log) and (instance.Password == Pass)):
                SesionUser = Sessions(start_time=datetime.now(), finish_time=None,
                                      Users=session.query(Users).filter_by(id=instance.id).first())
                session.add(SesionUser)
                session.commit()
                Exist = True
        session.close()
        return Exist

    def Register(self, Log, Pass):
        session = self.Session()
        Exist = False
        for instance in session.query(Users.Login):
            if (instance.Login == Log):
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
        session.close()

    def RoomForId(self, id):
        session = self.Session()
        ab = session.query(Apartments).filter_by(id=id).first()
        l = [ab.price, ab.address, ab.undergrounds, ab.discription, ab.photo, ab.room, ab.area, ab.id]
        session.close()
        return l

    def Rate(self, idU, idA, rateScore):
        session = self.Session()
        rate = Rates(idU, idA, rateScore)
        session.add(rate)
        session.commit()
        session.close()

    def UserId(self, Log):
        session = self.Session()
        for instance in session.query(Users.Login, Users.Password, Users.id):
            if (instance.Login == Log):
                id = instance.id
        session.close()
        return id

    def addRoom(self, price, address, undergrounds, discription, photo, room, area, link):
        session = self.Session()

        NewRoom = Apartments(price, address, undergrounds, discription, photo, room, area, link)

        session.add(NewRoom)
        session.commit()
        session.close()


    def addLink(self, link):
        session = self.Session()

        NewLink = Links(link)

        session.add(NewLink)
        session.commit()
        session.close()

    def getAllLinks(self):
        session = self.Session()
        l =[]
        for instance in session.query(Links.link):
            l.append(instance.link)

        session.close()
        return l



def LogOutUser(DBase, login):
    DBase.LogOut(login)
    return True


def getUserId(DBase, login):
    return DBase.UserId(login)


def LoginUser(DBase, login, password):
    result = DBase.Login(login, password)
    if result:
        return "Login success"
    else:
        return "Wrong login password"


def RegisterUser(DBase, login, password):
    result = DBase.Register(login, password)
    if result:
        return "Register success"
    else:
        return "User already exists"


def GetRoomForId(DBase, id):
    return DBase.RoomForId(id)


def FullDB(DBase, login, password):
    DBase.Insert(login, password)


def createRoom(DBase, price, address, undergrounds, discription, photo, room, area, link):
    DBase.addRoom(price, address, undergrounds, discription, photo, room, area, link)


def createBd():
    Base.metadata.create_all(engine)
    DBase = DatabaseFuction()
    return DBase


def rateRoom(DBase, idU, idA, rate):
    DBase.Rate(idU, idA, rate)


def DropTable():
    Users.__table__.drop(engine)
    Sessions.__table__.drop(engine)
