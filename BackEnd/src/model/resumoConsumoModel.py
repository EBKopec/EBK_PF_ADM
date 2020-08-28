from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
import numpy as np
from schema import Schema


bp_rc = Blueprint('resumo_consumo', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class resumo_consumo(db.Model):
    mes_id	= db.Column(db.Integer, primary_key=True)
    group =	db.Column(db.String(255), primary_key=True)
    ramal_ativo	= db.Column(db.Integer)
    valor_ramal	= db.Column(db.Float(precision=2,  decimal_return_scale=None))
    parcial	= db.Column(db.Float(precision=2,  decimal_return_scale=None))
    faturar_ramais = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    franquias =	db.Column(db.Float(precision=2,  decimal_return_scale=None))
    excedentes = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    total_faturar = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    ldn_minutes	= db.Column(db.Float(precision=2,  decimal_return_scale=None))
    ldn_values = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    local_minutes = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    local_values = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    movel_minutes = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    movel_values = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    ldn_minutes_exc = db.Column(db.Float(precision='12.2',  decimal_return_scale='12.2'))
    ldn_values_exc = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    local_minutes_exc	= db.Column(db.Float(precision='12.2',  decimal_return_scale=2))
    local_values_exc = db.Column(db.Float(precision=2,  decimal_return_scale=2))
    movel_minutes_exc	= db.Column(db.FLOAT(precision='12.2', decimal_return_scale=2))
    movel_values_exc = db.Column(db.Float(precision=2,  decimal_return_scale=2))
    ldn_total_m	= db.Column(db.String(255))
    ldn_total_valor	= db.Column(db.Float(precision=2,  decimal_return_scale=None))
    local_total_m = db.Column(db.String(255))
    local_total_valor = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    movel_total_m = db.Column(db.String(255))
    movel_total_valor = db.Column(db.Float(precision=2,  decimal_return_scale=None))
    total = db.Column(db.Float(precision=2,  decimal_return_scale=None))

    def __init__(self, mes_id, group, ramal_ativo, valor_ramal, parcial,\
                    faturar_ramais, franquias, excedentes, total_faturar, ldn_minutes,\
                    ldn_values, local_minutes, local_values, movel_minutes, movel_values, ldn_minutes_exc,\
                    ldn_values_exc, local_minutes_exc, local_values_exc, movel_minutes_exc, movel_values_exc, ldn_total_m, \
                    ldn_total_valor, local_total_m, local_total_valor, movel_total_m, \
                    movel_total_valor, total ):
        self.mes_id = mes_id
        self.group = group
        self.ramal_ativo = ramal_ativo
        self.valor_ramal = valor_ramal
        self.parcial = parcial
        self.faturar_ramais = faturar_ramais
        self.franquias = franquias
        self.excedentes = excedentes
        self.total_faturar = total_faturar
        self.ldn_minutes = ldn_minutes
        self.ldn_values = ldn_values
        self.local_minutes = local_minutes
        self.local_values = local_values
        self.movel_minutes = movel_minutes
        self.movel_values = movel_values
        self.ldn_minutes_exc = ldn_minutes_exc
        self.ldn_values_exc = ldn_values_exc
        self.local_minutes_exc = local_minutes_exc
        self.local_values_exc = local_values_exc
        self.movel_minutes_exc = movel_minutes_exc
        self.movel_values_exc = movel_values_exc
        self.ldn_total_m = ldn_total_m
        self.ldn_total_valor = ldn_total_valor
        self.local_total_m = local_total_m
        self.local_total_valor = local_total_valor
        self.movel_total_m = movel_total_m
        self.movel_total_valor = movel_total_valor
        self.total = total



@bp_rc.route('/pmpg/total/<string:month_id>', methods=['GET'])
def getTotal(month_id):
    query = resumo_consumo.query.filter(resumo_consumo.mes_id == month_id).all()
    result = Schema.resume_Schema.dump(query)
    # print(dir(db.session))
    db.session.close()
    return jsonify(result)