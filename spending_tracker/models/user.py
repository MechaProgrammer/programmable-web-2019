from spending_tracker.db_models.db_models import UserModel, WalletModel, CategoryModel
from spending_tracker.resources.errormodels import create_error_response
from spending_tracker.cli import db
from flask_restplus import abort
from flask import url_for


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
        }
        return resp

    def retrive_all(self) -> list:
        """Query all users from the database"""
        try:
            all_users = UserModel.query.all()
            if not all_users:
                create_error_response(404, "Users not found", f'There is no users in the database')
            else:
                return all_users
        except Exception as e:
            create_error_response(404, "Users not found", f'There is no users in the database')

    def create(self, payload: dict) -> None:
        """Create user

        args:
            payload (dict): Dict for creating the user
        """
        user = UserModel(
            user=payload['user'],
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


