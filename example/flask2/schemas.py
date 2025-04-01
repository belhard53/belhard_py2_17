from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserRegister(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    login: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    age: int = Field(gt=0, lt=120)
    
    @field_validator('username')
    def validate_username(cls, v):
        if not bool(re.fullmatch('[а-яА-ЯёЁ\s]+', v)):
            raise ValueError ("err - только русские")
        return v.title()