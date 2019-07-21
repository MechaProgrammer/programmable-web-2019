import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from models.models import create_app, db
from models import api, blueprint


app = create_app()

from models.users.usermodels import users
api.add_namespace(users)
app.register_blueprint(blueprint)
app.app_context().push()


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
