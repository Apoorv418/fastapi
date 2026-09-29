"""
Stream JSON Lines with FastAPI¶
To stream JSON Lines with FastAPI you can,
instead of using return in your path operation function,
use yield to produce each item in turn.
"""
from collections.abc import AsyncIterable, Iterable
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str | None

items =[
    Item(name = "plumbus", desc = "Hello my name is plumbus what is your name?"),
    Item(name="Portal Gun", desc="A portal opening device."),
]

@app.get("/items/stream")
async def stream_items()->AsyncIterable[Item]:
    for item in items:
        yield item

@app.get("/items/no-sync")
def stream_no_async() ->Iterable[Item]:
    for item in items:
        yield item

@app.get("/items/stream-no-annotation")
async def stream_items_no_annotation():
    for item in items:
        yield item



