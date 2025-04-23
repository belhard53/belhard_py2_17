from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_filter import FilterDepends

from models import UserFilter
from schema import *
from database import UserRepository as ur, QuizRepository as qr



# fastapi_filter


default_router = APIRouter()

user_router = APIRouter(
    prefix="/users", # слэш оставляем открытыми
    tags=['Пользователи']
)

quiz_router = APIRouter(
    prefix="/quizes", # слэш оставляем открытыми
    tags=['Квизы']
)

question_router = APIRouter(
    prefix="/questions", # слэш оставляем открытыми
    tags=['Вопросы']
)




@default_router.get('/', tags=['api'])
async def index():
    return {'data':'ok'}

# USER ------------------------
@user_router.get('')
async def get_users(
            limit:int = Query(ge=1, lt=10, default=3), 
            offset:int = Query(ge=0, default=0),
            user_filter: UserFilter = FilterDepends(UserFilter)
          ) -> dict[str, int | list[User]]:
    
    users = await ur.get_users(limit, offset, user_filter)
    return {"data":users, "limit":limit, "offset":offset}
    # return users

@user_router.get('/{id}')
async def get_user(id: int) -> User:
    user = await ur.get_user(id=id)
    if user:
        return user
    # return {'err':"User not found"} # но тогда get_user(id) -> User | dict[str,str]
    raise HTTPException(status_code=404, detail="User not found")

@user_router.post('')
async def add_user(user:UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}



# QUIZES ----------------------
@quiz_router.get('')
async def get_quizes() -> list[Quiz]:    
    quizes = await qr.get_quizes()    
    return quizes

@quiz_router.get('/{id}')
async def quiz(id: int) -> QuizWithQuestions:
# async def quiz(id: int) -> Quiz: # если без вопросов 
    quiz = await qr.get_quiz(id=id)
    if quiz:
        return quiz    
    raise HTTPException(status_code=404, detail="Quiz not found")

@quiz_router.get('/{id}/questions')
async def quiz_questions(id: int) -> list[Question]:
    quiz = await qr.get_quiz(id=id)
    if quiz:
        return quiz.question    
    raise HTTPException(status_code=404, detail="Quiz not found")

@quiz_router.post('')
async def add_quiz(quiz:QuizAdd = Depends()):
    id = await qr.add_quiz(quiz)
    return {'id':id}

@quiz_router.post('/{quiz_id}/link')
async def link_quiz(quiz_id:int, question_id:int) -> dict[str,bool]:
# async def link_quiz(quiz_id:int, question_id:list[int]) -> dict[str,bool]:
    try:
        res = await qr.link_quiz(quiz_id, question_id)            
    except Exception as e: 
        raise HTTPException(status_code=422, detail=str(e))
    
    return {'res':bool(res)}



# QUESTIONS ----------------------
# доделаем сами