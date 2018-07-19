# app/__init__.py

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True,
                static_folder="./static", template_folder="./static/templates")
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)


    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    from app import models

    migrate = Migrate(app, db)

    from api.api import api as api_module
    app.register_blueprint(api_module)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app