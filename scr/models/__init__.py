from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(
    blueprint,
    title='Money saving app',
    version='0.1',
    description='Save money by using this app!'
)
