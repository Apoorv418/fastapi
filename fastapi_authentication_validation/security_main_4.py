#real world example we will be working now##
# jwt - json web tokens
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from pydantic import BaseModel

Secret_Key = "ae9b04c9236368c6e12ad26555909e371cec1a2efa7892e60cc95a3b582fa290"
Algorithm = "HS256"
Access_Token_Expire_Minutes = 30

fake_users_db = {
    "john Doe": {
        "username": "johnDoe",
        "full_name": "John Doe",
        "email": "johnDoe@example.com",
        "hashed_password":  "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": "False"
    }
}

class Token(BaseModel):
    access_token : str
    token_type: str

class Token_Data(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password : str

password_hash = Password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

app = FastAPI()

