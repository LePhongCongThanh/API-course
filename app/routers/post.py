from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import session
from typing import List, Optional

router = APIRouter(
    prefix= "/sqlalchemy",
    tags= ["Posts"]
)

 
@router.get("/", response_model=list[schemas.postresponse]) #neu k dien gi thi phu thuoc vao depend(default)
def test_posts(db: session=Depends(get_db), user: schemas.userout=Depends(oauth2.get_current_user),
                limit: int=10, skip: int=0, search: Optional[str]=""): # limit la gioi han so bai viet chay ra tu bai viet gan nhat
    posts = db.query(models.Post2).filter(models.Post2.title.contains(search)).limit(limit).offset(skip).all() #skip=n la bo qua n bài đầu tiên

    return posts

@router.get("/posts/{ID}", response_model=schemas.postresponse)
def get_posts(ID: int, db: session=Depends(get_db), user: schemas.userout = Depends(oauth2.get_current_user)):
    post_id = db.query(models.Post2).filter(models.Post2.ID == ID).first()
    print(user.Email)
    if not post_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your post {ID} is not found")
    return post_id

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.postresponse)
def create_posts(posts: schemas.postcreate, db: session=Depends(get_db),
                  user: schemas.userout = Depends(oauth2.get_current_user)):
    print(user.ID_user)
    new_post = models.Post2(owner_id = user.ID_user, **posts.dict()) # dùng dòng này thay thế dòng dưới nó nhanh hơn
    # new_post = models.Post2(name=posts.name, title=posts.title, published=posts.published, rating=posts.rating)
    db.add(new_post) # add vào database
    db.commit()  # commit nó
    db.refresh(new_post) # truy cái post mới add gần nhat tu database  r lưu vào viến newposst
    print(new_post)
    return new_post

@router.delete("/posts/{ID}")
def delete_post(ID: int, db: session=Depends(get_db), user: schemas.userout=Depends(oauth2.get_current_user)):
    post2 = db.query(models.Post2).filter(models.Post2.ID == ID)
    post = post2.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post {ID} does not exist")
    if post.owner_id != user.ID_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform request")
    post2.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/post/{ID}")
def update_post(ID: int, post_update: schemas.posts, db: session=Depends(get_db),
                 user: schemas.userout = Depends(oauth2.get_current_user)):
    print(user.Email)
    post = db.query(models.Post2).filter(models.Post2.ID == ID)
    post_first = post.first()
    if post_first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post {ID} does not exist")
    if post_first.owner_id != user.ID_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform request")
    post.update(post_update.dict(),synchronize_session=False)
    db.commit()
    return {"your updated post": post.first()}
