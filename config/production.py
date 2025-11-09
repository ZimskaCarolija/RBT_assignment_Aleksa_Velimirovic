from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('PRO_DATABASE_URL')
    DEBUG = False
