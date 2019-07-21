import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///development.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(
    blueprint,
    title='Money saving app',
    version='0.1',
    description='Save money by using this app!'
)
app.register_blueprint(blueprint)
MIMETYPE = "application/json"
asd = api.namespace(name='users', description='User controls')
api.add_namespace(asd)


@asd.route('/<string:user>/')
class User(Resource):
    def get(self):
        resp = {
            'user': "Markus",
            'balance': 1002
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@asd.route('/')
class User(Resource):
    def get(self):
        resp = {
            'user': "Markus",
            'balance': 1002
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


if __name__ == '__main__':
    app.run(debug=True)
