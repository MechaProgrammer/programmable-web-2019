from flask import Blueprint, request, Response
from flask_restplus import Resource, Api, Namespace, fields
import json
from models.models import db
from models import api


MIMETYPE = "application/json"

users = api.namespace(name='users', description='User controls')


user_model = api.model('User model', {
    'name': fields.String
})


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


@users.route('/<string:user>/')
class User(Resource):
    def get(self, user):
        resp = {
            'user': user,
            'balance': 1002
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@users.route('/')
class User1(Resource):
    @api.expect(user_model)
    def post(self):
        user = UserItem(
            name=request.json['name']
        )
        db.session.add(user)
        db.session.commit()
        return Response(status=201, mimetype=MIMETYPE)