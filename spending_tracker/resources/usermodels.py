from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import api
from spending_tracker.resources.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError
from spending_tracker.db_models.db_models import UserModel
from spending_tracker.models.user import User
from flask import url_for
from spending_tracker.utils.helpers import schema_builder


users = Namespace(name='Users', description='User controls')

user_links = api.model('user links', {
    'self': fields.String(example='/api/users/<user>/'),
    'collection': fields.String('/api/users/'),
    'wallet': fields.String('/api/user/<user>/money/'),
    'categories': fields.String('/api/categories/<user>/')
})

single_user_model = api.model('all users', {
    'properties': fields.Nested(UserModel.get_schema()),
    'links': fields.Nested(user_links)
})


MIMETYPE = "application/json"

schema_415 = create_error_model('Unsupported media type', url='/api/users/', error="Unsupported media type",
                                message="Requests must be JSON")
schema_200 = schema_builder(UserModel, 'self', '/api/users/<user>/')
schema_404 = create_error_model('Not found', url='/api/users/<user>/', error="Not found", message='User: <user> was not found')


user_info = api.model('User info', {
    'self': fields.String(example='/api/users/<user>/'),
    'wallet': fields.String(example='/api/user/<user>/money/'),
    'categories': fields.String(example='/api/categories/<user>/')
})

user_model = api.model('User specs', {
    'user': fields.Nested(user_info)
})

all_users = api.model('All users query', {
    'properties': fields.Nested(user_model)
})


@users.route('/<string:user>/')
@users.param('user', 'Account user')
class UserResource(Resource):
    @users.response(404, description='Not found', model=schema_404)
    @users.response(200, description='Success', model=single_user_model)
    def get(self, user):
        user_collection = User()
        resp = {}
        resp['properties'] = user_collection.retrieve_user(user)
        resp['links'] = {
                'self': url_for('api.Users_user_resource', user=user),
                'collection': url_for('api.Users_user_collection'),
                'wallet': url_for('api.User_wallet_item', user=user),
                'categories': url_for('api.CategoryModel_category_collection', user=user)
            }
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)


@users.route('/')
class UserCollection(Resource):
    @users.response(201, 'Created', headers={'Location': '/api/users/<user>/'})
    @users.response(
        409,
        description='User already exists',
        model=create_error_model(
            'Already exists',
            url='api/users/<user>/',
            error="Already exists",
            message='User already exists')
        )
    @users.response(415, description='Unsupported media type', model=schema_415)
    @users.expect(UserModel.get_schema())
    def post(self):
        uri = url_for('api.Users_user_resource', user=request.json['user'])
        try:
            User().create(request.json)
        except IntegrityError:
            return create_error_response(
                409,
                'Already exists',
                f'User: {request.json["user"]} already exists',
                url=uri
            )
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    @users.response(200, description='Success', model=all_users)
    def get(self):
        users = {
            'properties': {}
        }
        users_all = User().retrive_all()
        for user in users_all:
            users['properties'][user.user] = {
                "self": url_for('api.Users_user_resource', user=user.user),
                "wallet": url_for('api.User_wallet_item', user=user.user),
                "categories": url_for('api.CategoryModel_category_collection', user=user.user)
            }
        return Response(json.dumps(users, indent=4), 200)


