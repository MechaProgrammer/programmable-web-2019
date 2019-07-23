from flask import Blueprint, request, Response, url_for
from flask_restplus import Resource, Api, Namespace, fields
import json
from models.models import db
from models import api, blueprint


users = Namespace(name='Users', description='User controls')

user_model = api.model('User model', {
        'name': fields.String(example='model user', description='Users name'),
        'balance': fields.Float(example=133, description='Account balance in euros.')
})


MIMETYPE = "application/json"


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)


@users.route('/<string:user>/')
@users.param('user', 'Account name')
class User(Resource):
    def get(self, user):
        resp = {
            'user': user,
            'balance': 1002
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@users.route('/')
class User1(Resource):
    @users.expect(user_model)
    def post(self):
        user = UserItem(
            name=request.json['name'],
            balance=request.json['balance']
        )
        db.session.add(user)
        db.session.commit()
        uri = api.url_for(User, user=request.json['name'])
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})
