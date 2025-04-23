# pip install fastapi,  uvicorn, pydantic, aiosqlite, sqlalchemy

from fastapi import FastAPI
from routers import user_router, default_router, quiz_router, question_router
import uvicorn
from contextlib import asynccontextmanager
from database import DataRepository as dr

import os

BASE_DIR = os.path.dirname(__file__)

@asynccontextmanager # реагирует на  методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await dr.create_table()
    await dr.add_test_data()
    print("------Bases build-------------")
    
    yield
    await dr.delete_table()
    print("-------------Bases drooped------------")


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(user_router)
app.include_router(quiz_router)
app.include_router(question_router)

 
if __name__ == '__main__':    
    uvicorn.run ("main2:app", reload=True, port=8600)  
    # uvicorn.run ("other_folder.main2:app", reload=True, port=8500)  
 
 
# uvicorn main2:app --host 0.0.0.0 --port 8000 --reload  