import typing as tp
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Query
from fastapi import Body
from .. import models
from . import schemas
from .auth import AuthHandler
from .schemas import UserCreateSchema
from django.db import IntegrityError
from django.db import transaction


api = FastAPI()

auth_handler = AuthHandler()


@api.get(
    '/tasks',
    responses={
        200: {'model': schemas.TaskSchema},
    },
)
def get_tasks(
    user=Depends(auth_handler.user_getter),
) -> tp.List[schemas.TaskSchema]:
    result = models.Task.objects.all()
    return [schemas.TaskSchema.from_model(task) for task in result]


@api.get(
    '/tasks/{task_id}',
    summary='Получить задание по id',
    responses={
        200: {'model': schemas.TaskSchema},
    },
)
def get_task(
    user=Depends(auth_handler.user_getter),
    task_id: int = Query(None)
) -> schemas.TaskSchema:
    try:
        task = models.Task.objects.get(id=task_id)
    except models.Task.DoesNotExist:
        raise HTTPException(status_code=404, detail='Item not found')

    return schemas.TaskSchema.from_model(task)


@api.get('/task_title/{task_title}',
         summary='Поиск по заголовку',
         responses={
             200: {'model': schemas.TaskSchema},
         }
         )
def get_task_title(
        user=Depends(auth_handler.user_getter),
        task_title: str = Query(None),
                   ) -> tp.List[schemas.TaskSchema]:
    result = models.Task.objects.filter(title=task_title).order_by('-date_of_change')
    return [schemas.TaskSchema.from_model(task) for task in result]


@api.post(
    '/tasks',
    responses={
        200: {'model': schemas.TaskSchema}
    }
          )
def create_task(
    user=Depends(auth_handler.user_getter),
    task: schemas.TaskCreateSchema = Body(...)
) -> schemas.TaskSchema:
    created_tack = models.Task.objects.create(
        title=task.title,
        status=task.status,
        type=task.type,
        priority=task.priority,
        description=task.description,
        executor_id=task.executor_id,
        creator=user,
    )
    return schemas.TaskSchema.from_model(created_tack)


@api.put('/tasks',
         responses={
             200: {'model': schemas.TaskSchema}
         }
         )
def update_task(
        user=Depends(auth_handler.user_getter),
        task_id: int = Query(...),
        task: schemas.TaskCreateSchema = Body(...)
) -> schemas.TaskSchema:
    task_to_update = models.Task.objects.get(id=task_id)
    task_to_update.title = task.title
    task_to_update.status = task.status
    task_to_update.type = task.type
    task_to_update.priority = task.priority
    task_to_update.description = task.description
    task_to_update.executor_id = task.executor_id
    task_to_update.save()
    return schemas.TaskSchema.from_model(task_to_update)


@api.delete('/tasks/delete/{task_id}',)
def delete_task(
    user=Depends(auth_handler.user_getter),
    task_id: int = Query(...),
):
    try:
        query = models.Task.objects.get(pk=task_id)
        query.delete()
    except models.Task.DoesNotExist:
        raise HTTPException(status_code=404, detail='Item not found')


@api.post('/register', status_code=201)
def register(auth_details: UserCreateSchema):
    try:
        hashed_password = auth_handler.get_password_hash(auth_details.password)
        models.User.objects.create(login=auth_details.login, password=hashed_password)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Username is taken')


@api.post('/login')
def login(auth_details: UserCreateSchema):
    users = models.User.objects.all()
    user = None
    for x in users:
        if x.login == auth_details.login:
            user = x
            break
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user.password)):#user or users?
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user.login)
    return {'token': token}
