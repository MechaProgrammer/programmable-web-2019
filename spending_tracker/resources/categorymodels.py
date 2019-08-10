from flask import request, Response
from flask_restplus import Resource, fields, Namespace
from spending_tracker.db_models.db_models import UserModel
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import CategoryModel
from spending_tracker.resources.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError


category = Namespace(name='CategoryModel', description='WalletModel categories')


@category.route('/<string:user>/')
class CategoryCollection(Resource):
    @category.expect(CategoryModel.get_schema())
    def post(self, user):
        db_user = UserModel.query.filter_by(user=user).first()
        categories = CategoryModel(
            wallet_id=db_user.wallets[0].id,
            travel=request.json['travel'],
            entertainment=request.json['entertainment'],
            eating_out=request.json['eating_out'],
            house=request.json['house'],
            bills=request.json['bills'],
            food=request.json['food'],
        )
        db.session.add(categories)
        db.session.commit()
        return Response(201)

    def get(self, user):
        db_user = UserModel.query.filter_by(user=user).first()
        user_wallet = db_user.wallets[0]
        categories = CategoryModel.query.filter_by(wallet_id=user_wallet.id).first()
        resp = dict(
            user=db_user.user,
            categories=dict(travel=categories.travel)
        )
        return Response(json.dumps(resp))
