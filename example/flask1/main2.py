from flask import Flask, render_template, redirect, url_for, session
import os

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места
# print(BASE_DIR)



users=['user1', 'user2', 'user3', 'suer4', 'user5', 'user6']

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

app.config['SECRET_KEY'] = 'my secret key 12334'

n = 0



@app.route("/")
def index():
    if not session['n']:
        session['n'] = 0
        
    
     
    return render_template('index.html')

@app.route("/s1/")
def s1():
    session['n'] += 1   
    return render_template('1.html', n = session['n'])
    # return redirect(url_for('index'))






app.run(debug=True)
