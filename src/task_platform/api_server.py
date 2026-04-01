from fastapi import FastAPI
from typing import Iterable

app = FastAPI()

tasks = [
    {"id": "1", "payload": {"type": "email", "user": 10}},
    {"id": "2", "payload": {"type": "order", "order_id": 42}},
]


@app.get("/tasks")
def get_tasks() -> Iterable:
    return tasks
