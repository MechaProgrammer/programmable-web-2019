from flask import request, Response
import json
from models import api
from flask_restplus import fields


MIMETYPE = "application/json"


def create_error_response(status_code, title, message):
    resource_url = request.path
    resp = dict(
        url=resource_url,
        error=title,
        message=message
    )
    return Response(json.dumps(resp), status_code, mimetype=MIMETYPE)


error_model = api.model(
    'Error model',
    {
        'url': fields.String(example='/api/users/<user>/'),
        'error': fields.String(example='Not found'),
        'message': fields.String(example='User: <user> was not found'),
    }
)