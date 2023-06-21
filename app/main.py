from fastapi import FastAPI, Response, status, HTTPException, Depends #import class FastAPI() từ thư viện fastapi
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import mysql.connector
import time
from . import models, schemas
from .database import engine, get_db
from. import utils
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI() # gọi constructor/instance và gán vào biến app

origins = ["*"] # khong có \ nhé
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router) #include vào fastapi
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hello World!!"}

# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# models.base.metadata.create_all(bind=engine) # gọi từ  file model để tạo bảng, tai database


