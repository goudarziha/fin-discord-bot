import asyncio
import discord

from celery.result import AsyncResult
from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse

from worker import create_task

app = FastAPI()

@app.get("/")
async def read_root():
    return {"hello": "world"}

@app.post("/tasks", status_code=201)
def run_task(payload = Body(...)):
    task_type = payload['type']
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})

@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)

