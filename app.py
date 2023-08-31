from flask import Flask
from werkzeug.exceptions import BadRequest

from tasks.views import bp as tasks_bp


app = Flask(__name__)

# register all the blueprintss
app.register_blueprint(tasks_bp)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000 # 5 MB

# error handlers
@app.errorhandler(404)
def not_found(error: BadRequest) -> dict:
    return {"error": "Not found."}, 404

@app.errorhandler(400)
def wrong_request(error: BadRequest) -> dict:
    return {"error": error.description}, 400


"""
The idea is to make a video proccessing service
1. recieve a video
2. validate the video, mp4 format and > 5 min.
3. create a task in (I don't know right now), generate a unique id of the task
4. return a uid to user
5. user has an endpoint that he can use to check the tasks statuses
6. if status is done the user can retrieve the results 

REST endpoints:
GET /tasks - returns a list of running tasks
POST /taks - recieves a video and creates a new task
GET /tasks/{uid} - return a specific task and it's compact results
GET /tasks/{uid}/results - returns results in full
"""

@app.route("/ping")
async def hello():
    return "PONG"


