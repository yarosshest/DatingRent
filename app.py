from flask import Flask, request, redirect, url_for, session, render_template, send_from_directory
import os
import jinja2
import EnterInSystem

# инициализация веб приложения
application = Flask(__name__)
application.config.update({
    'SQLALCHEMY_POOL_SIZE': None,
    'SQLALCHEMY_POOL_TIMEOUT': None
})

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
application.secret_key = '565009BA357CD1A05165F7E729DE7693'


def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# создание соединения с БД
db = EnterInSystem.createBd()

# Старт приложения
if __name__ == '__main__':
    application.run(host='0.0.0.0')


@application.route('/service-worker.js', methods=['GET'])
def sw():
    return application.send_static_file('service-worker.js')


@application.route('/offline', methods=['GET'])
def offline():
    return application.send_static_file('offline.html')


@application.route('/app', methods=['GET'])
def app():
    return application.send_static_file('js/app.js')


@application.route('/img', methods=['GET'])
def img():
    return application.send_static_file('images/icon-192x192.png')


# Получение страницы логина
@application.route('/login', methods=['GET'])
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
@application.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('office_GET'))
    if replay == "Wrong login password":
        return render('login.html', err="Неверный логин пароль")


@application.route("/relike", methods=['GET'])
def relike_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if "viev" in session:
                Ap = db.RoomForId(session["viev"])
                session['roomID'] = Ap.id
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
                del items[len(items) - 1]
                l = photo.split()
                photo1 = l[0]
                del l[0]
                return render_template('vievRoom.html', price=price, address=address, undergrounds=undergrounds,
                                       discription=discription, photo1=photo1, photoAr=l, room=room, area=area,
                                       items=items, ucan=ucan)
        else:
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@application.route("/relike", methods=['POST'])
def relike_POST():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if "rate" in request.form:
                db.re_rate(session['userId'], session['roomID'], bool(int(request.form["rate"])))
                if session["typeViev"]:
                    return redirect(url_for("LK_GET"))
                else:
                    return redirect(url_for("DL_GET"))

            if "exit" in request.form:
                if request.form["exit"] == "exit":
                    if session["typeViev"]:
                        return redirect(url_for("LK_GET"))
                    else:
                        return redirect(url_for("DL_GET"))

                if request.form["exit"] == "UserOffice":
                    return redirect(url_for("office_GET"))
        else:
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


# Получение главной страницы приложения
@application.route("/UserLab", methods=['GET'])
def UserLab_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            Ap = EnterInSystem.getRec(db, session["MaxAmount"], session["Metro"], session['userId'],
                                      session['ren'])
            if Ap == "Все квартиры с данными характеристиками оценены":
                session['eer'] = "Все квартиры с данными характеристиками оценены"
                return redirect(url_for('Filtr'))

            if Ap is not None:
                if "eer" in session:
                    del session["eer"]
                # затычка пока нет алгоритма
                session['roomID'] = Ap.id
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
                del items[len(items) - 1]
                l = photo.split()
                photo1 = l[0]
                del l[0]
                return render_template('UserLab.html', price=price, address=address, undergrounds=undergrounds,
                                       discription=discription,photo1=photo1, photoAr=l, room=room, area=area,
                                       items=items, ucan=ucan)
            # затычка пока нет алгоритма
            else:
                session["eer"] = "Квартир по вашим параметрам  не найдено"
                return redirect(url_for('Filtr'))
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))


# Главная страница приложения
@application.route("/UserLab", methods=['POST'])
def UserLab():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if 'exit' in request.form:
                if request.form["exit"] == "exit":# выход из сессии
                    session['email'] = None
                    session['password'] = None
                    session['Login'] = False
                    return redirect(url_for('login'))

                if request.form["exit"] == "UserOffice":
                    return redirect(url_for('office_GET'))

            if 'filter' in request.form:  # изминение фильтра
                return redirect(url_for('Filtr'))

            if "rate" in request.form:  # поиск
                db.Rate(session['userId'], session['roomID'], bool(int(request.form['rate'])))
                return redirect(url_for('UserLab_GET'))

        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


@application.route("/LK", methods=['GET'])
def LK_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            like = db.allAplike(session['userId'])
            return render('LK.html', like=like)
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))


@application.route("/LK", methods=['POST'])
def LK_POST():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if "rate" in request.form:
                session["viev"] = request.form["rate"]
                session["typeViev"] = True
                return redirect(url_for('relike_GET'))

            if "end" in request.form:
                if request.form["end"] == "1":
                    return redirect(url_for('office_GET'))


            return redirect(url_for('LK_GET'))
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))

@application.route("/DL", methods=['GET'])
def DL_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            dislike = db.allApDislike(session['userId'])
            return render('DL.html', dislike=dislike)
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))

@application.route("/DL", methods=['POST'])
def DL_POST():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if "rate" in request.form:
                session["viev"] = request.form["rate"]
                session["typeViev"] = False
                return redirect(url_for('relike_GET'))

            if "end" in request.form:
                if request.form['end'] == '1':
                    return redirect(url_for('office_GET'))

            return redirect(url_for('DL_GET'))
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))


@application.route("/office", methods=['GET'])
def office_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            return render('office.html')
        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))


@application.route("/office", methods=['POST'])
def office_POST():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if "end" in request.form:
                if request.form['end'] == "like":
                    return redirect(url_for('LK_GET'))

                if request.form['end'] == 'Dislike':
                    return redirect(url_for('DL_GET'))

                if request.form['end'] == "Search":
                    return redirect(url_for('Filtr_GET'))

                if request.form['end'] == "exit":
                    session.clear()
                    return redirect(url_for('login'))

            return render('office.html')

        else:
            return render('login.html')

    else:
        return redirect(url_for('login'))



# Получение фильтра
@application.route("/Filtr", methods=['GET'])
def Filtr_GET():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            if 'eer' in session:
                err = session['eer']
                return render('Filtr.html', error=err)
            else:
                return render('Filtr.html')
        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


# Фильтр
@application.route("/Filtr", methods=['POST'])
def Filtr():
    if 'Login' in session:  # проверка на залогиненость
        if session['Login']:
            # получение фильтров
            if 'MaxAmount' in request.form:
                session['MaxAmount'] = request.form['MaxAmount']
            if 'Metro' in request.form:
                session['Metro'] = request.form['Metro']

            session['ren'] = False
            if 'ren' in request.form:
                session['ren'] = True

            return redirect(url_for('UserLab'))
        else:
            return render('login.html')
    else:
        return redirect(url_for('login'))


# Получение страницы регистрации
@application.route('/registr', methods=['GET'])
def registr_Get():
    return render('registr.html')


# Регистрация
@application.route('/registr', methods=['GET', 'POST'])
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
@application.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))


def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
