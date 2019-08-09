from spending_tracker import db
from flask_restplus import Resource, fields, Namespace
from spending_tracker import api


class UserItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    #wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"))

    wallets = db.relationship("Wallet", back_populates='user_item')

    @staticmethod
    def get_schema():
        user_model = api.model('User', {
            'user': fields.String(example='model user', description='Username', required=True),
            'balance': fields.Float(example=133, description='Account balance in euros', required=True),
        })
        return user_model


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user_item.id"))
    money = db.Column(db.Integer, nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey("user_item.id"))
    #category = db.Column(db.String, nullable=False)
    # value = db.Column(db.Integer, unique=True, nullable=False)

    user_item = db.relationship("UserItem", back_populates='wallets')
    #category = db.relationship("Category", back_populates='wallet')
    # travel = db.relationship('Travel', back_populates="Wallet")

    @staticmethod
    def get_schema():
        wallet_model = api.model('Wallet', {
            #'category': fields.Nested(Category.get_schema()),
            "money": fields.Integer()
        })
        return wallet_model


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel = db.Column(db.Float, unique=True, nullable=False)

    #wallet = db.relationship('Wallet', back_populates="category")

    # entertainment = db.Column(db.Float, unique=True, nullable=False)
    # eating_out = db.Column(db.Float, unique=True, nullable=False)
    # house = db.Column(db.Float, unique=True, nullable=False)
    # bills = db.Column(db.Float, unique=True, nullable=False)
    # food = db.Column(db.Float, unique=True, nullable=False)

    @staticmethod
    def get_schema():
        category_model = api.model('Categories', {
            'travel': fields.Float(example=10, description='Travel expenses'),
        })
        return category_model
