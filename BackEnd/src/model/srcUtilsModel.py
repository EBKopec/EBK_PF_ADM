from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime


bp_su = Blueprint('src_utils', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class src_utils(db.Model):
    type_file = db.Column(db.String(255), primary_key=True)
    src_utils = db.Column(db.String(255))
    src_utils_desc = db.Column(db.String(255))
    src_change_date = db.Column(db.DateTime)

    def __init__(self, type_file, src_utils, src_utils_desc, src_change_date):
        self.type_file = type_file
        self.src_utils = src_utils
        self.src_utils_desc = src_utils_desc
        self.src_change_date = src_change_date


@bp_su.route('/srcutils/<string:file>', methods=['GET'])
def srcUtils(file):
    query = db.session.query(src_utils.src_utils).filter(src_utils.type_file==file).first()
    result = Schema.src_utils_Schema.dump(query)
    db.session.close()
    return result
