from flask import Flask
from flask_migrate import Migrate
from models import db
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from dotenv import load_dotenv
from commands import register_commands
import os

load_dotenv()
env = ProductionConfig
if os.getenv("FLASK_ENV") == "development":
    env = DevelopmentConfig

def create_app(config_class=env):

    app = Flask(__name__)  
    app.config.from_object(config_class)
    db.init_app(app)
    Migrate(app, db)
    register_commands(app) 
    from container import container
    container.init_db(db.session)
    app.container = container

    @app.route('/')
    def index():
        return "Flask + SQLAlchemy + Flask-Migrate setup is working!"

    return app

app = create_app()