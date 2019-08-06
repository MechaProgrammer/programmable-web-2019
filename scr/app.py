import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
#from scr.models.models import db, app
# from scr.models.models import create_app
# from scr.models import api, blueprint
# from scr.models.users.usermodels import users
#from gevent.pywsgi import WSGIServer


@click.command()
@click.option('--port', default=5000, help='Service port')
def run(port):
    from scr.models.models import app, db
    from scr.models import api, blueprint
    from scr.models.users.usermodels import users
    #app, db = create_app()
    app1 = app
    api.add_namespace(users, path='/users')
    app1.register_blueprint(blueprint)
    app1.app_context().push()
    db.create_all()
    app1.run(debug=True, port=port)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


if __name__ == '__main__':
    run()
