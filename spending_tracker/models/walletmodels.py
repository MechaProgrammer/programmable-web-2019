from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import Wallet, UserItem
from spending_tracker.utils.money_handler import money_add


single_user = Namespace(name='User', description='Single user controls')


MIMETYPE = "application/vnd.collection+json"


@single_user.route(f'/<string:user>/money/')
class WalletItem(Resource):
    @single_user.doc(description='Add money')
    @single_user.expect(Wallet.get_schema())
    def post(self, user):
        uri = api.url_for(WalletItem, user=user)
        db_user = UserItem.query.filter_by(user=user).first()
        if db_user.wallets:
            db_user.wallets[0].money = money_add(
                db_user.wallets[0].money,
                request.json['money']
            )
        else:
            walletti = Wallet(
                user=db_user.id,
                money=request.json['money']
            )
            db.session.add(walletti)
        db.session.commit()
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    def get(self, user):
        user_name = UserItem.query.filter_by(user=user).first()
        user_wallet = user_name.wallets
        resp = dict(
            user=user_name.user,
            wallet=user_wallet[0].money
        )
        return Response(
            json.dumps(resp), 200
        )