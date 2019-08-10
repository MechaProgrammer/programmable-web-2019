from spending_tracker import db
from spending_tracker.db_models.db_models import WalletModel, UserModel
from spending_tracker.utils.money_handler import money_add


class Wallet:
    def __init__(self, user, money):
        self.user = user
        self.money = money

    def create(self):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user.wallets:
            db_user.wallets[0].money = money_add(
                db_user.wallets[0].money,
                self.money
            )
        else:
            wallet_model = WalletModel(
                user_id=db_user.id,
                money=self.money
            )
            db.session.add(wallet_model)
        db.session.commit()
        return 201
