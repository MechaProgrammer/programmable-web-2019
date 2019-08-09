from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import Wallet, UserItem
from spending_tracker.models.usermodels import User
# from spending_tracker.models.categorymodels import Category
from spending_tracker.models.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError


single_user = Namespace(name='User', description='Single user controls')


MIMETYPE = "application/vnd.collection+json"


# class Wallet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user_item.id"))
#     #category = db.Column(db.String, nullable=False)
#     value = db.Column(db.Integer, unique=True, nullable=False)
#
#     #user = db.relationship("user_item", back_populates='wallet')
#     category = db.relationship("Category", back_populates='wallet')
#     # travel = db.relationship('Travel', back_populates="Wallet")
#
#     @staticmethod
#     def get_schema():
#         wallet_model = api.model('Wallet', {
#             'category': fields.Nested(Category.get_schema()),
#         })
#         return wallet_model


@single_user.route(f'/<string:user>/wallet/')
class WalletItem(Resource):
    @single_user.expect(Wallet.get_schema())
    def post(self, user):
        db_user = UserItem.query.filter_by(user=user).first()
        #uri = api.url_for(Wallet)
        uri = 'asd'
        walletti = Wallet(
            user=db_user.id,
            money=request.json['money']
            #category=request.json['category'],
            #amount=request.json['amount']
        )
        db.session.add(walletti)
        db.session.commit()
        return Response(
            status=201,
            mimetype=MIMETYPE,
            headers={'self': f'{uri}'})

    def get(self, user):
        user_name = UserItem.query.filter_by(user=user).first()
        print(user_name)
        resp = dict(
            user=user_name.user,
            wallet=Wallet.query.filter_by(user=user_name.id).first().money
        )
        return Response(
            json.dumps(resp), 200
        )