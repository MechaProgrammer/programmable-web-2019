from flask import request, Response, url_for
from flask_restplus import Resource, fields, Namespace
from spending_tracker import api
import json


entry_point = Namespace(name='API Entry point', description='Api entry point')

MIMETYPE = "application/json"

entry_point_model = api.model('Entry point', {
    'users': fields.Url(example='/api/users/', absolute=True),
    'wallet': fields.Url(example='/api/user/money/', absolute=True),
    'categories': fields.Url(example='/api/categories/', absolute=True)
})


@entry_point.route('/')
@entry_point.doc(description='Get API entry points')
class EntryPoint(Resource):
    """API entry point"""
    @entry_point.response(200, description='Success', model=entry_point_model)
    def get(self):
        """Get resource endpoints"""
        resp = {
            'users': url_for('api.Users_user_collection'),
            'wallet': url_for('api.Wallet_wallet_item', user='model_user'),
            'categories': url_for('api.Categories_category_collection', user='model_user')
        }

        return Response(
            json.dumps(resp, indent=4),
            mimetype=MIMETYPE
        )
