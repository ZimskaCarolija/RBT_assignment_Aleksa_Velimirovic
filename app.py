# app.py
from flask import Flask
from flask_migrate import Migrate
from models import db
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from dotenv import load_dotenv
from commands import register_commands
from routes.vacation import bp as vacation_bp 
from routes.users import bp as users_bp
from utils.response import ApiResponse 
import os
import logging

load_dotenv()
env = ProductionConfig
if os.getenv("FLASK_ENV") == "development":
    env = DevelopmentConfig

def create_app(config_class=env):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)

    from container import container
    with app.app_context():
        container.init_db(db.session)
        app.container = container

    register_commands(app)

    app.register_blueprint(vacation_bp)
    app.register_blueprint(users_bp)
    
    @app.errorhandler(404)
    def not_found(e):
        return ApiResponse.error("Route not found", 404)

    @app.errorhandler(401)
    def unauthorized(e):
        return ApiResponse.error("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return ApiResponse.error("Forbidden", 403)

    @app.errorhandler(500)
    def internal_error(e):
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)

    @app.route('/health')
    def health():
        return ApiResponse.success({"status": "healthy"})

    @app.route('/')
    def index():
        return "hello"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()