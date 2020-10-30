from administration import administrationExtensions
from app import PMPG
from flask import Flask, request, jsonify, session
from gevent.pywsgi import WSGIServer
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Resource, Api
from flask_cors import CORS
from model.controleAgrupamentoModel import bp_ca,configure
from model.tarifasModel import bp_tx,configure
from model.backupsModel import bp_bg,configure
from model.resumoConsumoModel import bp_rc, configure
from model.srcUtilsModel import bp_su, configure, srcUtils
from model.faturamentoModel import bp_fat, configure
from model.login.loginModel import bp_lg, configure
from model.anoMesModel import bp_am, configure
from model.excelModel import bp_xls,configure,fl_excel
from model.localSetorModel import bp_lcl, configure
from schema.Schema import configure as config_ma
from zipfile import ZipFile
import shutil
import os
from os.path import basename
from shutil import copyfile
from exportPdf import exportPDF
from tqdm.auto import tqdm
from sqls import sqls
from datetime import datetime, date
from utils import utils
import pandas as pd
import json
import dbConfig as cfg
import sys
import time
import logging
# Init App
app = Flask(__name__)
JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = cfg.conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 30
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 15
app.config['POOL_PRE_PING'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60*60
app.config['POOLCLASS'] = 'NullPool'
app.config['SECRET_KEY'] = 'super-secret'

# Init DB
configure(app)
# Init MA
config_ma(app)

# Ramais
from model import controleAgrupamentoModel,tarifasModel
app.register_blueprint(bp_ca)
app.register_blueprint(bp_tx)
app.register_blueprint(bp_bg)
app.register_blueprint(bp_rc)
app.register_blueprint(bp_su)
app.register_blueprint(bp_fat)
# app.register_blueprint(bp_fec)
app.register_blueprint(bp_lg)
app.register_blueprint(bp_am)
app.register_blueprint(bp_xls)
app.register_blueprint(bp_lcl)

logging.basicConfig(filename='/var/log/flask/main.proc.log',level=logging.DEBUG)
class main():
    def __init__(self):
        self.request = PMPG()
        self.sql = sqls()
        self.adm = administrationExtensions()
        self.gp = {'PMPG': ['PMPG', 'SME_ESCOLA', 'SME_CMEI']
                 , 'FMS': ['FMS_AIH', 'FMS_PAB']}
        
        # self.base_root = srcUtils('pdf').get('src_utils')


    def mainDef(self,month):

        #logging.basicConfig(filename='main.proc'+month+'.log',level=print)
        base_root = srcUtils('BASE_ROOT').get('src_utils')
        base_root_excel = srcUtils('XLSX').get('src_utils')
        folder = utils.checkDir(base_root,'Fechamento')
        folder_excel = utils.checkDir(base_root_excel,month)


        start_time = time.time()
        # print(srcUtils('pdf').get('src_utils'))
        logging.debug(" Started: %s --- Period: %s" % (datetime.now(), month))
        
        # Import Data from VSC to NF
        #self.request.importVSCtoNF(month)
        logging.debug(" --- %s seconds --- " % (time.time() - start_time))

        for index in self.request.groups:
            
            file_to_read=folder+"/Fechamento_"+index+".xlsx"
            file_to_write= folder_excel+"/"+"Fechamento_"+index+"_"+month+".xlsx"
            

            copyfile(file_to_read,file_to_write)
            for value in self.request.groups[index]:
                time.sleep(0.1)
                temp = time.time()

                # Insert Groups
                self.request.insertGroups(month, value)
                getView = self.sql.getViews(value, month)
                getExtQty = self.sql.getQtyExt(value, utils.monthId(month))
                getVlExt = self.sql.getVlPtExt(value, utils.monthId(month))
                df = self.request.execOperation(getView[0], getView[1])
                dfExt = self.request.execOperation(getExtQty[0], getExtQty[1])
                dfVlExt = self.request.execOperation(getVlExt[0],getVlExt[1])
                #month_id = utils.monthId(month) + '01'
                # print('dfExt', dfExt[0][2])
                if len(df) == 0:
                   continue
                else:
                    logging.debug(" Qty Rows: %s Group: %s Grouping: %s " % (len(df), index, value))
                    # Export Views to Excel
                    #self.request.writeExcelMonth(month_id, value, file_to_write)
                    self.request.writeExcelExt(dfExt, index, file_to_write)
                    self.request.writeExcelProp(dfVlExt, index, file_to_write)
                    self.request.writeExcel(df, value, index, file_to_write)
                    logging.debug(" --- Group %s %s seconds --- " % (value, (time.time() - temp)))

        logging.debug(" --- %s seconds --- " % (time.time()- start_time))
        self.zipTotal(month,'XLSX')
        self.total(month)
        self.summarizedReport(month)
        self.demonstrativeReport(month)


    def zipTotal(self, month,type_file):
        base_root = srcUtils(type_file).get('src_utils')+'\\'+month
        archiveZip = os.path.join(base_root,'Files_'+month+'.zip')
        if type_file == 'XLSX':
            utils.zipFilesInDir(base_root, archiveZip, lambda name : 'xlsx' in name)
        else:
            utils.zipFilesInDir(base_root, archiveZip, lambda name : 'pdf' in name)

        logging.debug('All files %s zipped successfully!' % ( type_file )) 
        
        # calling function to get all file paths in the directory 
        # file_paths = utils.get_all_file_paths(base_root)

        # # printing the list of all files to be zipped 
        # print('Following files will be zipped:') 
        # for file_name in file_paths: 
        #     print(file_name) 

        # # writing files to a zipfile 
        # with ZipFile(archiveZip,'w') as zip: 
        #     # writing each file one by one 
        #     for file in file_paths: 
        #         zip.write(file)
        
        # print('All files zipped successfully!') 
        # print('Zipped Done!')
        

    
    def total(self, month):
        for index in self.gp:
            for value in self.gp[index]:
                logging.debug("\n Grupo: %s " % value)
                self.adm.saveTotal(value, month)

    
    def summarizedReport(self, month):
        base_root = srcUtils('pdf').get('src_utils')
        folder = utils.checkDir(base_root,month)

        file_= "NFe_Mes_"+month+".pdf"
        self.pdf = exportPDF()
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.pdf.headerGroup()
        # Fill data
        for index in self.gp:
            for value in tqdm(self.gp[index]):
                self.pdf.cell(1, ln=2)
                self.pdf.drawBodyNFe(value, month)

        self.pdf.output(folder+"/"+file_)
        

    def demonstrativeReport(self, month):
        base_root = srcUtils('pdf').get('src_utils')
        folder = utils.checkDir(base_root,month)
        getList = self.sql.getListPdfs()
        df = pd.DataFrame.from_records(self.request.execOperation(getList[0], getList[1]),
                                           columns=['ID_PDF']).sort_values(by=['ID_PDF'], ascending=True)
        dfList = df['ID_PDF'].tolist()

        for index in self.gp:
            for value in tqdm(self.gp[index]):
                if (index == 'FMS'):
                    for i in range(len(dfList)):
                        pdf = exportPDF()
                        pdf.alias_nb_pages()
                        pdf.add_page()
                        pdf.drawBodyDmt(value, month, dfList[i])
                        pdf.add_page()
                        pdf.drawBodydms(value, month, dfList[i])
                        file_= "Demonstrativo_"+ value +"_Mes_"+ month +"_Grupo_Nº"+ dfList[i] +".pdf"
                        pdf.output(folder+"/"+file_)
        self.zipTotal(month,'pdf')


class App(Resource):
    def __init__(self):
        self.pmpg = main()

    def get(self, month):
        self.pmpg.mainDef(month)
        logging.debug('Executado_Mes %s' % (month))

        return {"period":month}

api.add_resource(App, '/pmpg/<string:month>')
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()