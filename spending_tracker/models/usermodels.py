from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.models.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError
from spending_tracker.db_models.db_models import UserItem


users = Namespace(name='Users', description='User controls')


class SchemeBuilder(dict):
    def add_control(self, ctrl_name, href, **kwargs):
        if ctrl_name not in self:
            self[ctrl_name] = {}
        self[ctrl_name] = kwargs
        self[ctrl_name] = fields.Url(example=href)


MIMETYPE = "application/vnd.collection+json"


def schema_builder(ctrl_name=None, href=None):
    asd = SchemeBuilder()
    asd.add_control(ctrl_name, href)
    control_scheme = api.model('links', asd)
    user_schema = api.model('User schema', {
        'properties': fields.Nested(UserItem.get_schema()),
        'links': fields.Nested(control_scheme)
    })
    return user_schema


@users.route('/<string:user>/')
@users.param('user', 'Account user')
class User(Resource):
    @users.response(404, description='Not found', model=create_error_model('Not found', url='/api/users/<user>/', error="Not found", message='User: <user> was not found'))
    @users.response(200, description='Success', model=schema_builder('self', '/api/users/<user>/'))
    def get(self, user):
        db_user = UserItem.query.filter_by(user=user).first()
        if db_user is None:
            return create_error_response(404, "Not found", f'User: {user} was not found')
        resp = {
            'user': db_user.user,
            'balance': db_user.balance,
            'links': {
                'self': api.url_for(User, user=user),
                'collection': api.url_for(UserCollection)
            }
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
    @users.expect(UserItem.get_schema())
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
