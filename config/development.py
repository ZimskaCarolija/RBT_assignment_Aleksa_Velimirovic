from .base import BaseConfig
from dotenv import load_dotenv
import os

# UČITAJ .env OVDE!
load_dotenv()  # <-- DODAJ OVO!

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')

    # DODAJ PROVERU!
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "DEV_DATABASE_URL nije postavljen u .env fajlu!\n"
            "Proveri da li .env postoji u root folderu projekta."
        )