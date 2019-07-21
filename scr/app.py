import click
import json
from flask import Flask, Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from models.models import create_app, UserItem, db


blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(
    blueprint,
    title='Money saving app',
    version='0.1',
    description='Save money by using this app!'
)

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()

user = api.namespace(name='users', description='User controls')
api.add_namespace(user)

MIMETYPE = "application/json"

user_model = api.model('User model', {
    'name': fields.String
})


@user.route('/<string:user>/')
@user.param('user', 'The username')
class User(Resource):
    def get(self, user):
        resp = {
            'user': user,
            'balance': 1002
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@user.route('/')
class User(Resource):
    @api.expect(user_model)
    def post(self):
        user = UserItem(
            name=request.json['name']
        )
        db.session.add(user)
        db.session.commit()
        return Response(status=201, mimetype=MIMETYPE)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
