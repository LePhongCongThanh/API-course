from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #tuong tac voi database
from fastapi import FastAPI, Response, status, HTTPException, Depends #import class FastAPI() từ thư viện fastapi
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from . import models, schemas
from. import utils
import mysql.connector
import time
from .config import settings
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL) #ket noi vào database 
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

# Dependency
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

#Situation of Working with SQL
device = FastAPI()
while True: #vong lap co diue kien  khi nào true thi dung
    try:
        conn = mysql.connector.connect(host="database-1.cuzymwi7r2cr.us-east-1.rds.amazonaws.com" ,
                                   database='mydb', user='admin', password='Congthanh123')
        cursor = conn.cursor(dictionary=True) #để thêm tên cott mỗi khí query // cursor chính là instance để mà có thể thao tác query update trên database
        print("Database connection successfully!")
        break    
    except Exception as error:
        print(" Database Connection failed")
        print("The error is:", error)
        time.sleep(5) # wait for 5 seconds before retrying

my_post = [{"title": "title of post 1", "content": "content 1", "ID": 1}, 
           {"title": "title of post 2", "content": "content 2", "ID": 2}]
# get method
# Path operation
@device.get("/") # giống flask, khai báo phương thức get và url o day la root
async def root(): # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
    return {"message": "Welcome to my API"} #trả lại cho user


@device.get("/posts") # cũng là get nhưng URLs khác
async def get_post(): # get_post là tên function
    return {"data": "This is your posts"}, {"all_post": my_post}

@device.get("/db/posts")
def all_db_posts():
    cursor.execute("""Select * from post""")
    posts = cursor.fetchall()
    print("all your posts:", posts)
    return {"all your posts: ": posts}


# post method


@device.post("/posts", status_code=status.HTTP_201_CREATED) # thay doi status code
def create_posts(post: schemas.postcreate):
    post_dict = post.dict()
    post_dict['ID'] = randrange(0,100000) #them mot key value trong library
    my_post.append(post_dict) # Add vào variable my_post
    print(post_dict)
    return {"message": "submit successfully"}, {"data": post_dict} 

@device.post("/db/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posts: schemas.postcreate):
    post_dict = posts.dict()
    cursor.execute("""INSERT INTO post(name, title, published, rating) VALUES (%s, %s, %s, %s)""",
                    (post_dict['name'], post_dict['title'], post_dict['published'], post_dict['rating'])
                    )
    conn.commit()
    cursor.execute("""Select * from post where ID = LAST_INSERT_ID()""")
    new_post = cursor.fetchone()
    print(new_post)
    return {"your post": new_post}



# get individual post
## get latest post
@device.get("/posts/recent/latest")
def get_post_latest():
    post = my_post[len(my_post)-1] #index chay tu 0 đến len(mypost)-1
    return {"detail post": post}

## get specific post
def find_posts(ID): 
    for p in my_post:
        if p['ID'] == ID:
            return p #4

@device.get("/posts/{ID}") #1 The "{ID}" part is a path parameter that allows you to specify the ID of the post in the URL.
def get_posts(ID: int): #2
    post = find_posts(ID) #3
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Your post {ID} is not found")
        #solution2
        # response.status_code = status.HTTP_404_NOT_FOUND .gán biến response :Response vào def get_posts
        # return {"message": f" Your post {ID} not found"}
    return {"detail post": post} 

@device.get("/db/posts/{ID}") #1 The "{ID}" part is a path parameter that allows you to specify the ID of the post in the URL.
def get_posts(ID: int): #2
    cursor.execute("""SELECT * from post where ID = %s""", (ID,))
    post = cursor.fetchone() #3
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Your post {ID} is not found")
        #solution2
        # response.status_code = status.HTTP_404_NOT_FOUND .gán biến response :Response vào def get_posts
        # return {"message": f" Your post {ID} not found"}
    return {"detail post": post} 





# Delete Posts
def find_index_post(ID): 
    for i, p in enumerate(my_post):
        if p['ID'] == ID:
           return i

@device.delete("/posts/{ID}", status_code=status.HTTP_204_NO_CONTENT) # path parameter
def delete_post(ID: int):
    index = find_index_post(ID) 
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your post {ID} does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # dont want to send any data back, clients đủ hiểu ntn

@device.delete("/db/posts/{ID}")
def delete_post(ID: int):
    cursor.execute("""Select * from post where ID = %s""", (ID,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your post {ID} is not found")
    cursor.execute("""Delete from post where ID = %s""", (ID,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# Put method
@device.put("/posts/{ID}")
def update_post(ID: int, post: schemas.posts):
    index = find_index_post(ID) # tim xem post nay no co ton tai khong theo ID, neu ton tai tim index cua no de thay the
    if index == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           details=f"your post {ID} is not found") # neu k co, thi stop
    post_dict = post.dict() #chuyen thong tin post update nhan vao thanh dict
    post_dict['ID'] = ID # gan ID cu cho no
    my_post[index] = post_dict # update vi tri
    return {"message": "updated successfully"}, {"data": post_dict}

@device.put("/db/posts/{ID}")
def update_post(ID: int, post: schemas.posts):
    cursor.execute("""SELECT * FROM post where ID = %s""", (ID,))
    post_ID = cursor.fetchone()
    if post_ID == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail=f"your post {ID} does not exist") # neu k co, thi stop
    post_dict = post.dict()
    cursor.execute("""UPDATE post SET name = %s, title = %s, published = %s, rating = %s WHERE ID = %s""", 
                   (post_dict['name'], post_dict['title'], post_dict['published'], post_dict['rating'], str(ID)))# tim xem post nay no co ton tai khong theo ID, neu ton tai tim index cua no de thay the
    conn.commit()
    cursor.execute("""SELECT * from post where ID = %s """, (ID,))
    updated_post = cursor.fetchone()
    return {"message": "updated successfully"}, {"data": updated_post}


# Post method
@device.post("/createpost") # phuong thức post user send data to API server
async def create_posts(payload: dict = Body(...)): #thông tin server được lưu dưới dạng dictionary
    print(payload)
    return {"message": "successfully creat a post"}, {"Your Post": f"title: {payload['title']} and message: {payload['message']}"} # trả lại cho user

#pandatic base model
class comment(BaseModel):
    name: str
    comment: str
    published: bool = False # khong dien gi trả về False
    rating: int = None # Khong dien gi tra về None

@device.post("/comment")
def create_comment(cmt: comment):
    print(cmt) 
    print(cmt.rating, cmt.name)
    print(cmt.dict)
    return {"New comment": "Successfully comment"} # trả về user

