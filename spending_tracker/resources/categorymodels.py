from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.db_models.db_models import CategoryModel
from spending_tracker.resources.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError
from spending_tracker.models.category import Category


category = Namespace(name='CategoryModel', description='WalletModel categories')


@category.route('/<string:user>/')
class CategoryCollection(Resource):
    @category.expect(CategoryModel.get_schema())
    def post(self, user):
        category_class = Category(user)
        resp = category_class.add_categories(request.json)
        return Response(resp)

    def get(self, user):
        user_categories = Category(user)
        resp = user_categories.get_categories()
        return Response(json.dumps(resp))
