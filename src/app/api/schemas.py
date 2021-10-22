import datetime
from pydantic import BaseModel
from .. import models
from pydantic import Field
from enum import Enum
import datetime
import typing as tp


class UserCreateSchemes(BaseModel):
    id: int
    login: str = Field(..., description='Логин')
    password: str = Field(...)


class UserScheme(BaseModel):
    id: int
    login: str


class TaskSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(..., description='Заголовок')
    status: str = Field(..., description='Статус')
    type: str = Field(..., description='Тип')
    priority: str = Field(description='Приоритет')
    description: str = Field(description='Описание')
    executor: UserScheme
    creator: UserScheme
    date_of_creation: datetime.datetime
    date_of_change: datetime.datetime

    @classmethod
    def from_model(cls, model: models.Task):
        return cls(
            id=model.id,
            title=model.title,
            status=model.status,
            type=model.type,
            priority=model.priority,
            descriprion=model.description,
            executor=model.executor,
            creator=model.creator,
            date_of_creation=model.date_of_creation,
            date_of_change=model.date_of_change,
        )


class TaskCreateSchema(BaseModel):
    title: str = Field(...)
    status: str = Field(...)
    type: str = Field(...)
    priority: str
    description: str
    executor_id: tp.Optional[int] = Field(None)

