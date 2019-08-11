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

schema_415 = create_error_model(
    'Unsupported media type',
    url='/api/users/',
    error="Unsupported media type",
    message="Requests must be JSON"
)

schema_200 = schema_builder(UserModel, 'self', '/api/users/<user>/')

schema_404 = create_error_model(
    'Not found',
    url='/api/users/<user>/',
    error="Not found",
    message='User: <user> was not found'
)


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
    @users.doc(description='Get user info')
    @users.response(404, description='Not found', model=schema_404)
    @users.response(200, description='Success', model=single_user_model)
    def get(self, user):
        user_collection = User()
        resp = {'properties': user_collection.retrieve_user(user), 'links': {
            'self': url_for('api.Users_user_resource', user=user),
            'collection': url_for('api.Users_user_collection'),
            'wallet': url_for('api.Wallet_wallet_item', user=user),
            'categories': url_for('api.Categories_category_collection', user=user)
        }}
        return Response(json.dumps(resp), 200, mimetype=MIMETYPE)

    @users.doc(description='Delete user')
    @users.response(204, description='Deleted')
    @users.response(404, description='Not found', model=schema_404)
    def delete(self, user):
        db_user = User()
        db_user.delete(user)
        return 204


@users.route('/')
class UserCollection(Resource):
    @users.doc(description='Add user')
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
    @users.response(400, 'Bad Request')
    @users.response(415, description='Unsupported media type', model=schema_415)
    @users.expect(UserModel.get_schema(), validate=True)
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
            headers={'Location': f'{uri}'})

    @users.doc(description='Get all users')
    @users.response(200, description='Success', model=all_users)
    def get(self):
        user_collection = {
            'properties': {}
        }
        users_all = User().retrive_all()
        for user in users_all:
            user_collection['properties'][user.user] = {
                "self": url_for('api.Users_user_resource', user=user.user),
                "wallet": url_for('api.Wallet_wallet_item', user=user.user),
                "categories": url_for('api.Categories_category_collection', user=user.user)
            }
        return Response(json.dumps(user_collection, indent=4), 200, mimetype=MIMETYPE)


