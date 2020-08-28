from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime


bp_fat = Blueprint('fat', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

class vw_pmpgs(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_pmpg_0800s(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sme_cmeis(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sme_escolas(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sms_aih_0800s(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sms_aihs(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sms_pab_0800s(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


class vw_sms_pabs(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID	= db.Column(db.Integer)
    ID = db.Column(db.Integer)
    USER_ID	= db.Column(db.Integer)
    AGRUPAMENTO	= db.Column(db.String(255))
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.Time)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.Time)
    CUSTO = db.Column(db.Float)
    VALIDAR_AGRUPAMENTO	= db.Column(db.String(19))
    CHECAGEM_VALOR = db.Column(db.String(16))
    VALIDAR_HORA = db.Column(db.String(15))

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, ID, USER_ID, AGRUPAMENTO, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO, VALIDAR_AGRUPAMENTO, VALIDAR_HORA):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.ID = ID
        self.USER_ID = USER_ID
        self.AGRUPAMENTO = AGRUPAMENTO
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO = CUSTO
        self.VALIDAR_AGRUPAMENTO = VALIDAR_AGRUPAMENTO
        self.CHECAGEM_VALOR = CHECAGEM_VALOR
        self.VALIDAR_HORA = VALIDAR_HORA


@bp_fat.route('/faturamento/<int:group>/<int:month>/<int:page_num>', methods=['GET'])
def getFat(group,month,page_num):
    
    if group == 0:
        query = vw_pmpgs.query.filter(vw_pmpgs.MES_ID==month)
    
    if group == 1:
        query = vw_pmpg_0800s.query.filter(vw_pmpg_0800s.MES_ID==month)
    
    if group == 2:
        query = vw_sme_escolas.query.filter(vw_sme_escolas.MES_ID==month)
    
    if group == 3:
        query = vw_sme_cmeis.query.filter(vw_sme_cmeis.MES_ID==month)

    if group == 4:
        query = vw_sms_pabs.query.filter(vw_sms_pabs.MES_ID==month)
    
    if group == 5:
        query = vw_sms_pab_0800s.query.filter(vw_sms_pab_0800s.MES_ID==month)

    if group == 6:
        query = vw_sms_aihs.query.filter(vw_sms_aihs.MES_ID==month)
    
    if group == 7:
        query = vw_sms_aih_0800s.query.filter(vw_sms_aih_0800s.MES_ID==month)


    extensions = query

    pg = extensions.paginate(page=page_num).items
    total = []
    total_pages={}
    # total_pages['Total'] = (extensions.paginate(page=page_num).total)
    total_pages['Pages'] = (extensions.paginate(page_num).pages)
    total_pages['Current_Page'] = (extensions.paginate(page_num).page)

    result = Schema.vws_Schema.dump(pg)
    query.session.close()
    return jsonify({"docs":result,'Pages':total_pages})


