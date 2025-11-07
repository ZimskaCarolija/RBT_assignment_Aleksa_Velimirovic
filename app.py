from flask import Flask
from flask_migrate import Migrate
from models import db
from config.development import DevelopmentConfig
from dotenv import load_dotenv

load_dotenv()

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)  
    app.config.from_object(config_class)
    db.init_app(app)
    Migrate(app, db)

    @app.route('/')
    def index():
        return "Flask + SQLAlchemy + Flask-Migrate setup is working!"

    return app

app = create_app()
