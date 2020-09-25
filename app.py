from flask import Flask, request, redirect, url_for, session, render_template
import os
import jinja2
import EnterInSystem

# инициализация веб приложения
app = Flask(__name__, static_url_path="/static")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
app.secret_key = '565009BA357CD1A05165F7E729DE7693'


def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# создание соединения с БД
db = EnterInSystem.createBd()

# Старт приложения
if __name__ == '__main__':
    #app.run(debug=False,host='0.0.0.0')
    app.run(debug=True)


# Получение страницы логина
@app.route('/login', methods=['GET'])
def login_Get():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            email = session['email']
            password = session['password']
            EnterInSystem.LoginUser(db, email, password)
            return redirect(url_for('Filtr'))
        else:
            return render('login.html')
    else:
        return render('login.html')


# Собственно логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form['Email']
    password = request.form['password']
    replay = EnterInSystem.LoginUser(db, email, password)
    if replay == "Login success":
        session['email'] = email
        session['password'] = password
        session['Login'] = True
        session['userId'] = db.UserId(email)
        # Костыль для удаления
        session['scam'] = 0
        # Костыль для удаления
        return redirect(url_for('Filtr'))
    if replay == "Wrong login password":
        return render('login.html', err="Неверный логин пароль")


# Получение главной страницы приложения
@app.route("/UserLab", methods=['GET'])
def UserLab_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            # затычка пока нет алгоритма
            Ap = db.RoomForId(1)
            session['roomID'] =1
            price = Ap.price
            undergrounds = Ap.undergrounds
            discription = Ap.discription
            photo = Ap.photo
            room = Ap.room
            area = Ap.area
            address = Ap.address
            price = Ap.price
            ucan = Ap.ucan
            items = Ap.items.split('/')
            del items[len(items) - 1]
            l = photo.split()
            photo1 = l[0]
            del l[0]
            return render_template('UserLab.html', price=price, address=address, undergrounds=undergrounds, discription=discription,
                                   photo1=photo1, photoAr=l, room=room, area=area, items=items, ucan=ucan)
            # затычка пока нет алгоритма
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))


# Главная страница приложения
@app.route("/UserLab", methods=['POST'])
def UserLab():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if 'exit' in request.form:  # выход из сессии
                session['email'] = None
                session['password'] = None
                session['Login'] = False
                return redirect(url_for('login'))

            if 'filter' in request.form:  # изминение фильтра
                return redirect(url_for('Filtr'))

            if "search" in request.form:  # поиск
                # затычка пока нет алгоритма
                db.Rate(session['userId'], session['roomID'], int(request.form['inlineRadioOptions']))
                Ap = db.RoomForId(1+session['scam'])
                session['roomID'] = 1 + session['scam']
                price = Ap.price
                undergrounds = Ap.undergrounds
                discription = Ap.discription
                room = Ap.room
                photo = Ap.photo
                area = Ap.area
                address = Ap.address
                ucan = Ap.ucan.split('/')
                del ucan[len(ucan) - 1]
                items = Ap.items.split('/')
                del items[len(items)-1]
                l = photo.split()
                photo1 = l[0]
                del l[0]
                session['scam'] =session['scam']+1
                return render_template('UserLab.html', price=price, address=address, undergrounds=undergrounds,
                              discription=discription, photo1=photo1, photoAr=l, room=room, area=area, items=items, ucan=ucan)
                # затычка пока нет алгоритма
        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


# Получение фильтра
@app.route("/Filtr", methods=['GET'])
def Filtr_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            return render('Filtr.html')
        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


# Фильтр
@app.route("/Filtr", methods=['POST'])
def Filtr():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            # получение фильтров
            if 'MaxAmount' in request.form:
                session['MaxAmount'] = request.form['MaxAmount']
            if 'KolRoom' in request.form:
                session['KolRoom'] = request.form['KolRoom']
            if 'Metro' in request.form:
                session['Metro'] = request.form['Metro']
            return redirect(url_for('UserLab'))
        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


# Получение страницы регистрации
@app.route('/registr', methods=['GET'])
def registr_Get():
    return render('registr.html')


# Регистрация
@app.route('/registr', methods=['GET', 'POST'])
def registr():
    email = request.form['Email']
    password = request.form['password']
    res = EnterInSystem.RegisterUser(db, email, password)
    if res == "Register success":
        session['Register'] = True
        session['email'] = email
        session['password'] = password
        return redirect(url_for('login'))
    else:
        return render('registr.html', err="Такой email уже есть")


# Нулевая страница
@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))

def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
