from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import select, Integer, ForeignKey, String, Table, Column, func


from schema import UserAdd
from datetime import datetime

import os

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
    
DB_PATH = os.path.join(DB_DIR, 'fastapi.db')    

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
# engine = create_async_engine("sqlite+aiosqlite:///example//fastapi//db//fastapi.db")
# engine = create_async_engine("sqlite+aiosqlite:///db//fastapi.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass
    
#    # можно тут добавить тогда эти столбцы будут во всех таблицах
#    # т.к. мы наследуемся от этого класса
    
#     id: Mapped[int] = mapped_column(primary_key=True)
    
#     # будет вписывать дататайм при создании записи
#     dateCreate: Mapped[datetime] = mapped_column(        
#                                         server_default=func.now(),
#                                         nullable=False)
    
#     # будет вписывать дататайм при обновлении записи
#     dateUpdate: Mapped[datetime] = mapped_column(        
#                                         server_default=func.now(),
#                                         server_onupdate=func.now(),
#                                         nullable=False)

class UserOrm(Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]
    # quiz = relationship('QuizOrm', backref='user')
    
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        
async def delete_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)     


async def add_test_data():
    async with new_session() as session:
        users = [
            UserOrm(name='user1', age=20),
            UserOrm(name='user2', age=30, phone='123456789')
        ]

        session.add_all(users)
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
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)
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