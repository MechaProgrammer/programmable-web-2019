import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from models.models import create_app, db
from models import api, blueprint
from models.users.usermodels import users


def run():
    app = create_app()
    api.add_namespace(users, path='/users')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    app.run(debug=True)


if __name__ == '__main__':
    run()
