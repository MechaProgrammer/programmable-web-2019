from spending_tracker.db_models.db_models import UserModel, CategoryModel, WalletModel
from spending_tracker.cli import db
from spending_tracker.resources.errormodels import create_error_response
from spending_tracker.utils.money_handler import money_add, money_subtract
from spending_tracker.models.wallet import Wallet


class Category:
    def __init__(self, user):
        self.user = user

    def validate_balance(self, user_id, categories):
        wallet = WalletModel.query.filter_by(user_id=user_id).first()
        balance = wallet.money
        print(balance)
        print(categories)
        total_spending = 0
        for k, v in categories['categories'].items():
            total_spending += money_add(total_spending, v)
        if balance < total_spending:
            create_error_response(
                400, title='User does not have enough money', message=f'User {self.user} does no have enough money'
            )
        return total_spending

    def subtract_balance(self, balance):
        wallet = Wallet(self.user)
        resp = wallet.add_money(balance, subtract=True)
        if resp == 201:
            return True

    def add_categories(self, categories: dict) -> int:
        """Add categories to database.

        Returns:
            int: Status code 200 if success, else aborts
        """
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user is None:
            create_error_response(404, title='Not found', message=f'User {self.user} was not found')

        spending = self.validate_balance(db_user.id, categories)
        self.subtract_balance(spending)

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

    def change_category_values(self, categories: dict):
        db_user = UserModel.query.filter_by(user=self.user).first()
        if db_user is None:
            create_error_response(404, title='Not found', message=f'User {self.user} was not found')
        wallet_id = db_user.wallets[0].id
        category_model = CategoryModel.query.filter_by(wallet_id=wallet_id).first()
        if category_model is None:
            create_error_response(404, title='Not found', message='Categories not found')
        for k, v in categories['categories'].items():
            if k in repr(category_model):
                continue
            else:
                create_error_response(400, title='Bad Request', message=f'Category {k} does not exists')
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

    def get_categories(self) -> dict:
        """Query categories from db
        Returns:
            dict: Result dict
            else returns error response to api
        """
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
                categories=dict(
                    travel=categories.travel,
                    entertainment=categories.entertainment,
                    eating_out=categories.eating_out,
                    house=categories.house,
                    bills=categories.bills,
                    food=categories.food
                )
            )
            return resp
        else:
            create_error_response(404, title='Not found', message='User wallet has no categories')
