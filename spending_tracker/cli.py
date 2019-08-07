import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from .models.models import app, db
from spending_tracker.models import api, blueprint
from spending_tracker.models.users.usermodels import users
from pathlib import Path
import os


def create_file():
    new_file = Path(__file__).parents[4]
    folder_name = new_file / 'Results'
    folder_name1 = new_file / 'Data'
    if folder_name.exists():
        return
    if folder_name1.exists():
        return
    else:
        os.mkdir(folder_name)
        os.mkdir(folder_name1)


@click.command()
@click.option('--port', default=5000, help='Service port')
@click.option('--debug', default=False, is_flat=True, help='App debug mode')
def run(port, debug):
    api.add_namespace(users, path='/users')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    create_file()
    app.run(debug=debug, port=port)
