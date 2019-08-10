from spending_tracker.db_models.db_models import UserModel
from spending_tracker.db_models.db_models import CategoryModel
from spending_tracker import db
from spending_tracker.resources.errormodels import create_error_response


class Category:
    def __init__(self, user):
        self.user = user

    def add_categories(self, categories):
        db_user = UserModel.query.filter_by(user=self.user).first()
        categories_all = CategoryModel(
            wallet_id=db_user.wallets[0].id,
            travel=categories['travel'],
            entertainment=categories['entertainment'],
            eating_out=categories['eating_out'],
            house=categories['house'],
            bills=categories['bills'],
            food=categories['food'],
        )
        db.session.add(categories_all)
        db.session.commit()
        return 201

    def get_categories(self):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user.wallets:
            user_wallet = db_user.wallets[0]
        else:
            create_error_response(404, title='Not found', message='User has no wallet')
        categories = CategoryModel.query.filter_by(wallet_id=user_wallet.id).first()
        if categories is not None:
            resp = dict(
                user=db_user.user,
                categories=dict(travel=categories.travel)
            )
            return resp
        else:
            create_error_response(404, title='Not found', message='User wallet has no categories')
