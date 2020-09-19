import logging
#logging.basicConfig(filename='main.proc.log',level=logging.DEBUG)
logging.basicConfig(filename='/var/log/flask/main.proc.log',level=logging.DEBUG)
class sqls():

    # Create Table
    def createTable(self, month):
        month = month
        create = " CREATE TABLE FATURAMENTO_%s " \
                 "(  MES_FATURAMENTO_ID INT " \
                 " , MES_ID int " \
                 " , FATURAMENTO_ID int " \
                 " , BATCH_ID int " \
                 " , TIPO varchar(255) " \
                 " , ORIGEM varchar(255) " \
                 " , DATA date " \
                 " , HORA time " \
                 " , DESTINO varchar(255) " \
                 " , CIDADE_DESTINO varchar(255) " \
                 " , DURACAO_REAL time " \
                 " , CUSTO_ORIGINAL decimal(13,3) " \
                 " , CUSTO decimal(13,3) " \
                 " , USER_ID int " \
                 " , USER_DESC varchar(255) " \
                 " , DISTRIBUTOR_ID int " \
                 " , CONSTRAINT Faturamento_PK PRIMARY KEY(FATURAMENTO_ID) " \
                 " , CONSTRAINT Faturamento_UK UNIQUE KEY(ORIGEM,DESTINO,DATA,HORA))" % month
        logging.debug("The table FATURAMENTO_%s has been created!" % month)
        return create, 5

    # Drop Table
    def dropTable(self, month):
        drop = "DROP TABLE IF EXISTS FATURAMENTO_%s " % month
        logging.debug("The table FATURAMENTO_%s has been dropped!" % month)
        return drop, 5, month

    # Drop Table
    def dropTableVw(self, group):
        drop = "DROP TABLE IF EXISTS VW_{}s ".format(group)
        logging.debug("The table VW_{}s has been dropped!".format(group))
        return drop, 5, group

    # Get Data
    def getDataFaturamento(self, table, month):
        month = month
        table = table
        select = " SELECT CAST(CONCAT(FORMAT(LOCALTIME, 'yyyyM'), ID ) AS BIGINT) MES_FATURAMENTO_ID " \
                     " , FORMAT(LOCALTIME, 'yyyyM') AS 'MES_ID' " \
                     " , ID AS 'ID' " \
                     " , BATCHID  " \
                     " , CASE  " \
                     "    WHEN DESTINATIONDESC IN ( 'PONTA GROSSA'  " \
                     " , 'VILA RURAL DE GUARAGI'  " \
                     " , 'BISCAIA'  " \
                     " , 'GUARAGI'  " \
                     " , 'ROXO ROIZ'  " \
                     " , 'PINHEIRINHO' " \
                     " , 'UVAIA'  " \
                     " , 'COLONIA TRINDADE'  " \
                     " , 'BOCAINA'  " \
                     " , 'CONCHAS VELHAS'  " \
                     " , 'CERRADO GRANDE'  " \
                     " , 'MATO QUEIMADO'  " \
                     " , 'KALINOSKI'  " \
                     " , 'CERRADINHO'  " \
                     " , 'PASSO DO PUPO'  " \
                     " , 'TAQUARI DOS POLACOS'  " \
                     " , 'TABULEIRO'  " \
                     " , 'COLONIA SANTA CRUZ'  " \
                     " , 'FAXINAL GRANDE')  " \
                     " AND SUBSTRING(DESTINATIONNUMBER,5,1) BETWEEN 2 AND 5  " \
                     " THEN '1'  " \
                     " WHEN SUBSTRING(DESTINATIONNUMBER,1,2) = 55 " \
                     " AND SUBSTRING(DESTINATIONNUMBER,5,1) BETWEEN 6 AND 9  " \
                     " THEN '2'  " \
                     " ELSE '3'  " \
                     " END AS 'TIPO'  " \
                     " , CASE  " \
                     " WHEN SUBSTRING(CAST(ANI AS VARCHAR),5,4) = '0000'  " \
                     " THEN SUBSTRING(CAST(ANI AS VARCHAR),9,4)  " \
                     " WHEN LEN(ANI) = 4  " \
                     " THEN ANI  " \
                     " WHEN LEN(ANI) > 8  " \
                     " AND SUBSTRING(CAST(ANI AS VARCHAR), 1,2) = '55' AND ISNUMERIC(ANI) = 1 " \
                     " THEN SUBSTRING(CAST(ANI AS VARCHAR), 3, 10)  " \
                     " WHEN LEN(ANI) > 8    " \
                     "  AND SUBSTRING(CAST(ANI AS VARCHAR), 1,4) = '0055' AND ISNUMERIC(ANI) = 1 " \
                     " THEN SUBSTRING(CAST(ANI AS VARCHAR), 5, 12)" \
                     " WHEN UPPER(CAST(ANI AS VARCHAR)) LIKE '%ANONYMOUS%' " \
                     "   OR UPPER(CAST(ANI AS VARCHAR)) LIKE '%PRIVATE%' " \
                     " THEN '0' " \
                     " WHEN ISNUMERIC(ANI) = 0 " \
                     "  AND (UPPER(CAST(ANI AS VARCHAR)) NOT LIKE '%ANONYMOUS%' " \
                     "   OR UPPER(CAST(ANI AS VARCHAR)) NOT LIKE '%PRIVATE%') " \
                     " THEN '-1' " \
                     " ELSE ANI  " \
                     " END AS 'ORIGEM' " \
                     " , FORMAT(LOCALTIME, 'yyyy-MM-dd') AS 'DATA'  " \
                     " , FORMAT(LOCALTIME, 'HH:mm:ss') AS 'HORA'  " \
                     " , CASE   " \
                     "  WHEN SUBSTRING(CAST(DESTINATIONNUMBER AS VARCHAR), 1,2) = '55' " \
                     " THEN SUBSTRING(CAST(DESTINATIONNUMBER AS VARCHAR), 3,12) " \
                     " ELSE CAST(DESTINATIONNUMBER AS VARCHAR) " \
                     " END AS 'DESTINO' " \
                     " , CAST(DESTINATIONDESC AS VARCHAR(255)) COLLATE SQL_Latin1_General_Cp1251_CS_AS AS 'CIDADE_DESTINO' " \
                     " , CONVERT(TIME, DATEADD(SECOND, USERDURATION + 86400000, 0), 114) AS 'DURACAO_REAL' " \
                     " , USERCOST AS 'CUSTO_ORIGINAL'  " \
                     " , CASE  " \
                     " WHEN (DESTINATIONNUMBER IN ( SELECT AliasE164  " \
                     " FROM useralias  " \
                     " WHERE (AliasE164 LIKE '55423220%' OR AliasE164 LIKE '%4200000000%')  " \
                     " AND UserID IN ( 2824 " \
                     " , 2833 " \
                     " , 2831 " \
                     " , 2834 " \
                     " , 2832 " \
                     " , 2835 " \
                     " , 2855 " \
                     " , 2902  " \
                     " , 2857)))  " \
                     " THEN 0  " \
                     " ELSE USERCOST  " \
                     " END AS 'CUSTO'  " \
                     " , USERID AS 'USER_ID' " \
                     " , REPLACE(USERDESC, 'SMS', 'FMS') AS 'USER_DESC' " \
                     " , DISTRIBUTORID AS 'DISTRIBUTOR_ID' " \
                     " FROM INTEGRATED_{}  " \
                     " WHERE BATCHID IN (270,303)  " \
                     " AND DISTRIBUTORID IN ('1','25')  " \
                     " AND ISNULL(DESTINATIONNUMBER,'') != '' " \
                     " AND DNIS NOT IN ( '4280558006432626' " \
                     " , '4280558006451250' " \
                     " , '4280558006439595' " \
                     " , '4280558006435052' " \
                     " , '4280558006437880') " \
                     " AND USERCOST != 0 " \
                     " AND (day(UTCTime) - day(localtime)) = 0" \
                     " AND ANI NOT IN ( '554200009990', '554200009991', '554200009992', '554200009993'" \
                     "                , '554200009994', '554200009995', '554200009996', '554200009997'" \
                     "                , '554200009998', '554200009999')" \
                     " UNION ALL " \
                     " SELECT CAST(CONCAT(FORMAT(ORIG.LOCALTIME, 'yyyyM'), ORIG.ID ) AS BIGINT) MES_FATURAMENTO_ID " \
                     " , FORMAT(ORIG.LOCALTIME, 'yyyyM') AS 'MES_ID' " \
                     " , ORIG.ID AS 'ID' " \
                     " , ORIG.BATCHID " \
                     " , '3' AS 'TIPO'  " \
                     " , CASE  " \
                     " WHEN SUBSTRING(CAST(ORIG.ANI AS VARCHAR),5,4) = '0000'  " \
                     " THEN SUBSTRING(CAST(ORIG.ANI AS VARCHAR),9,4)  " \
                     " WHEN LEN(ORIG.ANI) = 4  " \
                     " THEN ORIG.ANI  " \
                     " WHEN LEN(ORIG.ANI) > 8 " \
                     " AND SUBSTRING(CAST(ORIG.ANI AS VARCHAR), 1,2) = '55' AND ISNUMERIC(ORIG.ANI) = 1 " \
                     " THEN SUBSTRING(CAST(ORIG.ANI AS VARCHAR), 3, 10)  " \
                     " WHEN UPPER(CAST(ORIG.ANI AS VARCHAR)) LIKE '%ANONYMOUS%' " \
                     "   OR UPPER(CAST(ORIG.ANI AS VARCHAR)) LIKE '%PRIVATE%' " \
                     " THEN '0' " \
                     " WHEN ISNUMERIC(ORIG.ANI) = 0 " \
                     "  AND (UPPER(CAST(ORIG.ANI AS VARCHAR)) NOT LIKE '%ANONYMOUS%' " \
                     "   OR UPPER(CAST(ORIG.ANI AS VARCHAR)) NOT LIKE '%PRIVATE%') " \
                     " THEN '-1' " \
                     " ELSE ORIG.ANI " \
                     " END AS 'ORIGEM' " \
                     " , FORMAT(ORIG.LOCALTIME, 'yyyy-MM-dd') AS 'DATA'  " \
                     " , FORMAT(ORIG.LOCALTIME, 'HH:mm:ss') AS 'HORA'  " \
                     " , CASE " \
                     "    WHEN LEN(DEST.DESTINATIONNUMBER) = 12 " \
                     "     AND SUBSTRING(CAST(DEST.DESTINATIONNUMBER AS VARCHAR), 1,5) = '55800' " \
                     "    THEN CONCAT('550',SUBSTRING(CAST(DEST.DESTINATIONNUMBER AS VARCHAR), 3,10)) " \
                     "    WHEN DEST.DESTINATIONNUMBER LIKE '%4230300153%' " \
                     "    THEN '5508006432626' " \
                     "    WHEN LEN(DEST.DESTINATIONNUMBER) = 12 " \
                     "     AND SUBSTRING(CAST(DEST.DESTINATIONNUMBER AS VARCHAR), 1,2) = '55' " \
                     "    THEN SUBSTRING(CAST(DEST.DESTINATIONNUMBER AS VARCHAR), 3,10)  " \
                     "    ELSE CAST(DEST.DESTINATIONNUMBER AS VARCHAR) " \
                     " END AS 'DESTINO' " \
                     " , 'BRASIL' AS 'CIDADE_DESTINO'  " \
                     " , CONVERT(TIME, DATEADD(SECOND, ORIG.USERDURATION + 86400000, 0), 114) AS 'DURACAO_REAL'  " \
                     " , ORIG.USERCOST AS 'CUSTO_ORIGINAL'  " \
                     " , CASE  " \
                     " WHEN (ORIG.DESTINATIONNUMBER IN ( SELECT AliasE164  " \
                     " FROM useralias  " \
                     " WHERE (AliasE164 LIKE '55423220%' OR AliasE164 LIKE '%4200000000%')  " \
                     " AND UserID IN ( 2824 " \
                     " , 2833 " \
                     " , 2831 " \
                     " , 2834 " \
                     " , 2832 " \
                     " , 2835 " \
                     " , 2855 " \
                     " , 2902 " \
                     " , 2857 ))) " \
                     " THEN 0  " \
                     " ELSE  " \
                     " ORIG.USERCOST  " \
                     " END AS 'CUSTO'  " \
                     " , ORIG.USERID AS 'USER_ID' " \
                     " , REPLACE(ORIG.USERDESC, 'SMS', 'FMS') AS 'USER_DESC' " \
                     " , ORIG.DISTRIBUTORID AS 'DISTRIBUTOR_ID' " \
                     " FROM INTEGRATED_{} ORIG " \
                     " JOIN INTEGRATED_{} DEST ON DEST.RelatedOriginatingID = ORIG.TransactionID " \
                     " WHERE ORIG.DNIS IN ( '4280558006432626' " \
                     " , '4280558006451250' " \
                     " , '4280558006439595' " \
                     " , '4280558006435052' " \
                     " , '4280558006437880') " \
                     " AND ORIG.BATCHID IN (270,303)" \
                     " AND DEST.BATCHID IN (270,303)" \
                     " AND ORIG.DISTRIBUTORID IN ('1','25') " \
                     " AND DEST.DISTRIBUTORID IN ('1','25') " \
                     " AND ORIG.TRANSACTIONTYPECODE = 3 " \
                     " AND ORIG.USERCOST != 0 " \
                     " AND (day(ORIG.UTCTime) - day(ORIG.localtime)) = 0" \
                     " AND ORIG.ANI NOT IN ( '554200009990', '554200009991', '554200009992', '554200009993'" \
                     "                , '554200009994', '554200009995', '554200009996', '554200009997'" \
                     "                , '554200009998', '554200009999')".format(month, month, month)
        return select, 0, table

    # Get Views
    def getViews(self, grupo, month):
        view = " SELECT TIPO " \
               " , ORIGEM " \
               " , DATE_FORMAT(DATA, '%d/%m/%Y') DATA " \
               " , DATE_FORMAT(HORA, '%H:%i:%s') HORA " \
               " , DESTINO " \
               " , CIDADE_DESTINO " \
               " , DURACAO_REAL " \
               " , REPLACE(CUSTO,'.',',')  CUSTO " \
               " FROM VW_{}s  " \
               " WHERE CUSTO > 0 " \
               "   and MES_ID = {} " \
               " ORDER BY 2 ASC, 3 ASC, 4 ASC".format(grupo, month)
        return view, 2

    # Create Views
    def insertGroupsProc(self, month, *group):
        view = ['spc_vw_agrupamento', month, group]
        return view, 4

    # Backup
    def backUpGroups(self, month):
        bkp = ['BACKUP_TABLE', month]
        return bkp, 5

    # Get Grouping
    def getGroup(self, group, month):
        group = ['agrupamento', group, month]
        # group = " select TL.TIPO_DESC " \
        #         "      , CONCAT(sum(extract(MINUTE from (sec_to_time(time_to_sec(FAT.DURACAO_REAL))% 86400))) + " \
        #         " EXTRACT(MINUTE FROM (sec_to_time(sum(extract(SECOND " \
        #         " from (sec_to_time(time_to_sec(FAT.DURACAO_REAL))% 86400)))))), ':', " \
        #         " (EXTRACT(SECOND FROM (sec_to_time(sum(extract(SECOND " \
        #         " from (sec_to_time(time_to_sec(FAT.DURACAO_REAL))% 86400)))))))) Soma_de_Duracao " \
        #         " , SUM(ROUND(FAT.CUSTO,2)) Soma_de_Custo " \
        #         " from FATURAMENTO_{} FAT " \
        #         " JOIN tarifa tar ON tar.BATCH_ID = fat.BATCH_ID " \
        #         " AND (tar.TIPO_ID = fat.TIPO) " \
        #         " JOIN tipo_ligacao tl ON tl.tipo_id = fat.TIPO " \
        #         " WHERE DESTINO NOT LIKE '550800%' " \
        #         " AND FAT.USER_ID IN ('{}') " \
        #         " group by FAT.TIPO " \
        #         " order by FAT.TIPO asc"
        return group, 3

    # Get Users Group
    def getUsersGroup(self, table):
        table = table
        select = " SELECT UGroupID AS 'GROUP_ID' " \
                 ", CAST(Description AS VARCHAR(255)) COLLATE SQL_Latin1_General_Cp1251_CS_AS AS 'GROUP_DESCRIPTION' " \
                 " FROM UGroup"
        return select, 0, table


    # Get Users
    def getUsers(self, table):
        table = table
        select = " SELECT [UserID] AS 'USER_ID' " \
                 " , [Description] AS 'USER_DESC' " \
                 " , [UserCode] AS 'USER_CODE' " \
                 " , [UGroupID] AS 'USER_GROUP_ID' " \
                 " , [ActivationDate]  AS 'ACTIVATION_DATE' " \
                 " , [ExpirationDate] AS 'EXPIRATION_DATE' " \
                 " , [EnabledDate] AS 'ENABLED_DATE' " \
                 " FROM [VSCDB].[dbo].[User] "
        # " WHERE UGroupID = 270 "
        # return execOperation(select, 0), table
        return select, 0, table

    # # Get Qty Extensions
    # def getQtyExt(self, groupId):
    #     select = " SELECT COUNT(CA.LINHA) AS QTY  " \
    #              "      , US.User_Group AS USUARIO " \
    #              " FROM CONTROLE_AGRUPAMENTO CA " \
    #              " JOIN USERS US ON US.USER_ID = CA.USER_GROUP_ID   " \
    #              " where US.USER_ID = {} " \
    #              " GROUP BY US.User_Group ".format(groupId)
    #     return select, 2

    # Get Fares
    # def getFares(self):
    #     select = " SELECT T.USER_ID AS 'USER_CODE' " \
    #              "      , tl.tipo_desc AS 'CALL_TYPE' " \
    #              "      , T.CUSTO  AS 'COST' " \
    #              "      , T.FRANQUIA_MIN AS 'MIN_TELEPHONE_FRANCHISE' " \
    #              "      , T.FRANQUIA_VALOR AS 'VALUES_TELEPHONE_FRANCHISE' " \
    #              "      , T.VALOR_RAMAL AS 'VALUE_EXTENSION' " \
    #              " FROM TIPO_LIGACAO tl " \
    #              " join tarifa t on t.TIPO_ID = tl.TIPO_ID "
    #     return select, 2

    # # Activate Extensions
    # def setExt(self, ext):
    #     ext = ext
    #     update = " UPDATE CONTROLE_AGRUPAMENTO " \
    #              " SET STATUS = 'Y' " \
    #              "   , DATA_CANCELAMENTO = NULL " \
    #              "   , DATA_VALIDACAO_CLIENTE = SYSDATE() " \
    #              " WHERE LINHA = {} ".format(ext)
    #     return update, 5

    # # Deactivate Extensions
    # def deactivateExt(self, ext):
    #     update = " UPDATE CONTROLE_AGRUPAMENTO " \
    #              " SET STATUS = 'N' " \
    #              "   , DATA_CANCELAMENTO = SYSDATE() " \
    #              " WHERE LINHA = {} ".format(ext)
    #     return update, 5

    # # Change Groups
    # def changeGroup(self, ext, group):
    #     ext = ext
    #     group = group
    #     update = " UPDATE CONTROLE_AGRUPAMENTO " \
    #              " SET USER_GROUP_ID = {} " \
    #              "   , DATA_ALTERACAO_GRUPO = SYSDATE() " \
    #              " WHERE LINHA = {} ".format(group, ext)
    #     return update, 5

    # # Register Extensions
    # def registerExtensions(self, *data):
    #     insert = "INSERT INTO CONTROLE_AGRUPAMENTO (LINHA,USER_GROUP_ID,TIPO_LINHA,DATA_ENVIO_NOVA,STATUS) " \
    #              " VALUES ({},{},{},NOW(),'P')".format(data[0], data[1], data[2])

    #     return insert, 5

    # Consumption to be billed
    def excessCons(self, group):
        select = " SELECT distinct tl.tipo_desc AS 'CALL_TYPE' " \
                 "      , T.CUSTO AS 'COST' " \
                 "      , T.FRANQUIA_MIN AS 'MIN_TELEPHONE_FRANCHISE' " \
                 "      , T.FRANQUIA_VALOR AS 'VALUES_TELEPHONE_FRANCHISE' " \
                 " FROM TIPO_LIGACAO tl " \
                 " join tarifa t on t.TIPO_ID = tl.TIPO_ID " \
                 " join users us on us.user_id = t.user_id " \
                 " WHERE us.user_group LIKE '%{}%' " \
                 " order by 1 asc ".format(group)
        return select, 2

    # Ext List
    def extList(self, group):
        select = "select CA.linha as 'RAMAL' " \
                 "     , US.USER_GROUP as 'GRUPO' " \
                 "     , CA.data_envio_nova as 'DATA_INSTALACAO' " \
                 "     , CA.data_validacao_cliente as 'DATA_ATIVACAO' " \
                 "     , CA.data_cancelamento as 'DATA_CANCELAMENTO' " \
                 "     , T.VALOR_RAMAL    AS 'VALOR_RAMAL' " \
                 "     , CA.STATUS AS 'STATUS'" \
                 "     , CalculoRamal(CA.data_validacao_cliente,CA.data_cancelamento,T.VALOR_RAMAL,ca.STATUS) AS  'PROPORCIONAL' " \
                 " from controle_agrupamento CA " \
                 " JOIN USERS US ON US.USER_ID = CA.USER_GROUP_ID " \
                 " JOIN tarifa T ON us.user_id = t.user_id " \
                 " where CA.STATUS IN ('Y','N') " \
                 "   AND US.USER_GROUP LIKE '%{}%' " \
                 " GROUP BY CA.linha " \
                 " order by 4 asc, 5 DESC ".format(group)
        return select, 2
