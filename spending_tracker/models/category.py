from spending_tracker.db_models.db_models import UserModel
from spending_tracker.db_models.db_models import CategoryModel
from spending_tracker import db
from spending_tracker.resources.errormodels import create_error_response
from spending_tracker.utils.money_handler import money_add, money_subtract


class Category:
    def __init__(self, user):
        self.user = user

    def add_categories(self, categories):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user is None:
            create_error_response(404, title='Not found', message=f'User {self.user} was not found')
        wallet_id = db_user.wallets[0].id
        category_model = CategoryModel.query.filter_by(wallet_id=wallet_id).first()
        if category_model is None:
            category_model = CategoryModel()
            category_model.wallet_id = wallet_id
        for k, v in categories['categories'].items():
            try:
                if v >= 0:
                    setattr(category_model, k, money_add(getattr(category_model, k), v))
                else:
                    setattr(category_model, k, money_subtract(getattr(category_model, k), v))
            except AttributeError:
                create_error_response(400, title='Bad Request', message=f'Category {k} does not exists')

        db.session.add(category_model)
        db.session.commit()
        return 200

    def get_categories(self):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user is None:
            create_error_response(404, title='Not found', message=f'User {self.user} was not found')
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
