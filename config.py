import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = os.environ.get("DEBUG", True)