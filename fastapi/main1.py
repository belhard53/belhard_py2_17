from fastapi import FastAPI, Depends
from pydantic import BaseModel

import uvicorn



class STaskAdd(BaseModel):
   name: str
   description: str | None = None


app = FastAPI()

@app.get('/', tags=['Привет'])
async def home():
    return {'id':1, 'name':'Vasya'}




@app.post('/', tags=['hello1'])
async def add_task(task: STaskAdd = Depends()):
    # kdsffl
    return {'data':task['name']} 
 
 
# if __name__ == '__main__':    
#     uvicorn.run ("main:app", reload=True)  
 
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload  

# PS C:\Belhard\Python\!UrokiPro> uvicorn main1:app
# ERROR:    Error loading ASGI app. Could not import module "main1".