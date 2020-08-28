from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify, json
from flask_restful import Resource, Api
from schema import Schema
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token


bp_lg = Blueprint('application_users', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    CORS(app)
    app.db = db


class application_users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), default=False)
    bcrypt = Bcrypt()

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


@bp_lg.route('/users/register', methods=['POST'])
def register():
    query = application_users( application_users.id
                            , application_users.username
                            , application_users.password
                            , application_users.email)

    username = request.json["username"]
    password = application_users.bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    email = request.json['email']

    if query.query.filter(application_users.username == username).first():
        return jsonify({'Error':'User already existed'})

    query.username = username
    query.password = password
    query.email = email

    db.session.add(query)
    db.session.commit()
    db.session.refresh(query)
    db.session.close()
    
    result = Schema.app_users_Schema.dump(query)
    return jsonify(result)


@bp_lg.route('/login', methods=['POST'])
def login():
    query = db.session.query(application_users.username
                            , application_users.password)
    username = request.json["username"]
    password = request.json["password"]
    extension = query.filter(application_users.username == username).first()
    # query = application_users.query.filter(application_users.username == username).first()

    # print(application_users.bcrypt.check_password_hash(extension.password, password))
    
    if not extension or not application_users.bcrypt.check_password_hash(extension.password, password):
        return jsonify({'Error':'Invalid UserName and/or password'}), 401
    else:
        access_token = create_access_token(identity=extension)
        # print(access_token)
        result = jsonify(access_token)
    query.session.close()
    return result,200