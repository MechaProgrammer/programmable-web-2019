from flask import Blueprint, request, Response, url_for, abort
from flask_restplus import Resource, Api, fields, Namespace, reqparse
import json
from models.models import db
from models import api, blueprint
from utils.error import create_error_response, error_model, create_error_model
from sqlalchemy.exc import IntegrityError


users = Namespace(name='Users', description='User controls')
asd = 'asdasdasd'

control_scheme = api.model('Controls', {
    'uri': fields.String
})

user_models = api.model('User models', {
        'user': fields.String(example='model user', description='Username', required=True),
        'balance': fields.Float(example=133, description='Account balance in euros'),
})

user_model = api.model('User model', {
    'properties': fields.Nested(user_models),
    'controls': fields.Nested(control_scheme)
})



MIMETYPE = "application/json"

# user_model = api.schema_model(
#     'Users', 
#     {
#         'title': 'user',
#         'type': 'object',
#         'properties': {
#             'items': {
#                 'type': 'array',
#                 'items': {
#                     'properties': {
#                         'type': 'object',
#                         'user': {
#                             'type': 'string',
#                             'description': 'Username'
#                         },
#                         'balance': {
#                             'type': 'integer',
#                             'description': 'account balance'
#                         }
#                     }
#                 }
#             },
#             '@controls': {
#                 'type': 'object',
#                 'properties': {
#                     'href': {
#                         'type': 'string',
#                     }
#                 }
#             },
#         }
#     }
# )


error_schema = api.schema_model(
    'User schema', 
    {
        'properties': {
            'uri': {
                'type': 'string',
                'description': 'Username'
            },
            'name': {
                'type': 'integer',
                'description': 'account balance'
            },
        }
    }
)


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)


@users.route('/<string:user>/')
@users.param('user', 'Account user')
class User(Resource):
    @users.response(404, description='Not found', model=create_error_model(url='/api/users/<user>/', error="Not found", message='User: <user> was not found'))
    @users.response(200, description='Found', model=user_model)
    @users.marshal_with(user_model)
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
class User1(Resource):
    @users.response(201, 'Created', headers={"Location": '/api/users/<user>/'})
    @users.response(409, description='User already exists', model=create_error_model(url='/api/users/', error="Already exists", message='User already exists', self='/api/users/<user>/'))
    @users.expect(user_models)
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
