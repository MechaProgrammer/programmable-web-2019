from spending_tracker import db
from spending_tracker.db_models.db_models import WalletModel, UserModel
from spending_tracker.utils.money_handler import money_add
from spending_tracker.resources.errormodels import create_error_response


class Wallet:
    def __init__(self, user):
        self.user = user

    def add_money(self, money):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user.wallets:
            db_user.wallets[0].money = money_add(
                db_user.wallets[0].money,
                money
            )
        else:
            wallet_model = WalletModel(
                user_id=db_user.id,
                money=money
            )
            db.session.add(wallet_model)
        db.session.commit()
        return 201

    def balance(self):
        user_name = UserModel.query.filter_by(user=self.user).first()
        if user_name is None:
            create_error_response(404, title='Not found', message=f'User {user_name} was not found')
        user_wallet = user_name.wallets[0]
        resp = dict(
            user=user_name.user,
            wallet=user_wallet.money
        )
        return resp
