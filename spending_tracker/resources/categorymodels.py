from flask import request, Response, url_for
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker.db_models.db_models import CategoryModel
from spending_tracker.resources.errormodels import create_error_model
from spending_tracker.models.category import Category
from spending_tracker import api


category = Namespace(name='Categories', description='Wallet categories')


user_links = api.model('user links', {
    'self': fields.String(example='/api/users/<user>/'),
    'collection': fields.String('/api/users/'),
    'wallet': fields.String('/api/user/<user>/money/'),
    'categories': fields.String('/api/categories/<user>/')
})

single_user_model = api.model('User categories', {
    'properties': fields.Nested(CategoryModel.get_schema()),
    'links': fields.Nested(user_links)
})

schema_404 = create_error_model(
    'Category user not found',
    url='/api/categories/<user>/',
    error="Not found",
    message='User: <user> was not found'
)

schema_400 = create_error_model(
    'Category does not exists',
    url='/api/categories/<user>/',
    error="Bad Request",
    message='Category <category> does not exists'
)


@category.route('/<string:user>/')
class CategoryCollection(Resource):
    @category.doc(description='Add spending categories')
    @category.expect(CategoryModel.get_schema(user=True), validate=True)
    @category.response(201, description='Created', model=user_links)
    @category.response(404, description='Not found', model=schema_404)
    @category.response(400, description='Bad Request', model=schema_400)
    def post(self, user):
        category_class = Category(user)
        resp = category_class.add_categories(request.json)
        return Response(status=resp)

    @category.doc(description='Get spending categories')
    @category.response(200, description='Success', model=single_user_model)
    @category.response(404, description='Not found', model=schema_404)
    def get(self, user):
        user_categories = Category(user)
        resp = {'properties': user_categories.get_categories(), 'links': {
            'self': url_for('api.Users_user_resource', user=user),
            'collection': url_for('api.Categories_category_collection', user=user),
            'wallet': url_for('api.Wallet_wallet_item', user=user),
            'categories': url_for('api.Categories_category_collection', user=user)
        }}
        return Response(json.dumps(resp, indent=4))
