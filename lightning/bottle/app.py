from flask import Flask
from bottle.db import db
from bottle.extensions import migrate


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("APP")
    app.config.from_object("bottle.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_database(app)
    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    init_taks_runner(app)

    @app.route("/")
    def hello_world():
        return "⚡️⚗️⚡️"
    return app


def configure_database(app):
    """configure database"""
    db.init_app(app)


def configure_extensions(app):
    """configure flask extensions"""
    migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    pass


def register_blueprints(app):
    """register all blueprints for application"""
    pass


def init_taks_runner(app=None):
    """Init async job executor"""
    pass
