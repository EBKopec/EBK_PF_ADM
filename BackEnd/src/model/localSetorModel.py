from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime


bp_lcl = Blueprint('local', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


# Local
class local(db.Model):
    id_local = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao_local = db.Column(db.String(255))

    def __init__(self, id_local, descricao_local):
        self.id_local = id_local
        self.descricao_local = descricao_local

# Get Local
@bp_lcl.route('/local/<int:page_num>', methods=['GET'])
def getLocal(page_num):
    per_page = 10
    query = db.session.query(local)

    pg = query.paginate(page=page_num,per_page=per_page).items

    total = []
    total_pages={}
    total_pages['Total'] = (query.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (query.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (query.paginate(page=page_num,per_page=per_page).page)
    result = Schema.localSetores_Schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})

@bp_lcl.route('/local', methods=['GET'])
def getLocalnoPg():    
    query = db.session.query(local)
    result = Schema.localSetores_Schema.dump(query)
    db.session.close()
    return jsonify(result)



# Add Local
@bp_lcl.route('/setlocal', methods=['POST'])
def addLocal():
    query = local( local.id_local
                 , local.descricao_local)
    
    id_local = local.id_local
    descricao_local = request.json["descricao_local"]

    query.id_local = local.id_local
    query.descricao_local = descricao_local

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.localSetor_Schema.dump(query)
    return jsonify(result)


# Update Local
@bp_lcl.route('/updlocal/<int:id>', methods=['POST'])
def updLocal(id):
    query = local.query.filter(local.id_local==id)
    query.update(request.json)
    db.session.commit()
    query.session.close()
    result = Schema.localSetor_Schema.dump(query)
    return jsonify(result)


# Delete Local
@bp_lcl.route('/dellocal/<int:id>', methods=['DELETE'])
def dellocal(id):
    query = local.query.filter(local.id_local==id).first_or_404(description='Não existe o local informado')
    query.delete()
    result = {'Local':'{} Deleted'.format(local.descricao_local)}
    db.session.commit()
    query.session.close()
    return jsonify(result)

# Setor
class setor(db.Model):
    id_setor = db.Column(db.Integer, primary_key=True)
    descricao_setor = db.Column(db.String(255))

    def __init__(self, id_setor, descricao_setor):
        self.id_setor = id_setor
        self.descricao_setor = descricao_setor


# Get Setor
@bp_lcl.route('/setor/<int:page_num>', methods=['GET'])
def getSetor(page_num):
    per_page = 10
    query = db.session.query(setor)

    pg = query.paginate(page=page_num,per_page=per_page).items

    total = []
    total_pages={}
    total_pages['Total'] = (query.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (query.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (query.paginate(page=page_num,per_page=per_page).page)
    result = Schema.localSetores_Schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})

@bp_lcl.route('/setor', methods=['GET'])
def getSetornoPg():
    query = db.session.query(setor)
    result = Schema.localSetores_Schema.dump(query)
    db.session.close()
    return jsonify(result)

# Add Setor
@bp_lcl.route('/setsetor', methods=['POST'])
def addSetor():
    query = setor( setor.id_setor
                 , setor.descricao_setor)
    
    id_setor = setor.id_setor
    descricao_setor = request.json["descricao_setor"]

    query.id_setor = setor.id_setor
    query.descricao_setor = descricao_setor

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.localSetor_Schema.dump(query)
    return jsonify(result)


# Update Setor
@bp_lcl.route('/updSetor', methods=['POST'])
def updSetor(id):
    query = setor.query.filter(setor.id_local==id)
    query.update(request.json)
    db.session.commit()
    query.session.close()
    result = Schema.localSetor_Schema.dump(query)
    return jsonify(result)


# Delete Setor
@bp_lcl.route('/delsetor/<int:id>', methods=['DELETE'])
def delsetor(id):
    query = setor.query.filter(setor.id_setor==id).first_or_404(description='Não existe o setor informado')
    query.delete()
    result = {'Setor':'{} Deleted'.format(setor.descricao_setor)}
    db.session.commit()
    query.session.close()
    return jsonify(result)


# Place
class local_setor(db.Model):
    id_local_setor = db.Column(db.Integer, primary_key=True)
    id_local = db.Column(db.Integer)
    id_setor = db.Column(db.Integer)


    def __init__(self, id_local_setor, id_local, id_setor):
        self.id_local_setor = id_local_setor
        self.id_local = id_local
        self.id_setor = id_setor

# Get Local Setor
@bp_lcl.route('/localsetor/<int:page_num>', methods=['GET'])
def getLocalSetor(page_num):
    per_page = 10
    query = db.session.query( local_setor.id_local_setor
                            , local.id_local
                            , local.descricao_local
                            , setor.id_setor
                            , setor.descricao_setor
                            , db.func.concat(local.descricao_local, ' - ',setor.descricao_setor).label('Local_Setor'))
    descriptions = query.join(local, local.id_local == local_setor.id_local)\
                        .join(setor, setor.id_setor == local_setor.id_setor)

    pg = descriptions.paginate(page=page_num,per_page=per_page).items

    total = []
    total_pages={}
    total_pages['Total'] = (descriptions.paginate(page=page_num,per_page=per_page).total)
    total_pages['Pages'] = (descriptions.paginate(page=page_num,per_page=per_page).pages)
    total_pages['Current_Page'] = (descriptions.paginate(page=page_num,per_page=per_page).page)
    result = Schema.localSetores_Schema.dump(pg)
    db.session.close()
    return jsonify({"docs":result,'Pages':total_pages})


# Get Local Setor - No Pages
@bp_lcl.route('/localsetor', methods=['GET'])
def getLocalSetorNoPg():
    query = db.session.query( local_setor.id_local_setor
                            , db.func.concat(local.descricao_local, ' - ',setor.descricao_setor).label('Local_Setor'))
    descriptions = query.join(local, local.id_local == local_setor.id_local)\
                        .join(setor, setor.id_setor == local_setor.id_setor).all()

    result = Schema.localSetores_Schema.dump(descriptions)
    db.session.close()
    return jsonify(result)


# Set Place
@bp_lcl.route('/setplace', methods=['POST'])
def setPlace():
    query = local_setor( local_setor.id_local_setor
                        , local_setor.id_local
                        , local_setor.id_setor)

    id_local = request.json["id_local"]
    id_setor = request.json["id_setor"]
    local_setor_id = ""

    if (len(str(id_setor)) == 1):
        local_setor_id = str(id_local) + '00' +  str(id_setor)
    elif (len(str(id_setor)) == 2):
        local_setor_id = str(id_local) + '0' + str(id_setor)
    else:
        local_setor_id = str(id_local) + str(id_setor)

    print('Aquiii', local_setor_id, id_local, id_setor)
    query.id_local_setor = local_setor_id
    query.id_local = id_local
    query.id_setor = id_setor

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    result = Schema.localSetor_Schema.dump(query)
    return jsonify(result)


# Delete Places
@bp_lcl.route('/delplace/<int:id>', methods=['DELETE'])
def delplace(id):
    query = local_setor.query.filter(local_setor.id_local_setor==id).first_or_404(description='Não existe o ID informado')
    query.delete()
    result = {'Place':'{} Deleted'.format(local_setor.id_local_setor)}
    db.session.commit()
    query.session.close()
    return jsonify(result)