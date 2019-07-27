from flask import Blueprint, request, Response, url_for, abort
from flask_restplus import Resource, Api, Namespace, fields, reqparse
import json
from models.models import db
from models import api, blueprint
from utils.error import create_error_response, error_model, create_error_model
from sqlalchemy.exc import IntegrityError


users = Namespace(name='Users', description='User controls')

user_model = api.model('User model', {
        'user': fields.String(example='model user', description='Username'),
        'balance': fields.Float(example=133, description='Account balance in euros')
})

MIMETYPE = "application/json"


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)


@users.route('/<string:user>/')
@users.param('user', 'Account user')
class User(Resource):
    @users.response(404, description='Not found', model=create_error_model(url='/api/users/<user>/', error="Not found", message='User: <user> was not found'))
    def get(self, user):
        db_user = UserItem.query.filter_by(user=user).first()
        if db_user is None:
            return create_error_response(404, "Not found", f'User: {user} was not found')
        resp = {
            'user': db_user.user,
            'balance': db_user.balance
        }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@users.route('/')
@users.response(201, 'Created', headers={"self": '/api/users/<user>/'})
class User1(Resource):
    @users.response(409, description='User already exists', model=create_error_model(url='/api/users/', error="Already exists", message='User already exists', self='/api/users/<user>/'))
    @users.expect(user_model)
    def post(self):
        uri = api.url_for(User, user=request.json['user'])
        user = UserItem(
            user=request.json['user'],
            balance=request.json['balance']
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", f'User: {request.json["user"]} already exists', self=uri)
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})
