from pydantic import BaseModel, ConfigDict

# USER ------------------------
class UserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None
    
class User(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class UserId(BaseModel):
    id: int
    
    
# QUESTION ------------------------
class QuestionAdd(BaseModel):
    question: str
    answer: str
    wrong1: str
    wrong2: str
    wrong3: str

class Question(QuestionAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuestionId(BaseModel):
    id: int
    

# QUIZ ------------------------
class QuizAdd(BaseModel):
    name: str
    user_id: int
    
class Quiz(QuizAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class QuizId(BaseModel):
    id: int
    
class QuizWithQuestions(Quiz):
    question: list[Question]    
    
    