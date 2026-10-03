from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

class User(BaseModel):
    username: str
    email:str | None = None
    full_name: str |None = None
    disabled: bool |None = None

def fakedecode_token(tokne):
    return User(
        username = token + "fakedecoded", email = "john@example.com", full_name = "John_Doe"
    )

async def get_current_user(token: Annotated[str, Depends(OAuth2_scheme)]):
    user = fakedecode_token(token)
    return user

@app.get("/users/me")
async def read_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


