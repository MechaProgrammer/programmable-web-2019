from flask import request, Response
from flask_restplus import Resource, fields, Namespace
from spending_tracker.db_models.db_models import UserItem
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import Category
from spending_tracker.models.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError


category = Namespace(name='Category', description='Wallet categories')


@category.route('/<string:user>/')
class CategoryCollection(Resource):
    @category.expect(Category.get_schema())
    def post(self, user):
        db_user = UserItem.query.filter_by(user=user).first()
        categories = Category(
            wallet_id=db_user.wallets[0].id,
            travel=request.json['travel']
        )
        db.session.add(categories)
        db.session.commit()
        return Response(201)

    def get(self, user):
        db_user = UserItem.query.filter_by(user=user).first()
        user_wallet = db_user.wallets[0]
        categories = Category.query.filter_by(wallet_id=user_wallet.id).first()
        resp = dict(
            user=db_user.user,
            categories=dict(travel=categories.travel)
        )
        return Response(json.dumps(resp))
