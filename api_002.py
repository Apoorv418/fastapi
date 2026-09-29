"""
#SQLModel is built on top of SQLAlchemy and Pydantic. It was made by the same author of FastAPI to be the perfect match for FastAPI applications that need to use SQL databases.
Tip

You could use any other SQL or NoSQL database library you want (in some cases called "ORMs"), FastAPI doesn't force you to use anything. 😎

As SQLModel is based on SQLAlchemy, you can easily use any database supported by SQLAlchemy (which makes them also supported by SQLModel), like:

PostgreSQL
MySQL
SQLite
Oracle
Microsoft SQL Server, etc.
"""

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, Select

class Hero(SQLModel, Table = True):
    id: int | None = Field(default = None, primary_key = True)
    name: str = Field(index = True)
    age: int | None = Field(default = None, index = True)
    secret_name = str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args = connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/heroes/")
def create_hero(hero: Hero, session: sessionDep)->Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes")
def read_heroes(
    session: sessionDep,
    offset: int =0,
    limit: Annotated[int, Query(le = 100)] = 100,

)-> list[Hero]:
    heroes = session.exec(Select(Hero).offset(offset).limit(limit)).all()
    return heroes

class HeroBase(SQLModel):
    name : str = Field(index = True)
    age: int |None = Field(default = None, index = True)

class Hero(HeroBase):
    id : int |None = Field(default = None, primary_key= True)
    secret_name : str

class HeroPublic(HeroBase):
    id : int

class HeroCreate(HeroBase):
    secret_name = str

class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name = str | None = None


@app.post("/heroes/", response_model = HeroPublic)
def create_hero(hero: HeroCreate, session: sessionDep):
    db_Hero = Hero.model_validate(hero)
    session.add(db_Hero)
    session.commit()
    session.refresh(db_Hero)
    return db_Hero

@app.get("/heroes/", response_model = list[HeroPublic])
def get_hero(session: sessionDep, offset : int = 0, limit: Annotated[int, Query(le=100)]= 100,):
    heroes = session.exec(Select(Hero).offset(offset).limit(limit)).all()
    return heroes

