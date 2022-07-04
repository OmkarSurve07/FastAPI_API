from os import access
from typing import Optional
from urllib import response
from sqlalchemy import engine
from app import schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, utils, oauth2
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
from app import database


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
         conn = psycopg2.connect(host='localhost',
                                 database='tawqeedb',
                                 user='postgres',
                                 password='admin',
                                 cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to databse failed!")
        print("Error:", error)
        time.sleep(2)  # password check every two seconds if wrong !


@app.get("/sql")
def test_post(db: Session = Depends(get_db)):
    return{"status": "success"}


app.include_router(user.router)
# app.include_router(auth.router)

@app.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)) :
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            details=f"Invalid Credentials")

    # cretae JWT tocken here !
    access_token = oauth2.created_access_token({"user_id": user.id})
    return {"access_token" : access_token, "token_type": "bearer"}

    # return {"token": "Example Token"}



@app.get("/home")
async def root():
    return {"message": "WELCOME TO TAWQEE !"}
# login page API


class login(BaseModel):   # Created Models
    email: str
    password: str
    contact: Optional[int] = None


# @app.post("/login/{id}")
# async def root(data: login, id, response: Response):
#     print(id)
#     # login = cursor.execute("""SELECT * FROM login""")
#     # print(login)
#     customer_id = data.dict()
#     if not customer_id:
#         raise HTTPException(status_code=404)
#         # response.status_code = 404
#         # return {'message': f"post with id: {id} was not found"}
#     customer_id['id'] = range(0, 100000)
#     login_customer.append(customer_id)
#     return {"data": f"TAWQEE login customer {id}"}

login_customer = [{"id": 1}]


class CustomerData(BaseModel):
    name: str


@app.post("/createpost/{id}")
def create_post(data: CustomerData, id):
    print(data)
    # print(id)
    return {"data": f"post works {id}!"}


# "/users" can be added rather login.
# @app.post("/login", status_code=status.HTTP_201_CREATED)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # hash users password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.get("/login/{id}")
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id: {id} does not exist")
#     return user
@app.get("/manage_account")
async def root():
    return {"message": "WELCOME TO TAWQEE Manage Account Page !"}


# manage account post method with specific PK{id} from db.
@app.post("/manage_account/{id}")
def manage_account(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)) :
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    access_token = oauth2.created_access_token(date={"user_id": id})
    return {"access_token": access_token, "token_type": "bearer"}
