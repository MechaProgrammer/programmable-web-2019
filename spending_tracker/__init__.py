from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restplus import Api
import os


db = SQLAlchemy()


def create_app():
    project_root = os.path.abspath(os.path.dirname(__file__))
    app = Flask("Spending-tracker")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(project_root, 'spending_tracker.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    title='Spending Tracker',
    version='0.1',
    description='Track your spending with this app',
    doc='/api/doc',
    default_mediatype='json'
)
