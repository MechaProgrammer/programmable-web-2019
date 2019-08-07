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
#from gevent.pywsgi import WSGIServer


def create_file():
    new_file = Path(__file__).parents[1]
    print(new_file)
    os.mkdir(new_file  / 'test')


@click.command()
@click.option('--port', default=5000, help='Service port')
def run(port):
    api.add_namespace(users, path='/users')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    create_file()
    app.run(debug=True, port=port)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


#if __name__ == '__main__':
    #run()
