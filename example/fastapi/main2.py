# pip install fastapi,  uvicorn, pydantic, aiosqlite, sqlalchemy

from fastapi import FastAPI
from routers import user_router, default_router
import uvicorn
from contextlib import asynccontextmanager
from database import create_table, delete_table, add_test_data

import os

BASE_DIR = os.path.dirname(__file__)

@asynccontextmanager # реагирует на  методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await create_table()
    await add_test_data()
    print("------Bases build-------------")
    
    yield
    await delete_table()
    print("-------------Bases drooped------------")


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(user_router)

 
if __name__ == '__main__':    
    uvicorn.run ("main2:app", reload=True, port=8200)  
    # uvicorn.run ("other_folder.main2:app", reload=True, port=8500)  
 
 
# uvicorn main2:app --host 0.0.0.0 --port 8000 --reload  