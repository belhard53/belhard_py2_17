from fastapi import FastAPI, Depends
from pydantic import BaseModel

# import uvicorn



class STaskAdd(BaseModel):
   name: str
   description: str | None = None


app = FastAPI()

@app.get('/', tags=['Default'])
async def home(q: str="*", filter: str=""):    
    return {'id':1, 'name':'Vasya', 'q':q, 'f':filter}



@app.post('/', tags=['hello1'])
async def add_task(task: STaskAdd = Depends()):
    # добавляем в базу
    return {'data':task['name']} 
 
 
# if __name__ == '__main__':    
#     uvicorn.run ("main:app", reload=True)  
 
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload  
