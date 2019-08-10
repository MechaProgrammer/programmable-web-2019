from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import WalletModel, UserModel
from spending_tracker.utils.money_handler import money_add
from spending_tracker.models.wallet import Wallet


single_user = Namespace(name='User', description='Single user controls')


MIMETYPE = "application/vnd.collection+json"


@single_user.route(f'/<string:user>/money/')
class WalletItem(Resource):
    @single_user.doc(description='Add money to users wallet')
    @single_user.expect(WalletModel.get_schema())
    def post(self, user):
        uri = api.url_for(WalletItem, user=user)
        money = request.json['money']
        status = Wallet(user, money).create()
        return Response(
            status=status,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    @single_user.doc(description='Get money from users wallet')
    def get(self, user):
        user_name = UserModel.query.filter_by(user=user).first()
        user_wallet = user_name.wallets
        resp = dict(
            user=user_name.user,
            wallet=user_wallet[0].money
        )
        return Response(
            json.dumps(resp), 200
        )