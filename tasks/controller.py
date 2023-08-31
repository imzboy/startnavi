from flask import abort

from tasks.enums import ContentTypes, Statuses
from tasks.models import VideoProcessTask



class TaskProccesingOrchestrator:
    """By utilizing Liskov subtitution we can write one logic for all current and future task types."""

    # dict to add more maps of content type to tasks types.
    _content_type_to_process_type = {
        ContentTypes.MP4: VideoProcessTask,
    }

    @classmethod
    def start(cls, file) -> str:
        """Define what task type is needed for the format and start the processing."""
        content_type = file.content_type
        task_type = cls._content_type_to_process_type.get(content_type)
        
        if not task_type:
            supported_content_types = ", ".join([c_type.value for c_type in cls._content_type_to_process_type.keys()])
            abort(400, f"File type '{file.content_type}' not supported, supported types are "
                       f"{supported_content_types}.")
        # create a task instance
        task = task_type()
        # fill the pk attr 
        task.save()
        # get the correct task type
        process = task.proccessing_task
        # start the processing and set the task_id for future lookups
        process.apply_async(args=[file.read()], task_id=task.pk)
        return task.pk


    @classmethod
    def end(cls, content_type: str, task_id: str) -> None:
        """Change the task status to FINNISHED. Used by celery task."""
        task_type = cls._content_type_to_process_type.get(content_type)
        task = task_type.get(task_id)
        task.status = Statuses.FINNISHED
        task.save()
