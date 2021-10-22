import typing as tp
from fastapi import FastAPI, HTTPException
from fastapi import Query
from fastapi import Body
from .. import models
from . import schemas


api = FastAPI()


@api.get('/echo')
def echo(message: str = Query('hello')):
    return message


@api.get(
    '/tasks',
    responses={
        200: {'model': schemas.TaskSchema},
    },
)
def get_tasks() -> tp.List[schemas.TaskSchema]:
    result = models.Task.objects.all()
    return [schemas.TaskSchema.from_model(task) for task in result]


@api.get(
    '/tasks/{task_id}',
    summary='Получить задание по id',
    responses={
        200: {'model': schemas.TaskSchema},
    },
)
def get_task(task_id: int = Query(None)) -> schemas.TaskSchema:
    try:
        task = models.Task.objects.get(id=task_id)
    except models.Task.DoesNotExist:
        raise HTTPException(status_code=404, detail='Item not found')

    return schemas.TaskSchema.from_model(task)


@api.post(
    '/tasks',
    responses={
        200: {'model': schemas.TaskSchema}
    }
          )
def create_task(task: schemas.TaskCreateSchema = Body(...)) -> int:
    models.Task.objects.create(
        title=task.title,
        status=task.status,
        type=task.type,
        priority=task.priority,
        description=task.description,
        executor=task.executor_id,
        creator=task.creator_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
    return schemas.TaskSchema.from_model(task)


@api.delete('/tasks/delete/{task_id}',)
def delete_task(task_id: int):
    try:
        query = models.Task.objects.get(pk=task_id)
        query.delete()
    except models.Task.DoesNotExist:
        raise HTTPException(status_code=404, detail='Item not found')





