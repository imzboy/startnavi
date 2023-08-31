import datetime
from abc import ABC
from flask import abort

from pydantic import Field, validator
from redis_om import NotFoundError, JsonModel
from celery.result import AsyncResult
from celery import Task
from process import app

from process.tasks import start_video_processing
from tasks.enums import Statuses



class BaseTask(JsonModel, ABC):
    """Base abstract task class for storing all default fields needed for task processing."""
    
    # The celery task that will be used for proccessing.
    @property
    def processing_task(self) -> Task:
        # it needs to be a property for non-attributes in pydantic model
        raise NotImplementedError("Define a 'get_processing_task' function.")

    status: Statuses = Field(Statuses.PENDING.value)
    started_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    ended_at: datetime.datetime = None
    result: str = None

    @validator("ended_at", always=True)
    def get_ended_at(cls, v, values, **kwargs) -> datetime.datetime | None:
        """Pydantic v1 version of @property computed field.
           Take the stored 'date_done' from result backend."""
        async_result = AsyncResult(values["pk"], app=app)
        return async_result.date_done
    
    @validator("result", always=True)
    def get_result(cls, v, values, **kwargs) -> str | None:
        """Take the stored 'results' from result backend to minimize the size of one db entry."""
        async_result = AsyncResult(values["pk"], app=app)
        return async_result.result

    @classmethod
    def get_or_404(cls, pk):
        """Shortcut function for get or raise 404 error."""
        try:
            model = cls.get(pk)
            return model
        except NotFoundError:
            abort(404)

    class Config:
        underscore_attrs_are_private = True



class VideoProcessTask(BaseTask):
    """Model for video processing tasks."""

    @property
    def proccessing_task(self) -> Task:
        return start_video_processing
