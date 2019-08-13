from spending_tracker.db_models.db_models import UserModel, WalletModel, CategoryModel
from spending_tracker.resources.errormodels import create_error_response
from spending_tracker.cli import db


class User:
    def retrieve_user(self, user: str) -> dict:
        """Query user from the database

        args:
            user (str): Users name
        Returns:
            dict: Users name and balance
        """
        db_user = UserModel.query.filter_by(user=user).first()
        if db_user is None:
            create_error_response(404, "Not found", f'User: {user} was not found')
        resp = {
            'user': db_user.user,
            'balance': db_user.balance,
        }
        return resp

    def retrive_all(self) -> list:
        """Query all users from the database"""
        return UserModel.query.all()

    def create(self, payload: dict) -> None:
        """Create user

        args:
            payload (dict): Dict for creating the user
        """
        user = UserModel(
            user=payload['user'],
            balance=payload['balance']
        )
        db.session.add(user)
        db.session.commit()

    def delete(self, user: str) -> None:
        """Delete user and its items from the database

        args:
            user (str): Users name
        """
        db_user = UserModel.query.filter_by(user=user).first()
        if db_user is None:
            return create_error_response(404, "Not found", f'User: {user} was not found')
        db.session.delete(db_user)
        db.session.commit()


