from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restplus import Api


db = SQLAlchemy()


def create_app():
    app = Flask("Spending-tracker")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(
    blueprint,
    title='Spending Tracker',
    version='0.1',
    description='Track your spending with this app'
)
