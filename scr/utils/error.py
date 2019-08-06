from flask import request, Response, jsonify, current_app
import json
from scr.models import api
from flask_restplus import fields
from sqlalchemy.exc import IntegrityError


MIMETYPE = "application/json"


def create_error_response(status_code, title, message, **kwargs):
    resource_url = request.path
    resp = dict(
        url=resource_url,
        error=title,
        message=message
    )
    for i in kwargs:
        resp[i] = kwargs[i]
    return Response(json.dumps(resp), status_code, mimetype=MIMETYPE)


error_model = api.model(
    'Error model',
        {
            'url': fields.String(example='/api/users/<user>/'),
            'error': fields.String(example='Not found'),
            'message': fields.String(example='User: <user> was not found'),
        }
)


def create_error_model(model_name, **kwargs):
    modeli = {}
    for args in kwargs:
        modeli[args] = fields.String(example=kwargs[args])
    error_model = api.model(
        model_name,
            modeli
    )
    return error_model
