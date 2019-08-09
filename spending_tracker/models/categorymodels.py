from flask import request, Response
from flask_restplus import Resource, fields, Namespace
import json
from spending_tracker import db
from spending_tracker import api
from spending_tracker.models.errormodels import create_error_response, create_error_model
from sqlalchemy.exc import IntegrityError


category = Namespace(name='Category', description='Wallet categories')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    travel = db.Column(db.Float, unique=True, nullable=False)

    wallet = db.relationship('Wallet', back_populates="category")

    # entertainment = db.Column(db.Float, unique=True, nullable=False)
    # eating_out = db.Column(db.Float, unique=True, nullable=False)
    # house = db.Column(db.Float, unique=True, nullable=False)
    # bills = db.Column(db.Float, unique=True, nullable=False)
    # food = db.Column(db.Float, unique=True, nullable=False)

    @staticmethod
    def get_schema():
        category_model = api.model('Categories', {
            'travel': fields.Float(example=10, description='Travel expenses'),
        })
        return category_model
