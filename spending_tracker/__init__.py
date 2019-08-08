from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_restplus import Api


app = Flask("Spending-tracker")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
db.init_app(app)


blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(
    blueprint,
    title='Money saving app',
    version='0.1',
    description='Save money by using this app!'
)
