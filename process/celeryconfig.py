import os

broker_url = os.getenv("REDIS_URL")
result_backend = os.getenv("RESULT_BACK")
imports = ("process.tasks",)