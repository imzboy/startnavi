from celery import Celery
from config import Config


app = Celery("video_processing")
app.config_from_object("process.celeryconfig", namespace="CELERY")
