
from pydantic import BaseModel, EmailStr
from typing import Optional
class posts(BaseModel): #inherit from base model
    name: str
    title: str
    published: int = 1
    rating: int = 10

class postcreate(posts): #inherit from postd without add any fields hoacwj co the add them filde
    pass

class postresponse(posts): #inherit for posts, nees co qua nhieu field, khoog the ngon viet lai thi inherit nhu vay
    ID: int 
    class Config: #di return trar veef sqlschema model neen may khong hieu nen them dong nay der chuyen ve pandetic model
        orm_mode = True

class usercreate(BaseModel):
    Name: str
    Password: str
    Email: EmailStr #tu dong check validate email co hop li k

class userout(BaseModel): #reponese
    Name: str
    Email: EmailStr 
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    Email: EmailStr
    Password: str

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None