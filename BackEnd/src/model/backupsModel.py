from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from administration import administrationExtensions

bp_bg = Blueprint('faturamento', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db    
    
class faturamento(db.Model):
    MES_FATURAMENTO_ID = db.Column(db.Integer, primary_key=True)
    MES_ID = db.Column(db.Integer)
    FATURAMENTO_ID = db.Column(db.Integer)
    BATCH_ID = db.Column(db.Integer)
    TIPO = db.Column(db.String(255))
    ORIGEM = db.Column(db.String(255))
    DATA = db.Column(db.Date)
    HORA = db.Column(db.TIME)
    DESTINO = db.Column(db.String(255))
    CIDADE_DESTINO = db.Column(db.String(255))
    DURACAO_REAL = db.Column(db.TIME)
    CUSTO_ORIGINAL = db.Column(db.Float)
    CUSTO = db.Column(db.Float)
    USER_ID = db.Column(db.Integer)
    USER_DESC = db.Column(db.String(255))
    DISTRIBUTOR_ID = db.Column(db.Integer)

    def __init__(self, MES_FATURAMENTO_ID, MES_ID, FATURAMENTO_ID, BATCH_ID, TIPO, ORIGEM, DATA, HORA, DESTINO, CIDADE_DESTINO, DURACAO_REAL, CUSTO_ORIGINAL, CUSTO, USER_ID, USER_DESC, DISTRIBUTOR_ID):
        self.MES_FATURAMENTO_ID = MES_FATURAMENTO_ID
        self.MES_ID = MES_ID
        self.FATURAMENTO_ID = FATURAMENTO_ID
        self.BATCH_ID = BATCH_ID
        self.TIPO = TIPO
        self.ORIGEM = ORIGEM
        self.DATA = DATA
        self.HORA = HORA
        self.DESTINO = DESTINO
        self.CIDADE_DESTINO = CIDADE_DESTINO
        self.DURACAO_REAL = DURACAO_REAL
        self.CUSTO_ORIGINAL = CUSTO_ORIGINAL
        self.CUSTO = CUSTO
        self.USER_ID = USER_ID
        self.USER_DESC = USER_DESC
        self.DISTRIBUTOR_ID = DISTRIBUTOR_ID


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


@bp_bg.route('/backup', methods=['GET'])
def getBackups():
    query = db.session.query( faturamento.MES_ID
                            , db.func.count(faturamento.MES_FATURAMENTO_ID).label('QTY'))\
                       .group_by(faturamento.MES_ID).all()
    result = Schema.backups_Schema.dump(query)
    db.session.close()
    return jsonify(result)

@bp_bg.route('/backup/<int:mes>', methods=['GET'])
def backupGroups(mes):
    adm = administrationExtensions()
    query = adm.backUpBilling(mes)
    result = "Backup Done %s " % mes
    db.session.close()
    return jsonify({"Backup":result})


@bp_bg.route('/backupDone/<int:page_num>', methods=['GET'])
def getFec(page_num):
    query = vw_fechamento.query.filter(vw_fechamento.table_schema=='novafibra')\
                               .filter(vw_fechamento.table_name.like("%faturamento_%"))
    
    pg = query.paginate(page=page_num).items
    total_pages={}
    total_pages['Pages'] = (query.paginate(page_num).pages)
    total_pages['Current_Page'] = (query.paginate(page_num).page)

    result = Schema.backupDone_Schema.dump(pg)
    # print(dir(query.session))
    # db.engine.dispose()
    query.session.close()
    return jsonify({'Data':result, 'Info':total_pages})