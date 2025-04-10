from flask import (Flask, redirect, render_template, 
                request, session, url_for, jsonify)
from models import db, User, Question, Quiz, db_add_new_data

import os
from random import shuffle


BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'db', 'db_quiz.db')


html_config = {
    'admin':True,
    'debug':False
}

# menu = {}

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'secretkeysecretkeysecretkey1212121'

db.init_app(app)


with app.app_context():
    db_add_new_data()
    # quizes = Quiz.query.all()
    # # for q in quizes:
    #     # print(q, q.name, q.user, q.question)
    #     # for quest in q.question:
    #     #     print(quest)
        
    # print(quizes[1].question[1], quizes[1].question[1].answer)
    
    # question = db.session.query(Question).get(1)
    
    # добавить квиз
    # user = db.session.query(User).get(1)
    # quiz = Quiz(form.get('quiz_name'), user)
    # db.session.add(quiz)
    # db.session.commit()
    
    

@app.route('/', methods = ['GET'])
def index():
    return render_template('base.html', html_config = html_config)


@app.route('/quiz/', methods = ['POST', 'GET'])
def view_quiz():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        # print(quizes)
        return render_template('start.html', quizes=quizes, html_config = html_config)
    session['quiz_id'] = request.form.get('quiz')
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answers'] = 0
    return redirect(url_for('view_question'))



@app.route('/question/', methods = ['POST', 'GET'])
def view_question():
    
    # если квиз еще не выбран - перенаправляем на выбор
    if not session['quiz_id'] or session['quiz_id'] == -1:
        return redirect(url_for('view_quiz'))

    # если пост значит пришел ответ на вопрос        
    if request.method == 'POST':        
        question = Question.query.filter_by(id=session['question_id']).one()       
        # если ответы сходятся значит +1
        if question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        # следующий вопрос
        session['question_n'] += 1


    quiz = Quiz.query.filter_by(id = session['quiz_id']).one()
    
    #если вопросы закончились
    if int(session['question_n']) >= len(quiz.question):
        session['quiz_id'] = -1 # чтобы больше не работала страница question
        return redirect(url_for('view_result'))
    
    #если вопросы еще не закончились
    else:
        question = quiz.question[session['question_n']]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3 ]
        shuffle(answers)

        return render_template('question.html', 
                               answers=answers, 
                               question=question, 
                               html_config=html_config)


@app.route('/result/')
def view_result():
    return render_template('result.html', 
                    right=session['right_answers'], 
                    total=session['question_n'],
                    html_config=html_config)




app.run(debug=True)