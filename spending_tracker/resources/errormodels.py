from flask import request
from spending_tracker import api
from flask_restplus import fields, abort


MIMETYPE = "application/json"


def create_error_response(status_code: int, title: str, message: str, url=None, **kwargs) -> None:
    """Create error response
    Abort with given status code.
    """
    if not url:
        resource_url = request.path
    else:
        resource_url = url
    resp = dict(
        url=resource_url,
        error=title,
        message=message
    )
    for i in kwargs:
        resp[i] = kwargs[i]
    abort(status_code, url=resource_url, error=title, message=message)


error_model = api.model(
    'Error model',
        {
            'url': fields.String(example='/api/users/<user>/'),
            'error': fields.String(example='Not found'),
            'message': fields.String(example='User: <user> was not found'),
        }
)


def create_error_model(model_name: str, **kwargs) -> object:
    """Create error API model."""
    modeli = {}
    for args in kwargs:
        modeli[args] = fields.String(example=kwargs[args])
    error_model = api.model(
        model_name,
            modeli
    )
    return error_model
