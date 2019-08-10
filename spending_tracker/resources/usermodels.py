from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.resources.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError
from spending_tracker.db_models.db_models import UserModel
from spending_tracker.resources.walletmodels import WalletItem
from spending_tracker.resources.categorymodels import CategoryCollection
from spending_tracker.models.user import User
from flask import url_for
from spending_tracker.utils.helpers import schema_builder


users = Namespace(name='Users', description='User controls')


MIMETYPE = "application/json"

schema_415 = create_error_model('Unsupported media type', url='/api/users/', error="Unsupported media type",
                                message="Requests must be JSON")
schema_200 = schema_builder(UserModel, 'self', '/api/users/<user>/')
schema_404 = create_error_model('Not found', url='/api/users/<user>/', error="Not found", message='User: <user> was not found')


@users.route('/<string:user>/')
@users.param('user', 'Account user')
class UserResource(Resource):
    @users.response(404, description='Not found', model=schema_404)
    @users.response(200, description='Success', model=schema_200)
    def get(self, user):
        user_collection = User()
        resp = user_collection.retrieve_user(user)
        resp['links'] = {
                'self': url_for('api.Users_user_resource', user=user),
                'collection': url_for('api.Users_user_collection')
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
            url='/api/users/',
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
                self=uri
            )
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    def get(self):
        users = {}
        users_all = User().retrive_all()
        for user in users_all:
            users[user.user] = {
                "self": url_for('api.Users_user_resource', user=user.user),
                "wallet": url_for('api.User_wallet_item', user=user.user),
                "categories": url_for('api.CategoryModel_category_collection', user=user.user)
            }
        return Response(json.dumps(users, indent=4), 200)


