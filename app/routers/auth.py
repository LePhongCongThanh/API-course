from fastapi import APIRouter, status, HTTPException, Response, Depends
from ..schemas import UserLogin 
from sqlalchemy.orm import session
from  ..database import get_db
from .. import models
from .. import utils
router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: UserLogin, db: session=Depends(get_db)):
    user = db.query(models.user).filter(models.user.Email == user_credentials.Email).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your email does not exit")
    if not utils.verify(user_credentials.Password, user.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your password is not correct")  
    return {"token":"succesfully"}
    
          