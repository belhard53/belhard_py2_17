from flask import Flask, render_template
import os

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места
# print(BASE_DIR)

users=['user1', 'user2', 'user3', 'suer4', 'user5', 'user6']

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

# модель MVC
    # model
    # view
    # controller

# app.add_url_rule("/", index) # если так  тогда без @app.route

# @app.route("/")
# def index():
#     return "Hello Python 123"

@app.route("/")
def index():
    return render_template('index.html')

# @app.route("/main2/item/<ind:id>/pic/")
@app.route("/sheet1/")
def sheet1():
    return render_template("1.html", h="HELLO 123456", users=users)


# на уроке не работал т.к. не было @ перед app    
@app.route('/sheet2/')
def sheet2():
    return render_template("2.html")    

@app.route("/test/<int:num>/")
def test(num):
    return f"тест номер {num} запущен"

@app.route("/message/<login>/<mes>")
def message(login, mes):
    return f" сообщение {login} --- {mes}"


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)
