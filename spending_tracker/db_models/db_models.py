from spending_tracker import db
from flask_restplus import Resource, fields, Namespace
from spending_tracker import api


user_category = db.Table(
    "associnations",
    db.Column("category_id", db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column("wallet_id", db.Integer, db.ForeignKey('wallet.id'), primary_key=True),
 )


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    wallets = db.relationship("Wallet", back_populates='user_item')
    #categories = db.relationship("Category", secondary='associnations', back_populates='user_item')

    @staticmethod
    def get_schema():
        user_model = api.model('User', {
            'user': fields.String(example='model user', description='Username', required=True),
            'balance': fields.Float(example=133, description='Account balance in euros', required=True),
        })
        return user_model


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_item.id"), unique=True)
    money = db.Column(db.Integer, nullable=False)

    categories = db.relationship("Category", secondary='associnations', back_populates='wallet')
    user_item = db.relationship("UserItem", back_populates='wallets')

    @staticmethod
    def get_schema():
        wallet_model = api.model('Wallet', {
            "money": fields.Integer()
        })
        return wallet_model


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"))
    travel = db.Column(db.Float, unique=True, nullable=True)
    entertainment = db.Column(db.Float, unique=True, nullable=True)
    eating_out = db.Column(db.Float, unique=True, nullable=True)
    house = db.Column(db.Float, unique=True, nullable=True)
    bills = db.Column(db.Float, unique=True, nullable=True)
    food = db.Column(db.Float, unique=True, nullable=True)

    wallet = db.relationship('Wallet', secondary='associnations', back_populates="categories")


    @staticmethod
    def get_schema():
        category_model = api.model('Categories', {
            'travel': fields.Float(example=10, description='Travel expenses'),
        })
        return category_model
