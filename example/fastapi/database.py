from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from models import *

from schema import UserAdd, QuizAdd
from datetime import datetime

import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'fastapi.db')    

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
# engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True) # echo=True - все sql в консоль
# engine = create_async_engine("sqlite+aiosqlite:///example//fastapi//db//fastapi.db")
# engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class  DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
    
    @classmethod            
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)     

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30, phone='123456789'),
                UserOrm(name='user3', age=41, phone='11'),
                UserOrm(name='user4', age=42, phone='22'),
                UserOrm(name='user5', age=43, phone='33'),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]
            
            quizzes = [
                QuizOrm(name='quiz1', user=users[0]),
                QuizOrm(name='quiz2', user=users[1]),
                QuizOrm(name='quiz3', user=users[2])
            ]
            
            questions = [
                QuestionOrm(question='Сколько будeт 2+2*2', answer='6',
                            wrong1='8', wrong2='2', wrong3='0'),
                QuestionOrm(question='Сколько месяцев в году имеют 28 дней?', answer='Все',
                            wrong1='Один', wrong2='Ни одного', wrong3='Два'),
                QuestionOrm(question='Какой рукой лучше размешивать чай?', answer='Ложкой',
                            wrong1='Правой', wrong2='Левой', wrong3='Любой')
            ]
            quizzes[0].question.append(questions[0])
            quizzes[0].question.append(questions[1])
            quizzes[1].question.append(questions[1])
            quizzes[1].question.append(questions[2])
            quizzes[2].question.append(questions[0])
            quizzes[2].question.append(questions[2])

            session.add_all(quizzes)
            session.add_all(users[3:])
            
            # flush() - используется для синхронизации изменений с базой данных без завершения транзакции
            # проверяет, что операции (вставка, обновление) не вызывают ошибок
            # Если последующие действия в транзакции зависят от предыдущих изменений, 
            # flush() делает эти изменения видимыми в рамках текущей сессии
            await session.flush() 
            await session.commit()

        



class UserRepository:
    
    @classmethod           
    async def add_user(cls, user: UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            print(data)
            user = UserOrm(**data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
            
    @classmethod
    async def get_users(cls, limit, offset, user_filter) -> list[UserOrm]:
        async with new_session() as session:
            print(user_filter)
            # query = select(UserOrm).limit(limit).offset(offset)
            query = select(UserOrm)
            query = user_filter.filter(query).limit(limit).offset(offset)
            query = user_filter.sort(query)
            print(query)
            
            # query = select(UserOrm).filter(user_filter).limit(limit).offset(offset)
            res = await session.execute(query)
            users = res.scalars().all()
            return users
            
    @classmethod
    async def get_user(cls, id) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).filter(UserOrm.id==id)
            # query = text(f"SELECT * FROM users WHERE id={id}")
            res = await session.execute(query) 
            user = res.scalars().first()
            return user
        
class QuizRepository:
    
    @classmethod           
    async def add_quiz(cls, quiz: QuizAdd) -> int:
        async with new_session() as session:
            data = quiz.model_dump()            
            quiz = UserOrm(**data)
            session.add(quiz)
            await session.flush()
            await session.commit()
            return quiz.id
            
    @classmethod
    async def get_quizes(cls) -> list[QuizOrm]:
        async with new_session() as session:                        
            query = select(QuizOrm)                        
            # query = select(QuizOrm).options(selectinload(QuizOrm.question)) # c вопросами
            res = await session.execute(query)
            quizes = res.scalars().all()            
            return quizes
            
    @classmethod
    async def get_quiz(cls, id) -> QuizOrm:
        async with new_session() as session:
            
            query = select(QuizOrm).where(QuizOrm.id==id) # чтобы работать со связью нужен lazy='joined' в models
            
            # еще другие варианты получить данные с коллекцией по связи
            # query = (select(QuizOrm) 
            #             .options(selectinload(QuizOrm.question))
            #             .filter(QuizOrm.id == id))             
            
            # # joinedload — один запрос с JOIN
            # session.execute(select(Quiz).options(joinedload(Quiz.questions)))

            # # selectinload — два запроса: основной и для связанных вопросов
            # session.execute(select(Quiz).options(selectinload(Quiz.questions)))
            
            res = await session.execute(query) 
            quiz = res.scalars().first()     
            # print(quiz.question)
            return quiz
    
    @classmethod
    async def link_quiz(cls, quiz_id, question_id) -> bool:
        async with new_session() as session:
            
            query = select(QuizOrm).where(QuizOrm.id==quiz_id)
            res = await session.execute(query)
            quiz = res.scalars().first()                         
            if not quiz:
                raise ValueError("Quiz not found")
            if question_id in [q.id for q in quiz.question]:
                raise ValueError("Already")
            
            query = select(QuestionOrm).where(QuestionOrm.id==question_id)            
            res = await session.execute(query)
            question = res.scalars().first()
            if not question:
                raise ValueError("Question not found")
            
            quiz.question.append(question)
            await session.flush()
            await session.commit()
        
            return True