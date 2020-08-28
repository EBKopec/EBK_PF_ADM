from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime


bp_am = Blueprint('ano', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class ano(db.Model):
    id_ano = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.String(255))

    def __init__(self, id_ano, ano):
        self.id_ano = id_ano
        self.ano = ano

@bp_am.route('/ano', methods=['GET'])
def getAno():
    per_page = 10
    query = db.session.query(ano)
    years= {}
    years = query.paginate(per_page=per_page).items
    result = Schema.anoMes_Schema.dump(years)
    db.session.close()
    return jsonify(result)



class mes(db.Model):
    id_mes = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(255))

    def __init__(self, id_ano, ano):
        self.id_mes = id_mes
        self.mes = mes

@bp_am.route('/mes', methods=['GET'])
def getMes():
    query = db.session.query(mes).all()
    result = Schema.anoMes_Schema.dump(query)
    db.session.close()
    return jsonify(result)