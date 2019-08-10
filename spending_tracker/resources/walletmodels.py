from flask import request, Response, url_for
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import api
from spending_tracker.db_models.db_models import WalletModel
from spending_tracker.models.wallet import Wallet
from spending_tracker.utils.helpers import schema_builder, SchemeBuilder
from spending_tracker.resources.errormodels import create_error_model


single_user = Namespace(name='User', description='Single user controls')


MIMETYPE = "application/json"

schema_415 = create_error_model('Unsupported media type wallet', url='/api/<user>/money/', error="Unsupported media type",
                                message="Requests must be JSON")


@single_user.route(f'/<string:user>/money/')
class WalletItem(Resource):
    @single_user.doc(description='Add money to users wallet')
    @single_user.expect(WalletModel.get_schema())
    @single_user.response(201, 'Created', headers={'Location': '/api/<user>/money/'})
    @single_user.response(415, description='Unsupported media type', model=schema_415)
    def post(self, user: str):
        uri = url_for('api.User_wallet_item', user=user)
        money = request.json['money']
        status = Wallet(user).add_money(money)
        return Response(
            status=status,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    @single_user.doc(description='Get money from users wallet')
    @single_user.response(200, description='Success', model=schema_builder(WalletModel, 'self', '/api/user/<user>/money/'))
    def get(self, user: str):
        resp = Wallet(user).balance()
        return Response(
            json.dumps(resp), 200
        )