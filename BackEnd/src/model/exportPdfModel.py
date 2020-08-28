from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api
from schema import Schema
from utils import utils
import datetime


bp_ep = Blueprint('exportPdf', __name__)

db = SQLAlchemy()

def configure(app):
    db.init_app(app)
    app.db = db


