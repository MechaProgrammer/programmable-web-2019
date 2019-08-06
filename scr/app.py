import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from scr.models.models import app, db
from scr.models import api, blueprint
from scr.models.users.usermodels import users
#from gevent.pywsgi import WSGIServer


@click.command()
@click.option('--port', default=5000, help='Service port')
def run(port):
    api.add_namespace(users, path='/users')
    app.register_blueprint(blueprint)
    app.app_context().push()
    db.create_all()
    app.run(debug=True, port=port)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


if __name__ == '__main__':
    run()
