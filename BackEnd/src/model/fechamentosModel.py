from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime

bp_fec = Blueprint('vw_fechamento', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

class vw_fechamento(db.Model):
    table_name = db.Column(db.String(255), primary_key=True)
    table_schema = db.Column(db.String(255))
    table_rows = db.Column(db.String(255))
    create_time = db.Column(db.String(255))

    def __init__(self, table_schema, table_name, table_rows, create_time):
        self.table_schema = table_schema
        self.table_name = table_name
        self.table_rows = table_rows
        self.create_time = create_time


@bp_fec.route('/backupDone/<int:page_num>', methods=['GET'])
def getFec(page_num):
    query = vw_fechamento.query.filter(vw_fechamento.table_schema=='novafibra')\
                               .filter(vw_fechamento.table_name.like("%faturamento_%"))
    
    pg = query.paginate(page=page_num).items
    total_pages={}
    total_pages['Pages'] = (query.paginate(page_num).pages)
    total_pages['Current_Page'] = (query.paginate(page_num).page)

    result = Schema.vwfechamento_Schema.dump(pg)
    return jsonify({'Data':result, 'Info':total_pages})