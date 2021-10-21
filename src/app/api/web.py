from fastapi import FastAPI
from fastapi import Query


api = FastAPI()


@api.get('/echo')
def echo(message: str = Query('hello')):
    return message


@api.get('/tasks/{id}')
def get_task(id: int = Query(None)):
    return id