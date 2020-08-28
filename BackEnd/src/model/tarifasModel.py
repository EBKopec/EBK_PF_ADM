from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from model import controleAgrupamentoModel
import datetime

bp_tx = Blueprint('tarifas', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db

USERS = controleAgrupamentoModel.Users
TARIFA = controleAgrupamentoModel.Tarifa


class TIPO_LIGACAO(db.Model):
    TIPO_ID = db.Column(db.Integer, primary_key=True)
    TIPO_DESC = db.Column(db.String(255))
    DATA_ALTERACAO = db.Column(db.Date)

    def __init__(self, TIPO_ID, TIPO_DESC, DATA_ALTERACAO):
        self.TIPO_ID = TIPO_ID
        self.TIPO_DESC = TIPO_DESC
        self.DATA_ALTERACAO = DATA_ALTERACAO



@bp_tx.route('/type', methods=['GET'])
def gettype():
    query = db.session.query( TIPO_LIGACAO.TIPO_ID.label('ID')
                            , TIPO_LIGACAO.TIPO_DESC.label('TIPO')
                            , TIPO_LIGACAO.DATA_ALTERACAO).all()
    
    result = Schema.types_schema.dump(query)
    db.session.close()
    return jsonify(result)


@bp_tx.route('/type', methods=['POST'])
def regtype():
    query = TIPO_LIGACAO( TIPO_LIGACAO.TIPO_ID.label('ID')
                        , TIPO_LIGACAO.TIPO_DESC.label('TIPO')
                        , TIPO_LIGACAO.DATA_ALTERACAO)

    TIPO_DESC = request.json["TIPO_DESC"]
    DATA_ALTERACAO = request.json["DATA_ALTERACAO"]

    query.TIPO_DESC = TIPO_DESC
    query.DATA_ALTERACAO = DATA_ALTERACAO

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.type_schema.dump(query)
    return jsonify(result)


@bp_tx.route('/type/<string:type_id>', methods=['DELETE'])
def deltype(type_id):

    if db.session.query(TIPO_LIGACAO).filter(TIPO_LIGACAO.TIPO_ID == type_id).count() > 0:
        db.session.query(TIPO_LIGACAO).filter(TIPO_LIGACAO.TIPO_ID == type_id).delete()
        result = {'Fare':type_id}
    else:
        result = {'Fare':'Tarifa inexistente'}
    
    db.session.commit()
    db.session.close()
    return jsonify(result)


# GetFares
@bp_tx.route('/fares/<int:page_num>', methods=['GET'], defaults={'groups': 'all'})
@bp_tx.route('/fares/<string:groups>/<int:page_num>', methods=['GET'])
def getFares(groups, page_num=1):
    per_page=6;
    query = db.session.query( USERS.User_Group.label('GRUPO')
                            , TARIFA.USER_ID.label('USER_CODE')
                            , TIPO_LIGACAO.TIPO_DESC.label('CALL_TYPE')
                            , TARIFA.CUSTO.label('COST')
                            , TARIFA.FRANQUIA_MIN.label('MIN_TELEPHONE_FRANCHISE')
                            , TARIFA.FRANQUIA_VALOR.label('VALUES_TELEPHONE_FRANCHISE')
                            , TARIFA.VALOR_RAMAL.label('VALUE_EXTENSION')
                            , TARIFA.TIPO_ID.label('TYPE_CALL_ID'))
    if groups == 'all' :
        extensions = query.join(TARIFA, TARIFA.TIPO_ID==TIPO_LIGACAO.TIPO_ID)\
                          .join(USERS, USERS.USER_ID==TARIFA.USER_ID, isouter=True)\
                          .order_by(USERS.USER_CODE.asc(),TIPO_LIGACAO.TIPO_DESC.asc())
    else:
        extensions = query.join(TARIFA, TARIFA.TIPO_ID==TIPO_LIGACAO.TIPO_ID)\
                          .join(USERS, USERS.USER_ID==TARIFA.USER_ID, isouter=True)\
                          .filter(TARIFA.USER_ID.in_(([groups])))

    pg = extensions.paginate(page=page_num,per_page=per_page).items

    total = []
    total_pages={}
    total_pages['Total'] = (extensions.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (extensions.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (extensions.paginate(page=page_num,per_page=per_page).page)
    result = Schema.fares_schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})


    db.session.close()
    return jsonify(result)


# Update Fares
@bp_tx.route('/fares/<string:group>&<string:type>', methods=['POST'])
def updtExt(group,type):
    query = TARIFA.query.filter(TARIFA.USER_ID==group, TARIFA.TIPO_ID == type)
    query.update(request.json)
    db.session.commit()

    result = Schema.tarifas_schema.dump(query)
    query.session.close()
    return jsonify(result)


# Register Fare
@bp_tx.route('/fares/regfare', methods=['POST'])
def regfare():

    query = TARIFA( TARIFA.USER_ID
                  , TARIFA.TIPO_ID
                  , TARIFA.CUSTO
                  , TARIFA.DATA_ALTERACAO
                  , TARIFA.FRANQUIA_MIN
                  , TARIFA.FRANQUIA_VALOR
                  , TARIFA.VALOR_RAMAL
                  , TARIFA.BATCH_ID
                )
    USER_ID = request.json["USER_ID"]
    TIPO_ID = request.json["TIPO_ID"]
    CUSTO = request.json["CUSTO"]
    DATA_ALTERACAO = request.json["DATA_ALTERACAO"]
    FRANQUIA_MIN = request.json["FRANQUIA_MIN"]
    FRANQUIA_VALOR = request.json["FRANQUIA_VALOR"]
    VALOR_RAMAL = request.json["VALOR_RAMAL"]
    BATCH_ID = request.json["BATCH_ID"]

    query.USER_ID = USER_ID
    query.TIPO_ID = TIPO_ID
    query.CUSTO = CUSTO
    query.DATA_ALTERACAO = DATA_ALTERACAO
    query.FRANQUIA_MIN = FRANQUIA_MIN
    query.FRANQUIA_VALOR = FRANQUIA_VALOR
    query.VALOR_RAMAL = VALOR_RAMAL
    query.BATCH_ID = BATCH_ID

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.tarifa_Schema.dump(query)
    return jsonify(result)


# Delete Fares
@bp_tx.route('/fares/delfare/<int:user_id>&<int:type_id>', methods=['DELETE'])
def delFare(user_id,type_id):
    if db.session.query(TARIFA)\
                 .filter(TARIFA.USER_ID == user_id)\
                 .filter(TARIFA.TIPO_ID==type_id).count() > 0:
        
        db.session.query(TARIFA)\
                  .filter(TARIFA.USER_ID == user_id)\
                  .filter(TARIFA.TIPO_ID==type_id).delete()
        result = {'Grupo':user_id}
    else:
        result = {'Fare':'Tarifa inexistente'}
    
    db.session.commit()
    db.session.close()
    return jsonify(result)