
import datetime
import os
import re
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import requests
from schemas import UserRegister

BASE_FOLDER = os.path.dirname(__file__)


app = Flask(__name__,
            static_folder=os.path.join(BASE_FOLDER, "static"),
            template_folder=os.path.join(BASE_FOLDER, "templates"))
app.config['SECRET_KEY'] = "my secret key - ds;ldks;ldks;ldks"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:120613@localhost:5432/fl_users"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.db"


db = SQLAlchemy(app)

WeatherID = "af9a1c40b40d720ee1e352270cfc4e85"
cl_num = 0




class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False)
    login = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'User {self.username}'


with app.app_context():
        db.create_all()

    
def add_user(username, login, email, password, age):
    with app.app_context():
        new_user = User(username1=username, login=login, email=email, password=password, age=age)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {username} added successfully!")


def remove_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"User {user.username} removed successfully!")
        else:
            print("User not found.")


def find_user_by_login(login):
    with app.app_context():
        user = User.query.filter_by(login=login).first()
        if user:
            return user
        else:
            print("User not found.")
            return None


def find_user_by_email(email):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        else:
            print("User not found.")
            return None


def get_city_id(s_city: str) -> int:
    city_id = 0
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': WeatherID})
        data = res.json()
        city_id = data['list'][0]['id']

    except Exception as e:
        print("Exception (find):", e)
    return city_id


def check_name(name: str, errs: list) -> bool:
    if not re.match(r'^[а-яА-ЯёЁ\s]+$', name):
        errs.append("Имя и фамилия должны содержать только русские буквы")
        return False
    return True


def check_login(login: str, errs: list) -> bool:
    if not re.match(r'^[a-zA-Z0-9_]{6,20}$', login):
        errs.append("Логин должен содержать латинские буквы, цифры, _ и быть длиной от 6 до 20 символов")
        return False
    if find_user_by_login(login):
        errs.append("Пользователь с таким логином уже существует")
        return False
    return True


def check_password(password: str, errs: list) -> bool:
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,15}$', password):
        errs.append(
            "Пароль должен содержать хотя бы 1 строчную букву, 1 заглавную букву и 1 цифру и быть длиной от 8 до 15 символов")
        return False
    return True


def check_email(email: str, errs: list) -> bool:
    if not re.match(r'^\S+@\S+\.\S+$', email):
        errs.append("Email должен быть валидным")
        return False
    if find_user_by_email(email):
        errs.append("Пользователь с таким email уже существует")
        return False
    return True






# def check_age(age: int, err: list) -> bool:
#     pass


def get_weather(city_id: int):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': WeatherID})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Exception (weather):", e)
        return None


@app.route('/')
def index():
    current_minute = datetime.datetime.now().minute
    return render_template('home_page.html', display_link=current_minute % 2 == 0)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')  # запрос к данным формы
        password = request.form.get('password')
        user = find_user_by_login(login)
        if user:
            if user.password != password:
                message = 'Неверный логин или пароль'
                return render_template('login.html', message=message, login=login)
            session['user_id'] = user.id
            session['username'] = user.username
        else:
            message = 'Неверный логин'
            return render_template('login.html', message=message, login=login)

        return redirect(url_for('index'))

    session['click_count'] = 0
    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
    # ------------- pydantic --------------
    # 
    #     try:
    #         user_data = UserRegister.model_validate(request.form.to_dict())
    #         print(user_data, type(user_data))
    #     except:
    #         pass
    # ----------------------------------------
        
        
        username = request.form['username']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        errors = []

        # Проверка имени и фамилии (только русские буквы)
        check_name(username, errors)

        # Проверка логина (латинские буквы, цифры, _ , от 6 до 20 символов)
        check_login(login, errors)

        # Проверка пароля (1 строчная, 1 заглавная, 1 цифра, от 8 до 15 символов)
        check_password(password, errors)

        # Проверка email (валидный email)
        check_email(email, errors)

        # Проверка возраста (целое число от 12 до 100)    
        try:
            age = int(age)
            if age < 12 or age > 100:
                errors.append("Возраст должен быть целым числом от 12 до 100")
        except ValueError:
            errors.append("Возраст должен быть целым числом от 12 до 100")

        if errors:
            for error in errors:
                flash(error)
            return render_template('register.html', username=username, login=login, email=email, age=age)
        else:
            add_user(username, login, email, password, age)
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/duck/')
def duck():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    url = requests.get('https://random-d.uk/api/random').json()['url']
    return render_template('duck.html', url=url)


@app.route('/fox/<int:num>/')
def fox(num: int):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if 1 <= num <= 10:
        urls = []
        for i in range(num):
            res = requests.get('https://randomfox.ca/floof/').json()
            urls.append(res['image'])
        return render_template('fox.html', urls=urls)
    else:
        return '<h1 style="color:red">Введите число от 1 до 10</h1>'


@app.route('/weather-minsk/')
def weather_msk():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = get_weather(625144)
    return render_template('weather.html', weather=data)


@app.route('/weather/<string:city>/')
def weather(city: str):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    city_id = get_city_id(city)
    data = get_weather(city_id)
    return render_template('weather.html', weather=data)


@app.route('/weather-reg/')
def weather_reg():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    current_minute = datetime.datetime.now().minute
    if current_minute % 2 != 0:
        return redirect(url_for('index'))
    city_ids = [625144, 629634, 620127, 627907, 627904, 625665]  #ID областных центров РБ
    weather_data = [get_weather(city_id) for city_id in city_ids]
    return render_template('weather_reg.html', weather_data=weather_data)


@app.route('/clicker/', methods=['GET', 'POST'])
def clicker():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['click_count'] += 1
    return render_template('clicker.html', num=session['click_count'])


@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)
