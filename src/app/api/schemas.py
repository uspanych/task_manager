import datetime
from pydantic import BaseModel
from .. import models
#from src.app import models
from pydantic import Field
from enum import Enum
import datetime
import typing as tp


class Type(str, Enum):
    BUG = 'bug'
    TASK = 'task'


class Priority(str, Enum):
    CRITICAL = 'critical'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Status(str, Enum):
    TO_DO = 'to_do'
    IN_PROGRESS = 'in_progress'
    CODE_REVIEW = 'code_review'
    DEV_TEST = 'dev_test'
    TESTING = 'testing'
    DONE = 'done'
    WONTFIX = 'wontfix'


class _BaseUserSchema(BaseModel):
    login: str = Field(..., description='Логин')


class UserCreateSchema(_BaseUserSchema):
    password: str = Field(...)


class UserSchema(_BaseUserSchema):
    id: int
    role: tp.Optional[str] = Field(None)

    @classmethod
    def from_model(cls, model: models.User):
        return cls(
            id=model.id,
            login=model.login,
            role=model.role,
        )


class TaskSchema(BaseModel):
    id: int = Field(...)
    title: str = Field(..., description='Заголовок')
    status: str = Field(..., description='Статус')
    type: str = Field(..., description='Тип')
    priority: str = Field(description='Приоритет')
    description: tp.Optional[str] = Field(None, description='Описание')
    executor: tp.Optional[UserSchema]
    creator: tp.Optional[UserSchema]
    date_of_creation: datetime.date
    date_of_change: datetime.date

    @classmethod
    def from_model(cls, model: models.Task):
        return cls(
            id=model.id,
            title=model.title,
            status=model.status,
            type=model.type,
            priority=model.priority,
            descriprion=model.description,
            executor=UserSchema.from_model(model.executor) if model.executor is not None else None,
            creator=UserSchema.from_model(model.creator),
            date_of_creation=model.date_of_creation,
            date_of_change=model.date_of_change,
        )


class TaskCreateSchema(BaseModel):
    title: str
    status: Status
    type: Type
    priority: Priority
    description: str
    executor_id: tp.Optional[int] = Field(None)


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'