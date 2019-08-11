from flask import request, Response, url_for
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker.db_models.db_models import WalletModel
from spending_tracker.models.wallet import Wallet
from spending_tracker.resources.errormodels import create_error_model, create_error_response
from spending_tracker import api


single_user = Namespace(name='Wallet', description='Single user wallet')


MIMETYPE = "application/json"

schema_415 = create_error_model('Unsupported media type wallet', url='/api/<user>/money/', error="Unsupported media type",
                                message="Requests must be JSON")
schema_404 = create_error_model('Wallet not found', url='/api/<user>/money/', error="Not found", message='User: <user> was not found')

user_links = api.model('wallet links', {
    'self': fields.String(example='/api/users/<user>/money/'),
    'categories': fields.String('/api/categories/<user>/')
})

single_user_model = api.model('wallet control', {
    'properties': fields.Nested(WalletModel.get_schema()),
    'links': fields.Nested(user_links)
})


@single_user.route(f'/<string:user>/money/')
class WalletItem(Resource):
    @single_user.doc(description='Add money to users wallet')
    @single_user.expect(WalletModel.get_schema(single=True))
    @single_user.response(201, 'Created', headers={'Location': '/api/user/<user>/money/'})
    @single_user.response(404, description='User not found', model=schema_404)
    @single_user.response(415, description='Unsupported media type', model=schema_415)
    def post(self, user: str):
        if not request.json:
            create_error_response(415, title='Unsupported media type', message='Requests must be JSON')
        uri = url_for('api.Wallet_wallet_item', user=user)
        money = request.json['money']
        status = Wallet(user).add_money(money)
        return Response(
            status=status,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    @single_user.doc(description='Get money from users wallet')
    @single_user.response(200, description='Success', model=single_user_model)
    @single_user.response(404, description='User not found', model=schema_404)
    def get(self, user: str):
        resp = {}
        resp['properties'] = Wallet(user).balance()
        resp['links'] = {
            'self': url_for('api.Wallet_wallet_item', user=user),
            'categories': url_for('api.Categories_category_collection', user=user)
        }
        return Response(
            json.dumps(resp, indent=4), 200
        )