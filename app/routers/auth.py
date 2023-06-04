from fastapi import APIRouter, status, HTTPException, Response, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm #class include username, password 
from ..schemas import UserLogin, Token 
from sqlalchemy.orm import session
from  ..database import get_db
from .. import models
from .. import utils, oauth2
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: session=Depends(get_db)):
    user = db.query(models.user).filter(models.user.Email == user_credentials.username).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Your email does not exit")
    if not utils.verify(user_credentials.password, user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Your password is not correct")
    token = oauth2.create_access_token(data = {"user_ID": user.ID_user}) #lay user ID lam payload
    return  {"access_token": token, "token_type": "bearer"}

@router.post("/login2", response_model=Token)
def login(user_credentials: UserLogin, db: session=Depends(get_db)):
    user = db.query(models.user).filter(models.user.Email == user_credentials.Email).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Your email does not exit")
    if not utils.verify(user_credentials.Password, user.Password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Your password is not correct")  
    token = oauth2.create_access_token(data = {"user_ID": user.ID_user})
    return  {"access_token": token, "token_type": "bearer"}
    
          