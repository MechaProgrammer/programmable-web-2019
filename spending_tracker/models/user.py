from spending_tracker.db_models.db_models import UserModel
from spending_tracker.resources.walletmodels import WalletItem
from spending_tracker.resources.categorymodels import CategoryCollection
from spending_tracker.resources.errormodels import create_error_response


class User:
    def retrieve_user(self, user):
        db_user = UserModel.query.filter_by(user=user).first()
        if db_user is None:
            return create_error_response(404, "Not found", f'User: {user} was not found')
        resp = {
            'user': db_user.user,
            'balance': db_user.balance,
        }
        return resp

    def retrive_all(self):
        return UserModel.query.all()


