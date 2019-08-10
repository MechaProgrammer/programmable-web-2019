from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import api
from spending_tracker.db_models.db_models import WalletModel
from spending_tracker.models.wallet import Wallet


single_user = Namespace(name='User', description='Single user controls')


MIMETYPE = "application/json"


@single_user.route(f'/<string:user>/money/')
class WalletItem(Resource):
    @single_user.doc(description='Add money to users wallet')
    @single_user.expect(WalletModel.get_schema())
    def post(self, user):
        uri = api.url_for(WalletItem, user=user)
        money = request.json['money']
        status = Wallet(user).add_money(money)
        return Response(
            status=status,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    @single_user.doc(description='Get money from users wallet')
    def get(self, user):
        resp = Wallet(user).balance()
        return Response(
            json.dumps(resp), 200
        )