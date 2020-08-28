from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify, send_file, send_from_directory, safe_join, make_response
from flask_restful import Resource, Api
from model.srcUtilsModel import bp_su, configure, srcUtils
from io import BytesIO
from schema import Schema
from utils import utils
import datetime
import os
from os.path import basename
import time
import zipfile

bp_xls = Blueprint('excel', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


@bp_xls.route('/download/<string:period>&<string:type_file>', methods=['GET'])
def fl_excel(period,type_file):
    base_root = srcUtils(str(type_file)).get('src_utils')
    FOLDER = os.path.join(base_root,period)
    resp = send_from_directory( FOLDER , filename='Files_'+str(period)+'.zip', as_attachment=True)
    response = make_response(resp)
    response.headers.set('Content-Type', 'application/octet-stream')
    # response.headers.set('responseType', 'stream')
    response.headers.set('Content-Disposition', 'attachment', filename='Files_'+period+'.zip')
    return response
    

