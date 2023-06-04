from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

secret_key = "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik"
Algorithm = "HS256"
token_expire_minutes = 60

def create_access_token (data: dict):

    expire_time = datetime.utcnow() + timedelta(minutes=token_expire_minutes)
    data.update({"exp": expire_time}) #payload bao gom ID_user and expire_time
    encoded_jwt = jwt.encode(data, secret_key, algorithm=Algorithm) #payload, secretkey, header
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=Algorithm) #payload la dictionary bao goom key_value la user_ID vax Exp
        ID: str = payload.get("user_ID") 
        if ID == None:
            raise credentials_exception
    except JWSError: # nguyen cao block tren sai vi du sai secret key, sal algrithm thi raise cai nay
        raise credentials_exception
        
    return ID
    
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="login")    
def get_current_user(token: str = Depends(OAuth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"could not validate credential", 
                                          headers= {"WWW-authenication": "Bearer"})
    user_ID = verify_access_token(token, credentials_exception)
    user = db.query(models.user).filter(models.user.ID_user == user_ID).first()
    print(user)
    return user
