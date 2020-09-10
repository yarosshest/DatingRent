from flask import Flask, request, redirect, url_for, session
# импортируем библиотеку для работы с файловой системой операционной системы
import os
import jinja2
import EnterInSystem

app = Flask(__name__)

# сохраняем в строковую переменную
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# создаем окружение для шаблона
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
app.secret_key = '565009BA357CD1A05165F7E729DE7693'

template = 'registr.html'
params = {'name': 'Josh', 'lastname': 'Scogin'}
t = jinja_env.get_template(template)
t.render(params)
session = {}
session['Login'] = False

# EnterInSystem.DropTable()
db = EnterInSystem.createBd()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session['Login'] and "email" in session:
        email = session['email']
        password = session['password']
        EnterInSystem.LoginUser(db, email, password)
        return redirect(url_for('UserLab'))

    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        replay = EnterInSystem.LoginUser(db, email, password)
        if replay == "Login success":
            session['email'] = email
            session['password'] = password
            session['Login'] = True
            return redirect(url_for('UserLab'))
        if replay == "Wrong login password":
            return render('login.html', err="Неверный логин пароль")
    else:
        if "email" in session:
            email = session['email']
            password = session['password']
            return render('login.html', Email=email, password=password)
        else:
            return render('login.html')


@app.route("/UserLab", methods=['GET', 'POST'])
def UserLab():
    if session['Login']:
        if request.method == 'POST':
            if "exit" in request.form:
                email = session['email']
                EnterInSystem.LogOutUser(db, email)
                session['Login'] = False
                return redirect(url_for('login'))

        return render('UserLab.html')
    else:
        return redirect(url_for('login'))




@app.route('/registr', methods=['GET', 'POST'])
def registr():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']
        EnterInSystem.RegisterUser(db, email, password)
        if EnterInSystem.RegisterUser(db, email, password) == "Register success":
            session['Register'] = True
            session['email'] = email
            session['password'] = password
            return redirect(url_for('login'))
        else:
            return render('registr.html', err="Такой email уже есть")
    else:
        return render('registr.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))


def render(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


if __name__ == '__main__':
    app.run(debug=True, )
