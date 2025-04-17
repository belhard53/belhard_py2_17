from pydantic import BaseModel, ConfigDict

class UserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None
    
class User(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class UserId(BaseModel):
    id: int
    
# class Quiz    

