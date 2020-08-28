from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime

bp_ca = Blueprint('controle_agrupamento', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


class controle_agrupamento_bkp(db.Model):
    linha = db.Column(db.String(255), primary_key=True)
    user_group_id = db.Column(db.Integer, primary_key=True)
    tipo_linha = db.Column(db.String(255))
    data_envio_nova = db.Column(db.Date)
    data_validacao_cliente = db.Column(db.Date)
    data_cancelamento = db.Column(db.Date)
    status = db.Column(db.String(10))
    data_alteracao = db.Column(db.Date, server_default=db.func.sysdate())

    def __init__(self, linha, user_group_id, tipo_linha, data_envio_nova, data_validacao_cliente, data_cancelamento, status, data_alteracao):
        self.linha = linha
        self.user_group_id = user_group_id
        self.tipo_linha = tipo_linha
        self.data_envio_nova = data_envio_nova
        self.data_validacao_cliente = data_validacao_cliente
        self.data_cancelamento = data_cancelamento
        self.status = status
        self.data_alteracao = data_alteracao

class Users(db.Model):
    USER_ID = db.Column(db.Integer, primary_key=True)
    USER_DESC = db.Column(db.String(255))
    USER_CODE = db.Column(db.Integer, primary_key=True)
    USER_GROUP_ID = db.Column(db.Integer)
    ACTIVATION_DATE = db.Column(db.Date)
    EXPIRATION_DATE = db.Column(db.Date)
    ENABLED_DATE = db.Column(db.Date)
    User_Group = db.Column(db.String(10))


    def __init__(self, USER_ID, USER_DESC, USER_CODE, USER_GROUP_ID, ACTIVATION_DATE, EXPIRATION_DATE, ENABLED_DATE, User_Group):
        self.USER_ID = USER_ID
        self.USER_DESC = USER_DESC
        self.USER_CODE = USER_CODE
        self.USER_GROUP_ID = USER_GROUP_ID
        self.ACTIVATION_DATE = ACTIVATION_DATE
        self.EXPIRATION_DATE = EXPIRATION_DATE
        self.ENABLED_DATE = ENABLED_DATE
        self.User_Group = User_Group

class Tarifa(db.Model):
    USER_ID = db.Column(db.Integer, primary_key=True)
    TIPO_ID = db.Column(db.Integer, primary_key=True)
    CUSTO = db.Column(db.Float)
    DATA_ALTERACAO = db.Column(db.Date)
    FRANQUIA_MIN = db.Column(db.Float)
    FRANQUIA_VALOR = db.Column(db.Float(precision=2))
    VALOR_RAMAL = db.Column(db.Float)
    BATCH_ID = db.Column(db.Integer)

    def __init__(self, USER_ID, TIPO_ID, CUSTO, DATA_ALTERACAO, FRANQUIA_MIN, FRANQUIA_VALOR, VALOR_RAMAL, BATCH_ID):
        self.USER_ID = USER_ID
        self.TIPO_ID = TIPO_ID
        self.CUSTO = CUSTO
        self.DATA_ALTERACAO = DATA_ALTERACAO
        self.FRANQUIA_MIN = FRANQUIA_MIN
        self.FRANQUIA_VALOR = FRANQUIA_VALOR
        self.VALOR_RAMAL = VALOR_RAMAL
        self.BATCH_ID = BATCH_ID



# Show ext pages
@bp_ca.route('/extensions/<int:ext>/<int:page_num>', methods=['GET'])
def exts(ext,page_num=1):
    per_page = 20
    query = db.session.query( Users.User_Group.label('Grupo')
                            , controle_agrupamento_bkp.linha
                            , controle_agrupamento_bkp.user_group_id
                            , controle_agrupamento_bkp.tipo_linha
                            , controle_agrupamento_bkp.data_envio_nova
                            , controle_agrupamento_bkp.data_validacao_cliente
                            , controle_agrupamento_bkp.data_cancelamento
                            , controle_agrupamento_bkp.status
                            , controle_agrupamento_bkp.data_alteracao
                            , db.func.CalculoRamal( controle_agrupamento_bkp.data_validacao_cliente
                                                  , controle_agrupamento_bkp.data_cancelamento
                                                  , Tarifa.VALOR_RAMAL
                                                  , controle_agrupamento_bkp.status).label('PROPORCIONAL'))
    if (ext == 0):
        extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
                          .join(Tarifa, Tarifa.USER_ID == Users.USER_ID)\
                          .group_by(controle_agrupamento_bkp.linha)
    else:
        extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
                          .join(Tarifa, Tarifa.USER_ID == Users.USER_ID)\
                          .filter(controle_agrupamento_bkp.linha==ext)\
                          .group_by(controle_agrupamento_bkp.linha)
    
    pg = extensions.paginate(page=page_num,per_page=per_page).items
    # print(dir(extensions.paginate(page=page_num)))
    total = []
    total_pages={}
    total_pages['Total'] = (extensions.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (extensions.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (extensions.paginate(page=page_num,per_page=per_page).page)
    result = Schema.exts_schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})



# Show ext to activation
@bp_ca.route('/extKeep/<string:sts>', methods=['GET'])
def extsKeep(sts):
    if (sts == 'A'):
        sts = ['Y','P','N']
    # else:
    #     this_status = sts
    
    # print(sts);
    query = db.session.query( Users.User_Group.label('Grupo')
                            , controle_agrupamento_bkp.linha
                            , controle_agrupamento_bkp.user_group_id
                            , controle_agrupamento_bkp.tipo_linha
                            , controle_agrupamento_bkp.data_envio_nova
                            , controle_agrupamento_bkp.data_validacao_cliente
                            , controle_agrupamento_bkp.data_cancelamento
                            , controle_agrupamento_bkp.status
                            , controle_agrupamento_bkp.data_alteracao
                            , db.func.CalculoRamal( controle_agrupamento_bkp.data_validacao_cliente
                                                  , controle_agrupamento_bkp.data_cancelamento
                                                  , Tarifa.VALOR_RAMAL
                                                  , controle_agrupamento_bkp.status).label('PROPORCIONAL'))
    extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
                      .join(Tarifa, Tarifa.USER_ID == Users.USER_ID)\
                      .filter(controle_agrupamento_bkp.status.in_(sts))\
                      .group_by(controle_agrupamento_bkp.linha).all()
    result = Schema.exts_schema.dump(extensions)
    db.session.close()
    return jsonify(result)





# # Show ext properties
# @bp_ca.route('/extensions/ext/<string:ext>', methods=['GET'])
# def ext(ext):
#     query = db.session.query( Users.User_Group.label('Grupo')
#                             , controle_agrupamento_bkp.linha
#                             , controle_agrupamento_bkp.user_group_id
#                             , controle_agrupamento_bkp.tipo_linha
#                             , controle_agrupamento_bkp.data_envio_nova
#                             , controle_agrupamento_bkp.data_validacao_cliente
#                             , controle_agrupamento_bkp.data_cancelamento
#                             , controle_agrupamento_bkp.status
#                             , controle_agrupamento_bkp.data_alteracao
#                             , db.func.CalculoRamal( controle_agrupamento_bkp.data_validacao_cliente
#                                                   , controle_agrupamento_bkp.data_cancelamento
#                                                   , Tarifa.VALOR_RAMAL
#                                                   , controle_agrupamento_bkp.status).label('PROPORCIONAL'))
#     extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
#                       .join(Tarifa, Tarifa.USER_ID == Users.USER_ID)\
#                       .filter(controle_agrupamento_bkp.linha==ext)\
#                       .first_or_404('Ramal não existente ainda!')
#     result = Schema.ext_schema.dump(extensions)
#     db.session.close()
#     return jsonify(result)


# Show exts qty per group
@bp_ca.route('/extensions/qty', methods=['GET'], defaults={"monthId":str(datetime.date.today().year)+str(datetime.date.today().month)})
@bp_ca.route('/extensions/qty/<int:monthId>', methods=['GET'])
def qty_ext(monthId):
    month_id = utils.monthId(monthId)
    # print("Month_id",month_id, "----", datetime.date.today(), "----", datetime.date.today().year, datetime.date.today().month, db.func.date_part('YEAR', datetime.date.today()))
    query = db.session.query(Users.User_Group.label('Grupo')\
                            , db.func.cast(db.func.sum(db.case([(db.and_( controle_agrupamento_bkp.status == "Y"
                                                                        , db.func.date_format(controle_agrupamento_bkp.data_alteracao,'%Y%m') <= month_id ), 1)], else_=0)), db.Integer).label('RAMAIS_ATIVOS')
                            , db.func.cast(db.func.sum(db.case([(db.and_( controle_agrupamento_bkp.status == "Y"
                                                                        , db.func.date_format(controle_agrupamento_bkp.data_validacao_cliente,'%Y%m') == month_id ), 1)], else_=0)), db.Integer).label('ATIVADOS_MES')
                            , db.func.cast(db.func.sum(db.case([(db.and_( controle_agrupamento_bkp.status == "P"
                                                                        , db.func.date_format(controle_agrupamento_bkp.data_envio_nova,'%Y%m') <= month_id ), 1)], else_=0)), db.Integer).label('EM_ATIVACAO')
                            , db.func.cast(db.func.sum(db.case([(db.and_( controle_agrupamento_bkp.status == "N"
                                                                        , db.func.date_format(controle_agrupamento_bkp.data_cancelamento,'%Y%m') == month_id ), 1)], else_=0)), db.Integer).label('DESCONECTADOS')
                            )
    
    if month_id == utils.monthId(str(datetime.date.today().year)+str(datetime.date.today().month)):
        print("Entrou Aqui IF", month_id)
        extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
        .filter(db.func.date_format(controle_agrupamento_bkp.data_envio_nova,'%Y%m')<=\
                                db.func.date_format(datetime.date.today(),'%Y%m'))\
        .group_by(Users.User_Group)
    else:
        print("Else Entrou Aqui", utils.monthId(str(datetime.date.today().year)+str(datetime.date.today().month)))
        extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
        .filter(db.func.date_format(controle_agrupamento_bkp.data_envio_nova,'%Y%m') <= month_id)\
        .group_by(Users.User_Group)
    print(extensions)
    result = Schema.exts_schema.dump(extensions)
    db.session.close()
    return jsonify(result)


# Activate and Deactivate Extensions
@bp_ca.route('/extensions/updtext/<string:ext>', methods=['POST'])
def updtExt(ext):
    query = controle_agrupamento_bkp.query.filter(controle_agrupamento_bkp.linha==ext)
    # status = request.json["status"]
    # data_validacao_cliente = request.json["data_validacao_cliente"]

    # query.status = status
    # query.data_validacao_cliente = data_validacao_cliente
    query.update(request.json)
    # db.session.add(query)
    db.session.commit()
    query.session.close()
    result = Schema.exts_schema.dump(query)
    return jsonify(result)


# Delete Extensions
@bp_ca.route('/extensions/delext/<string:ext>', methods=['DELETE'])
def delExt(ext):
    query = controle_agrupamento_bkp.query.filter(controle_agrupamento_bkp.linha==ext)
    if query.count() > 0:
        query.delete()
        result = {'Deleted':ext}
    else:
        result = {'Ramal':'Inexistente'}
    db.session.commit()
    query.session.close()
    return jsonify(result)

# Register Extensions
@bp_ca.route('/extensions/regext', methods=['POST'])
def regExt():

    query = controle_agrupamento_bkp( controle_agrupamento_bkp.linha
                                    , controle_agrupamento_bkp.user_group_id
                                    , controle_agrupamento_bkp.tipo_linha
                                    , controle_agrupamento_bkp.data_envio_nova
                                    , controle_agrupamento_bkp.data_validacao_cliente
                                    , controle_agrupamento_bkp.data_cancelamento
                                    , controle_agrupamento_bkp.status
                                    , controle_agrupamento_bkp.data_alteracao)

    linha = request.json["linha"]
    user_group_id = request.json["user_group_id"]
    tipo_linha = request.json["tipo_linha"]
    data_envio_nova = request.json["data_envio_nova"]
    data_validacao_cliente = controle_agrupamento_bkp.data_validacao_cliente
    data_cancelamento = controle_agrupamento_bkp.data_cancelamento
    status = request.json["status"]
    data_alteracao = request.json["data_alteracao"]

    query.linha = linha
    query.user_group_id = user_group_id
    query.tipo_linha = tipo_linha
    query.data_envio_nova = data_envio_nova
    # query.data_validacao_cliente = data_validacao_cliente
    # query.data_cancelamento = data_cancelamento
    query.status = status
    query.data_alteracao = data_alteracao

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.ext_schema.dump(query)
    return jsonify(result)


# Get Extension Information descriptive
@bp_ca.route("/extensions/desc/<int:month_id>/<int:page_num>", methods=['GET'])
def getExtDesc(month_id,page_num=1):
    per_page = 10;
    query = db.session.query(Users.User_Group.label('Grupo')
                            , controle_agrupamento_bkp.linha
                            , db.case([(db.and_( controle_agrupamento_bkp.status == "Y"
                                                    , db.func.cast(db.func.concat( db.func.year( controle_agrupamento_bkp.data_validacao_cliente)
                                                                    , db.func.month(controle_agrupamento_bkp.data_validacao_cliente)), db.Integer) == db.func.cast(month_id, db.Integer) ), controle_agrupamento_bkp.data_validacao_cliente)], else_='').label('ATIVADOS_MES')
                            , db.case([(db.and_( controle_agrupamento_bkp.status == "P"
                                                    , db.func.cast(db.func.concat( db.func.year( controle_agrupamento_bkp.data_envio_nova)
                                                                    , db.func.month(controle_agrupamento_bkp.data_envio_nova)), db.Integer) == db.func.cast(month_id, db.Integer) ), controle_agrupamento_bkp.data_envio_nova)], else_='').label('EM_ATIVACAO')
                            , db.case([(db.and_( controle_agrupamento_bkp.status == "N"
                                                    , db.func.cast(db.func.concat( db.func.year( controle_agrupamento_bkp.data_cancelamento)
                                                                    , db.func.month(controle_agrupamento_bkp.data_cancelamento)), db.Integer) == db.func.cast(month_id, db.Integer) ), controle_agrupamento_bkp.data_cancelamento)], else_='').label('DESCONECTADOS')
                            )
    print(query)
    extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)\
                      .filter(db.func.cast(\
                                  db.func.concat(\
                                      db.func.year(controle_agrupamento_bkp.data_alteracao),\
                                          db.func.month(controle_agrupamento_bkp.data_alteracao)), db.Integer)==\
                                              db.func.cast(month_id, db.Integer))\
                                                  .group_by(controle_agrupamento_bkp.linha)
                                                      
    pg = extensions.paginate(page=page_num,per_page=per_page).items
    # print(dir(extensions.paginate(page=page_num)))
    total = []
    total_pages={}
    total_pages['Total'] = (extensions.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (extensions.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (extensions.paginate(page=page_num,per_page=per_page).page)
    result = Schema.exts_schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})
