from spending_tracker import db, api
from flask_restplus import fields


user_category = db.Table(
    "associnations",
    db.Column("category_model_id", db.Integer, db.ForeignKey('category_model.id'), primary_key=True),
    db.Column("wallet_model_id", db.Integer, db.ForeignKey('wallet_model.id'), primary_key=True),
 )


class UserModel(db.Model):
    """Database model for user"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(32), unique=True, nullable=False)

    wallets = db.relationship("WalletModel", back_populates='user_model', cascade='delete, delete-orphan')

    @staticmethod
    def get_schema() -> object:
        """Schema for database User"""
        user_model = api.model('User', {
            'user': fields.String(example='model user', description='Username', required=True),
        })
        return user_model


class WalletModel(db.Model):
    """Database model for wallet"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), unique=True)
    money = db.Column(db.Integer, nullable=False)

    categories = db.relationship("CategoryModel", cascade='delete, delete-orphan')

    user_model = db.relationship("UserModel", back_populates='wallets')

    @staticmethod
    def get_schema(single=False) -> object:
        """Schema for database Wallet

        args:
            single (bool): if True, returns only money
        Returns:
            object: Model object
        """
        if not single:
            wallet_model = api.model('Wallet', {
                "user": fields.String(description='User name', required=True),
                "money": fields.Float(description='Money to wallet', required=True)
            })
        else:
            wallet_model = api.model('Wallet money', {
                "money": fields.Float(description='Money to wallet', required=True)
            })
        return wallet_model


class CategoryModel(db.Model):
    """Database model for Category"""
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet_model.id"), unique=True)
    travel = db.Column(db.Float, nullable=True)
    entertainment = db.Column(db.Float, nullable=True)
    eating_out = db.Column(db.Float, nullable=True)
    house = db.Column(db.Float, nullable=True)
    bills = db.Column(db.Float, nullable=True)
    food = db.Column(db.Float, nullable=True)

    wallet = db.relationship('WalletModel')

    def __repr__(self):
        return ['travel', 'entertainment', 'eating_out', 'house', 'bills', 'food']

    @staticmethod
    def get_schema(user=False) -> object:
        """Schema for database Wallet

        args:
            user (bool): If True, user is not included in the model
        Returns:
            object: Model object
        """
        category_model = api.model('Category', {
            'travel': fields.Float(example=10, description='Travel expenses'),
            'entertainment': fields.Float(example=10, description='Entertainment expenses'),
            'eating_out': fields.Float(example=10, description='Eating out expenses'),
            'house': fields.Float(example=10, description='House expenses'),
            'bills': fields.Float(example=10, description='Bills expenses'),
            'food': fields.Float(example=10, description='Food expenses'),
        })
        if not user:
            user_model = api.model('Category user', {
                'user': fields.String(example='Model user', required=True),
                'categories': fields.Nested(category_model)
            })
        else:
            user_model = api.model('Category categories', {
                'categories': fields.Nested(category_model, required=True)
            })
        return user_model


