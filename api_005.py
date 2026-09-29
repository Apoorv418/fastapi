"""
To stream SSE with FastAPI, 
use yield in your path operation function and 
set response_class=EventSourceResponse.
"""
from collections.abc import AsyncIterable , Iterable
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.sse import EventSourceResponse, ServerSentEvent
import asyncio

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str | None

items = [
    Item(name = "Plumber", desc = "a person who helps with fitment in the water related issues"),
    Item(name = "Constructor", desc = "a person who builds your and my houses when necessasry "),
    Item(name = "Doctor", desc = "an apple a days keeps the doctor away"),
]

# @app.get("/items/stream", response_class = EventSourceResponse)
# async def ss_items() -> AsyncIterable[Item]:
#     for item in items:
#         await asyncio.sleep(2) 
#         yield item

@app.get("/items/stream", response_class = EventSourceResponse)
async def stream_items()-> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(comment = "stream of item updates")
    for i, desc in enumerate(items):
        yield ServerSentEvent(data = desc, event = "item_update", id = str(i+1), retry = 5000)
