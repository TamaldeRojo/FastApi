from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #aa
from config.db import conn
import json
from typing import Optional

from schemas.user import userModel,usersModel
from schemas.exercise import exerciseModel,exercisesModel

from bson.objectid import ObjectId
from passlib.hash import sha256_crypt

app = FastAPI()
  
class Req(BaseModel):
    email: str
    password: str
class Exercise(BaseModel):
    email: Optional[str] = None 
    typeOf: str
    count: str
    
    
@app.get('/')
def read_root():
    urls = """{
        "usersGET":"/users",
        "usersGET_ID":"/users/id",
        "signup":"/signup",
        "signin":"/signin",
        "exercisesGET":"/exercises",
        "exercisesPOST":"/exercises"
        }"""
    json_urls = json.loads(urls)
    return json_urls

@app.get('/users')
def users():
    return usersModel(conn.MoveFit.Users.find())

app.get('/user/{id}')
def user(id: str):
    return userModel(conn.MoveFit.Users.find_one({"_id":ObjectId(str(id))}))

@app.post('/signup')
def signup(user: Req):
    user = dict(user)
    if conn.MoveFit.Users.find_one({"email": user['email']}):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user['password'])
    user_data = {"email": user['email'], "password": hashed_password}
    conn.MoveFit.Users.insert_one(user_data)

    return {"message": "Registration successful"},True

def hash_password(password):
    return sha256_crypt.hash(password)

@app.post('/signin')
def signin(user: Req):
    vUser = dict(user)
    print(vUser)
    plainPassword = vUser["password"]
    try: 
        theUser = conn.MoveFit.Users.find_one({"email":vUser['email']})
        print(theUser)
        if not theUser or not verify_password(plainPassword,theUser['password']):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        return {"message": "Login successful"}, True
    except Exception as e:
        print(f"Error : {e}")
        
def verify_password(plain_password, hashed_password):
    return sha256_crypt.verify(plain_password, hashed_password)

@app.post('/exercises')
def exercises(ex: Exercise):
    vEx = dict(ex)
    print(vEx["email"])
    try:
        user_data = {"email": vEx['email'], "typeOf": vEx['typeOf'],"count":vEx["count"]}
        conn.MoveFit.Exercises.insert_one(vEx)
        print("Succesfully Inserted i think...")
        return {"message" : "All good i guess"}
    except Exception as e:
        print(f"No exercise posted: {e}")
        return {"message" : "Not fine, there is an error"}

@app.get('/exercises')
def exercises():
    return exercisesModel(conn.MoveFit.Exercises.find())

