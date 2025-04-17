from fastapi import APIRouter, Depends, HTTPException
from schema import *
from database import UserRepository as ur

user_router = APIRouter(
    prefix="/users", # слэш оставляем открытыми
    tags=['Пользователи']
)

default_router = APIRouter()

@default_router.get('/', tags=['api'])
async def index():
    return {'data':'ok'}


@user_router.get('')
async def get_users() -> list[User]:
    users = await ur.get_users()
    return users

@user_router.get('/{id}')
async def get_user(id) -> User:
    user = await ur.get_user(id=id)
    if user:
        return user
    # return {'err':"User not found"} # но тогда get_user(id) -> User | dict[str,str]
    raise HTTPException(status_code=404, detail="User not found")

@user_router.post('')
async def get_user(user:UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}