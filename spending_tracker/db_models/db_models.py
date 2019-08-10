from spending_tracker import db
from flask_restplus import fields
from spending_tracker import api


user_category = db.Table(
    "associnations",
    db.Column("category_model_id", db.Integer, db.ForeignKey('category_model.id'), primary_key=True),
    db.Column("wallet_model_id", db.Integer, db.ForeignKey('wallet_model.id'), primary_key=True),
 )


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    wallets = db.relationship("WalletModel", back_populates='user_model')

    @staticmethod
    def get_schema():
        user_model = api.model('User', {
            'user': fields.String(example='model user', description='Username', required=True),
            'balance': fields.Float(example=133, description='Account balance in euros', required=True),
        })
        return user_model


class WalletModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), unique=True)
    money = db.Column(db.Integer, nullable=False)

    categories = db.relationship("CategoryModel", secondary='associnations', back_populates='wallet')
    user_model = db.relationship("UserModel", back_populates='wallets')

    @staticmethod
    def get_schema():
        wallet_model = api.model('Wallet', {
            "money": fields.Integer()
        })
        return wallet_model


class CategoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet_model.id"))
    travel = db.Column(db.Float, nullable=True)
    entertainment = db.Column(db.Float, nullable=True)
    eating_out = db.Column(db.Float, nullable=True)
    house = db.Column(db.Float, nullable=True)
    bills = db.Column(db.Float, nullable=True)
    food = db.Column(db.Float, nullable=True)

    wallet = db.relationship('WalletModel', secondary='associnations', back_populates="categories")


    @staticmethod
    def get_schema():
        category_model = api.model('Category', {
            'travel': fields.Float(example=10, description='Travel expenses'),
            'entertainment': fields.Float(example=10, description='Entertainment expenses'),
            'eating_out': fields.Float(example=10, description='Eating out expenses'),
            'house': fields.Float(example=10, description='House expenses'),
            'bills': fields.Float(example=10, description='Bills expenses'),
            'food': fields.Float(example=10, description='Food expenses'),
        })
        return category_model
