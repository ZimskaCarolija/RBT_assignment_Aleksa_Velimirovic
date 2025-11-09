from .base import BaseConfig
from dotenv import load_dotenv
import os

load_dotenv() 

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DEV_DATABASE_URL not set in .env file!\n"
        )