from .base import BaseConfig
import os

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')
    DEBUG = True
