from flask import Flask, render_template, redirect, url_for, session, request
import os

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__file__) # так работает если проект открыт из любого места
# print(BASE_DIR)



users=['user1', 'user2', 'user3', 'suer4', 'user5', 'user6']

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

app.config['SECRET_KEY'] = 'my secret key 12334'

# Flask по умолчанию хранит данные сессий на стороне клиента в виде файла cookie. 
# Однако, для обеспечения безопасности, Flask использует подписанные cookie, 
# что означает, что данные сессии шифруются и проверяются на целостность с 
# помощью секретного ключа, который хранится на сервере.

# Если вам нужно хранить данные сессий на сервере (например, для более сложных 
# приложений или когда вы не хотите доверять клиенту), вы можете использовать 
# сторонние расширения, такие как Flask-Session. Это расширение позволяет 
# хранить сессии в различных хранилищах, таких как файловая система, 
# Redis или база данных.

@app.route("/")
def index():
    if not session.get('n1'):
        session['n1'] = 0
    if not session.get('n2'):
        session['n2'] = 0   
    session['n1'] += 1
    session['qqq'] = "dsasdasdsdsds"*1000
    return render_template('index2.html', n = session['n1'])

@app.route("/s1/")
def s1():
    session['n2'] += 1   
    return render_template('1.html', n = session['n2'], users=users)
    # return redirect(url_for('index')) # перенаправляем на главную



@app.route("/s3/", methods=['GET', 'POST'])
def s3():
    if request.method == 'POST':
        err=[]
        user={}
        user['login'] = request.form.get('login123')
        user['pas'] = request.form.get('password123')
        print(user['login'], user['pas'])
        ok = True # если все пришло без ошибок
        if ok:
            return redirect(url_for('index'))
        return render_template('3.html', err=err, user=user)    
    return render_template('3.html')
    # 

@app.route('/get_form/')
def get_form():
    pass

app.run(debug=True)
