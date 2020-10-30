import pandas as pd
import numpy as np
from app import PMPG
from sqls import sqls
import locale
import json
from utils import utils
import logging
pd.options.mode.chained_assignment = None
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#logging.basicConfig(filename='main.proc.log',level=logging.DEBUG)
logging.basicConfig(filename='/var/log/flask/main.proc.administration.log',level=logging.DEBUG)
class administrationExtensions():

    def __init__(self):
        self.pmpg = PMPG()
        self.sql = sqls()

    # Consume Ext
    def conExt(self, group, month):
        ext = self.sql.getExtTotal(group, month)
        data = self.pmpg.execOperation(ext[0], ext[1])

        df = pd.DataFrame.from_records(data, columns=['TIPO','SOMA_DE_DURACAO','SOMA_DE_CUSTO','ID_PDF','ORIGEM'])





    # Excess Consumption
    def excessCon(self, group, month):
        """
        -/To result the data below is used excessCon method/-
        -/excessCon get group name and result consumption exceeded dataframe/-
        
        -/tipo, Soma_Duracao, Soma_Custo, VALOR_MIN, FRANQUIA_MIN, FRANQUIA_VALOR, EXCEDENTE_VALOR, EXCEDENTE_MIN/-
        -/LDN, 777 min 48 seg, 163.50   , 0.17     , 4000        , 680           , 0              , 0            /-
        
        -/Afterwards, resCon method receives a dataframe/-
        -/to process the data and result the total/-

        -/Grupo, Ramais_Ativo, Valor_ramal, Parcial, Faturar_Ramais, Franquias, Excedentes, Total_Faturar/-
        -/PMPG , 543         , 19.23      , 44.229 , 10389.969     , 1715.000 ,  3294.710 , 15399.679    /-
        """

        ex = self.sql.getGroup(group, month)
        exc = self.sql.excessCons(group)
        data = self.pmpg.execOperation(ex[0], ex[1])
        # print('TMP', data)
        # data = pd.DataFrame(tmp, columns=['TIPO', 'Soma_Duracao', 'Soma_Custo'])
        data2 = self.pmpg.execOperation(exc[0], exc[1])
        
        df = pd.DataFrame.from_records(data2, columns=["TIPO", "VALOR_MIN", "FRANQUIA_MIN", "FRANQUIA_VALOR"])
        
        if data.empty:
            default = {'TIPO': ['LDN','LOCAL', 'MOVEL'],
                    'Soma_Custo': [0,0,0],
                    'Soma_Duracao':['0','0','0'] }
            data = pd.DataFrame(default, columns=['TIPO', 'Soma_Duracao', 'Soma_Custo']).fillna(0).sort_values('TIPO', ascending=True).reset_index(drop=True)
        else:
            data.columns = ['TIPO', 'Soma_Duracao', 'Soma_Custo']
        #data.columns = ['TIPO', 'Soma_Duracao', 'Soma_Custo']
        # print('Data', type(data),'\n\n', data)
        # print('df', type(df),'\n\n', df)
        #data.columns = ['TIPO', 'Soma_Duracao', 'Soma_Custo']
        dfExc = pd.merge(left=data, right=df, on=['TIPO'], how='outer').fillna(0).sort_values('TIPO', ascending=True).reset_index(drop=True)
        dfExc['EXCEDENTE_VALOR'] = dfExc['Soma_Custo'].astype(float) - dfExc['FRANQUIA_VALOR'].astype(float)
        dfExc['EXCEDENTE_MIN'] = (pd.Series(
            dfExc['Soma_Duracao'].str.split().str[0] + '.' + dfExc['Soma_Duracao'].str.split().str[2]).astype(float)) \
                                  - dfExc['FRANQUIA_MIN'].astype(float)
        dfExc['EXCEDENTE_MIN'] = [x if x > 0 else 0 for x in dfExc['EXCEDENTE_MIN']]
        dfExc['EXCEDENTE_VALOR'] = [x if x > 0 else 0 for x in dfExc['EXCEDENTE_VALOR']]
        return dfExc


    # pre Resume consumption
    def preResCon(self, group, month):
        exc = self.excessCon(group, month)
        exp = self.sql.extList(group, month)
        data = pd.DataFrame.from_records(self.pmpg.execOperation(exp[0], exp[1])
                                         , columns=['RAMAL', 'GRUPO', 'DATA_INSTALACAO', 'DATA_ATIVACAO'
                , 'DATA_CANCELAMENTO', 'VALOR_RAMAL', 'STATUS', 'PROPORCIONAL'])
        xp = exc.fillna(0)
        data['DATA_ATIVACAO_REF'] = pd.to_datetime(data['DATA_ATIVACAO'], errors='coerce').dt.strftime('%Y%m')
        data['PROPORCIONAL'] = data['PROPORCIONAL'].astype('float')
        data['VALOR_RAMAL'] = data['VALOR_RAMAL'].astype('float')
        faturar = pd.DataFrame()
        faturar['RAMAL_ATIVO'] = data.query(" STATUS in ('Y','N') "
                                            " and PROPORCIONAL > 0 "
                                            " and DATA_ATIVACAO_REF <= @utils.monthId(@month)").groupby('GRUPO')['RAMAL'].count()
        faturar['VALOR_RAMAL'] = data.groupby('GRUPO')['VALOR_RAMAL'].unique().astype(float)
        faturar['PARCIAL'] = data.query(" STATUS in ('Y','N') "
                                        " and PROPORCIONAL != '19.23' "
                                        " and DATA_ATIVACAO_REF <= @utils.monthId(@month)").groupby('GRUPO')['PROPORCIONAL'].sum()
        faturar['FATURAR_RAMAIS'] = data.query(" STATUS in ('Y','N') "
                                               " and PROPORCIONAL > 0 "
                                               " and DATA_ATIVACAO_REF <= @utils.monthId(@month)").groupby('GRUPO')['PROPORCIONAL'].sum()
        faturar['FRANQUIAS'] = xp['FRANQUIA_VALOR'].sum()
        faturar['EXCEDENTES'] = xp['EXCEDENTE_VALOR'].sum()
        faturar['TOTAL_FATURAR'] = faturar['FATURAR_RAMAIS'] + faturar['FRANQUIAS'] + faturar['EXCEDENTES']
        faturar['LDN'] = xp.query("TIPO == 'LDN'")['FRANQUIA_MIN'][0]
        faturar['LOCAL'] = xp.query("TIPO == 'LOCAL'")['FRANQUIA_MIN'][1]
        faturar['MOVEL'] = xp.query("TIPO == 'MOVEL'")['FRANQUIA_MIN'][2]
        faturar['LDN_VALOR'] = xp.query("TIPO == 'LDN'")['FRANQUIA_VALOR'][0]
        faturar['LOCAL_VALOR'] = xp.query("TIPO == 'LOCAL'")['FRANQUIA_VALOR'][1]
        faturar['MOVEL_VALOR'] = xp.query("TIPO == 'MOVEL'")['FRANQUIA_VALOR'][2]
        faturar['LDN_EXC'] = xp.query("TIPO == 'LDN'")['EXCEDENTE_VALOR'][0]
        faturar['LOCAL_EXC'] = xp.query("TIPO == 'LOCAL'")['EXCEDENTE_VALOR'][1]
        faturar['MOVEL_EXC'] = xp.query("TIPO == 'MOVEL'")['EXCEDENTE_VALOR'][2]
        faturar['LDN_EXC_M'] = xp.query("TIPO == 'LDN'")['EXCEDENTE_MIN'][0]
        faturar['LOCAL_EXC_M'] = xp.query("TIPO == 'LOCAL'")['EXCEDENTE_MIN'][1]
        faturar['MOVEL_EXC_M'] = xp.query("TIPO == 'MOVEL'")['EXCEDENTE_MIN'][2]
        # Total Minutes and Total Values
        # LDN_TOTAL_M = xp.query("TIPO == 'LDN'")['Soma_Duracao'][0]
        # LOCAL_TOTAL_M = xp.query("TIPO == 'LOCAL'")['Soma_Duracao'][1]
        # MOVEL_TOTAL_M = xp.query("TIPO == 'MOVEL'")['Soma_Duracao'][2]
        # LDN_TOTAL_VALOR = xp.query("TIPO == 'LDN'")['Soma_Custo'][0]
        # LOCAL_TOTAL_VALOR = xp.query("TIPO == 'LOCAL'")['Soma_Custo'][1]
        # MOVEL_TOTAL_VALOR = xp.query("TIPO == 'MOVEL'")['Soma_Custo'][2]
        # TOTAL_VALOR = str(locale.currency(LDN_TOTAL_VALOR + LOCAL_TOTAL_VALOR + MOVEL_TOTAL_VALOR, grouping=True))
        
        faturar['LDN_TOTAL_M'] = xp.query("TIPO == 'LDN'")['Soma_Duracao'][0]
        faturar['LOCAL_TOTAL_M'] = xp.query("TIPO == 'LOCAL'")['Soma_Duracao'][1]
        faturar['MOVEL_TOTAL_M'] = xp.query("TIPO == 'MOVEL'")['Soma_Duracao'][2]
        faturar['LDN_TOTAL_VALOR'] = xp.query("TIPO == 'LDN'")['Soma_Custo'][0]
        faturar['LOCAL_TOTAL_VALOR'] = xp.query("TIPO == 'LOCAL'")['Soma_Custo'][1]
        faturar['MOVEL_TOTAL_VALOR'] = xp.query("TIPO == 'MOVEL'")['Soma_Custo'][2]
        
        billing = faturar.fillna(0)
        return billing
    
    # Resume consumption
    def resCon(self, group, month):
        faturar = self.preResCon(group, month)

        LDN_TOTAL_M = faturar['LDN_TOTAL_M'][0]
        LOCAL_TOTAL_M = faturar['LOCAL_TOTAL_M'][0]
        MOVEL_TOTAL_M = faturar['MOVEL_TOTAL_M'][0]
        LDN_TOTAL_VALOR = faturar['LDN_TOTAL_VALOR'][0]
        LOCAL_TOTAL_VALOR = faturar['LOCAL_TOTAL_VALOR'][0]
        MOVEL_TOTAL_VALOR = faturar['MOVEL_TOTAL_VALOR'][0]
        TOTAL_VALOR = str(locale.currency(LDN_TOTAL_VALOR + LOCAL_TOTAL_VALOR + MOVEL_TOTAL_VALOR, grouping=True))

        STFC = "STFC - " + str(locale.currency(round(faturar['TOTAL_FATURAR'][0], 2), grouping=True))
        FATURAR_RAMAIS = round(faturar['FATURAR_RAMAIS'][0], 2)
        RAMAIS_ATIVO = str(round(faturar['RAMAL_ATIVO'][0], 2)) + ' ramais (proporcional) - Total ' + str(
            locale.currency(FATURAR_RAMAIS, grouping=True))
        FRANQUIAS = ' - Total ' + str(locale.currency(round(faturar['FRANQUIAS'][0], 2), grouping=True))
        TTL_EXC = ' - Total ' + str(locale.currency(round(faturar['EXCEDENTES'][0], 2), grouping=True))
        LDN = ' - LDN ' + str(faturar['LDN'][0]) + "'00'' " + str(
            locale.currency(round(faturar['LDN_VALOR'][0], 2), grouping=True))
        LOCAL = ' Local ' + str(faturar['LOCAL'][0]) + "'00'' " + str(
            locale.currency(round(faturar['LOCAL_VALOR'][0], 2), grouping=True))
        MOVEL = ' - Móvel ' + str(faturar['MOVEL'][0]) + "'00'' " + str(
            locale.currency(round(faturar['MOVEL_VALOR'][0], 2), grouping=True)) + FRANQUIAS

        
        LDN_EXC = ' - LDN ' + str(format(faturar['LDN_EXC_M'][0], '.2f')).replace('.', "'") + "'' " + str(
            locale.currency(round(faturar['LDN_EXC'][0], 2), grouping=True))
        LOCAL_EXC = ' Local ' + str(format(faturar['LOCAL_EXC_M'][0], '.2f')).replace('.', "'") + "'' " + str(
            locale.currency(round(faturar['LOCAL_EXC'][0], 2), grouping=True))
        MOVEL_EXC = ' - Móvel ' + str(format(faturar['MOVEL_EXC_M'][0], '.2f')).replace('.', "'") + "'' " + str(
            locale.currency(round(faturar['MOVEL_EXC'][0], 2), grouping=True)) + TTL_EXC
        # print('LDN_EXC', LDN_EXC,'LOCAL_EXC',LOCAL_EXC,'MOVEL_EXC',MOVEL_EXC )

        return STFC, RAMAIS_ATIVO, LDN, LOCAL, MOVEL, LDN_EXC, LOCAL_EXC, MOVEL_EXC, faturar.index[0]\
            , LDN_TOTAL_M, locale.currency(LDN_TOTAL_VALOR,grouping=True)\
            , LOCAL_TOTAL_M, locale.currency(LOCAL_TOTAL_VALOR,grouping=True)\
            , MOVEL_TOTAL_M, locale.currency(MOVEL_TOTAL_VALOR,grouping=True), TOTAL_VALOR


    def saveTotal(self, group, month):
        totalBilling = pd.DataFrame()
        totalBilling = self.preResCon(group,month)
        totalBilling.insert(0,'mes_id', month)
        totalBilling.insert(1,'group', group)
        
        totalBilling['total'] = totalBilling['LDN_TOTAL_VALOR'] + totalBilling['LOCAL_TOTAL_VALOR'] + totalBilling['MOVEL_TOTAL_VALOR']
        
        data = []
        for v in totalBilling.itertuples(index=False,name=None):
            # print('totalBilling', v)
            data.append(v)

        self.pmpg.putData(data, 'resumo_consumo', month)
        logging.debug('---> Resume Consumed has been done <---');


    # Demonstrative FMS - PAB, AIH
    def dmsFMS(self, group, month):
        getView = self.sql.getVw_PDF(group, month)
        getResults = self.pmpg.execOperation(getView[0], getView[1])

        if len(getResults) == 0:
            return

        getList = self.sql.getListPdfs()
        df = pd.DataFrame.from_records(getResults,
                                       columns=[ 'TIPO', 'ORIGEM', 'DATA', 'HORA'
                                               , 'DESTINO', 'CIDADE_DESTINO', 'DURACAO'\
                                               , 'CUSTO', 'ID_PDF', 'LOCAL']).\
                          sort_values(by=['ORIGEM','TIPO','DATA','HORA'],ascending=True)
        #df['CUSTO'] = df['CUSTO'].replace(',','.', regex=True).astype(float)

        # DF CDRs
        dfResult = df.groupby(['ORIGEM','TIPO','ID_PDF'])
        dfList = pd.DataFrame.from_records(self.pmpg.execOperation(getList[0], getList[1]),columns=['ID_PDF']).sort_values(by=['ID_PDF'], ascending=True)

        dfResultTotal = df.groupby(['ID_PDF','TIPO'])[['CUSTO']].sum().sort_values(by=['ID_PDF','TIPO'], ascending=True).reset_index()

        # dfTotal = dfResultTotal.groupby(['ID_PDF'])[['CUSTO']].sum().reset_index()
        # print('dfResultTotal %s ' % dfResult)
        # for i,j in dfResultTotal.iterrows():
        #     print(j)


        return df,dfResult,dfResultTotal
    

    # Backup Billing
    def backUpBilling(self, month):
        billing = self.sql.backUpGroups(month)
        proc = billing[0][0]
        mnt = billing[0][1]
        op = billing[1]
        self.pmpg.execOperation([proc, mnt], op)
        #return {"Month": month}
        logging.debug("Backup Done %s" % month)


# run.setExt('9998','2824',"'Ramal'")
# run.setExt('9090','2824',"'Ramal'")
# run.setUpExt('9999')  
# run.setUpExt('8889')
# run.shutOffExt('9998')
# run.changeExt('8888','2824')
# grupos = {'FMS': ['FMS_PAB']}

# run = administrationExtensions()
# # # # # run.saveTotal('SME_CMEI',20204)

# for index in grupos:
#     for value in grupos[index]:
#         run.dmsFMS(value, 20192)