from typing import Dict
from flask import Blueprint, abort, request


from tasks.models import VideoProcessTask
from tasks.controller import TaskProccesingOrchestrator


bp = Blueprint("tasks_bp", import_name="tasks")


@bp.route("/tasks", methods=["GET"])
async def list() -> Dict[str, list]:
    return VideoProcessTask.all_pks()


@bp.route("/tasks/<task_id>", methods=["GET"])
async def detail(task_id: str) -> dict:
    return VideoProcessTask.get_or_404(pk=task_id).dict()


@bp.route("/tasks", methods=["POST"])
async def create() -> dict:
    # check if the user sent the file.
    if 'file' not in request.files:
        abort(400, "No file send.")
    file = request.files["file"]
    task_id = TaskProccesingOrchestrator.start(file)
    return {"uid": task_id}
