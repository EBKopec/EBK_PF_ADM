  
from flask import Blueprint, current_app, request, jsonify
from model.controleAgrupamentoModel import controle_agrupamento_bkp, Users
from schema.controleAgrupamentoSchema import controle_agrupamento_bkpSchema
from flask_restful import Resource, Api

bp_ca = Blueprint('controle_agrupamento', __name__)

# class controle_agrupamento(Resource):
    # def get(self, page_num):
        # query = db.session.query(Users.User_Group
        #                         , controle_agrupamento_bkp.linha
        #                         , controle_agrupamento_bkp.user_group_id
        #                         , controle_agrupamento_bkp.tipo_linha
        #                         , controle_agrupamento_bkp.data_envio_nova
        #                         , controle_agrupamento_bkp.data_validacao_cliente
        #                         , controle_agrupamento_bkp.data_cancelamento
        #                         , controle_agrupamento_bkp.status
        #                         , controle_agrupamento_bkp.data_alteracao_grupo)
        # extensions = query.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)
        # pg = extensions.paginate(page=page_num).items
        # # print(dir(extensions.paginate(page=page_num)))
        # total = []
        # total_pages={}
        # total_pages['Total'] = (extensions.paginate(page=page_num).total)
        # total_pages['Pages'] = (extensions.paginate(page_num).pages)
        # total_pages['Current_Page'] = (extensions.paginate(page_num).page)
        # result = exts_schema.dump(pg)
        # total = jsonify({"docs":result,'Pages':total_pages})
        # return total


@bp_ca.route('/ext/<int:page_num>', methods=['GET'])
def ramais(page_num):
    tq = controle_agrupamento_bkp.query(Users.User_Group
                                , controle_agrupamento_bkp.linha
                                , controle_agrupamento_bkp.user_group_id
                                , controle_agrupamento_bkp.tipo_linha
                                , controle_agrupamento_bkp.data_envio_nova
                                , controle_agrupamento_bkp.data_validacao_cliente
                                , controle_agrupamento_bkp.data_cancelamento
                                , controle_agrupamento_bkp.status
                                , controle_agrupamento_bkp.data_alteracao_grupo)
    extensions = tq.join(Users, Users.USER_ID==controle_agrupamento_bkp.user_group_id)
    # pg = extensions.paginate(page=page_num).items
    print("Aqui", extensions)
    # print(dir(extensions.paginate(page=page_num)))
    total = []
    # total_pages={}
    # total_pages['Total'] = (extensions.paginate(page=page_num).total)
    # total_pages['Pages'] = (extensions.paginate(page_num).pages)
    # total_pages['Current_Page'] = (extensions.paginate(page_num).page)
    # result = exts_schema.dump(pg)
    # total = jsonify({"docs":result,'Pages':total_pages})
    return total