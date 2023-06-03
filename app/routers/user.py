from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from sqlalchemy.orm import session #tuong tac database
from ..database import get_db

router = APIRouter(
    prefix="/sqlalchemy",
    tags=["Users"]
)

@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=schemas.userout)
def creatuser(user: schemas.usercreate, db: session=Depends(get_db)):
    #hashed_password = pwd_context.hash(user.Password) #transform password thanh hash
    #user.Password = hashed_password # gan lai nhuw ban dau
    user.Password = utils.hash(user.Password)
    new_user =models.user(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{ID}", response_model=schemas.userout)
def get_user(ID: int, db: session=Depends(get_db)):
    user = db.query(models.user).filter(models.user.ID_user == ID).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user {ID} does not exit")
    return user