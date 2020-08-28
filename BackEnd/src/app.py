from __future__ import print_function
from sqls import sqls
from datetime import datetime, date
from tqdm.auto import tqdm
from mysql import connector as c
from openpyxl import load_workbook
from pyspin.spin import Spin1, Spinner
import calendar
import time
import pandas as pds
import pyodbc as pd
import sys
import locale
from builtins import FileNotFoundError

class PMPG():
    def __init__(self):
        #year = str(date.today().year)
        #month = str(date.today().month)
        #ym = year + "" + month
        self.url_vsc = 'Driver={SQL Server};server=189.85.23.20,25789;DATABASE=VSCDB;UID=everton.kopec;PWD=Nova@123'
        self.url_nova = 'DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=localhost;' \
                        'PORT=3306;DATABASE=novafibra;UID=app;PWD=Bigodao@00;charset=utf8mb4'
        self.url_nova_proc = c.connect(user='app', password='Bigodao@00', db='novafibra', host='localhost', auth_plugin='mysql_native_password')
        self.sql = sqls()
        #self.month = '20207'
        self.listGroupsCreated = []
        # self.file_to_write = ""
        self.groups = {'PMPG': ['PMPG', 'PMPG_0800', 'SME_ESCOLA', 'SME_CMEI']
                    , 'FMS': ['SMS_AIH', 'SMS_AIH_0800', 'SMS_PAB', 'SMS_PAB_0800']}

    # Create Connection
    def createConn(self):
        conn_vsc = pd.connect(self.url_vsc)
        conn_nova = pd.connect(self.url_nova)
        conn_nova_proc = self.url_nova_proc
        return conn_vsc, conn_nova, conn_nova_proc
    

    def execOperation(self, exec, ins, *values):
        """
        Execute Operation
        INS - Instrução - 0 - Para Select na Base do Vsc
        INS - Instrução - 1 - Para Insert na base da NovaFibra
        INS - Instrução - 2 - Select na base da NovaFibra
        INS - Instrução - 3 - Create Groups Views from Procedures
        INS - Instrução - 4 - Execute Procedures
        INS - Instrução - n - Create,Drop,update,delete Table na Base NovaFibra
        O restante ainda está pra ser definido,
        porém temos operações de Create e Drop/Table
        """
        cur_vsc = self.createConn()[0].cursor()
        cur_nova = self.createConn()[1].cursor()
        cur_nova_proc = self.createConn()[2].cursor()
        # print("Exec %s instrução %s" % (exec, ins))
        if ins == 0:
            cur_vsc.execute(str(exec))
            return cur_vsc.fetchall()
        elif ins == 1:
            for data in values:
                print('data: ', len(data))
                cur_nova.executemany(str(exec), data)
        elif ins == 2:
            cur_nova.execute(exec)
            data = cur_nova.fetchall()
            return data
        elif ins == 3:
            cur_nova_proc.callproc(exec[0], [exec[1],exec[2]])
            for group in cur_nova_proc.stored_results():
                data = pds.DataFrame(group.fetchall())
            return data
        elif ins == 4:
            cur_nova_proc.callproc(exec[0], [exec[1][0], exec[1][1]])
        elif ins == 5:
            cur_nova_proc.callproc(exec[0], [exec[1]])
        else:
            cur_nova.execute(exec)

        cur_nova.commit()
        cur_nova.close()
        cur_vsc.close()

    
    # Put Data into NovaFibra
    def putData(self, data, table, *month):
        if len(month) >= 0:
            tables = table
        # if len(month) > 0:
        #     table = table + '_' + month[0]
        ins = data
        num_columns = len(data[0])
        # print(num_columns)
        # A função abaixo passa o número de colunas dinamicamente
        # tirando a necessidade de inserir manualmente a quantidade
        insert = "REPLACE INTO {} VALUES ({})".format(tables, ','.join(['?' for column in range(num_columns)]))
        self.execOperation(insert, 1, ins)
        print("The values has been inserted on Table: %s!" % table)
    
    #Método Temporário
    # Insert Groups
    def insertGroups(self, month, *groups):
        listGroups = list(groups)

        for i in listGroups:
            print("\n Creating Table --> %s " % i)
            view = self.sql.insertGroupsProc(month, i)
            proc = view[0][0]
            mnt = view[0][1]
            gp = view[0][2][0]
            self.execOperation([proc, [mnt, gp]], view[1])
            self.listGroupsCreated.append(i)
            # print("\n The Table %s has been created \n\n" % i)

        return print(" The Tables %s have been inserted \n " % self.listGroupsCreated)

    # Import Data
    # From: VSC Database
    # To: Nova Fibra Database
    def importVSCtoNF(self, month):
        
        getData = self.sql.getDataFaturamento("FATURAMENTO", month)
        results = self.execOperation(getData[0], getData[1], getData[2])
        data = []
        for i in results:
            data.append(i)
        self.putData(data, getData[2])
        return print("Import Data executed successfully!")


    # time sum up and cost - Used for exportExcel
    def sumTimeCost(self, df):
        totalSecs = 0
        group = pds.DataFrame.from_records(df, columns=["Tipo", "Soma_Duracao", "Soma_Custo"])
        group["Soma_Duracao"] = group["Soma_Duracao"].str.split(':')
        # Adding time
        for i in group["Soma_Duracao"]:
            timeparts = [int(s) for s in i]
            totalSecs += (timeparts[0] * 60 + timeparts[1]) * 60
        totalSecs, sec = divmod(totalSecs, 60)
        min = divmod(totalSecs, 60)
        # Put time to total
        total_time = "%s min %s seg" % (min)
        # Adding cost total and put into Series
        # after add to DataFrame Group
        total_cost = group["Soma_Custo"].sum()
        df2 = pds.Series(['Total', total_time, total_cost], index=["Tipo", "Soma_Duracao", "Soma_Custo"])
        group = group.append(df2, ignore_index=True)
        # Put time format to:
        # 3405 min 36 sec
        for i in range(len(group["Soma_Duracao"]) - 1):
            group["Soma_Duracao"][i] = group["Soma_Duracao"][i][0] + ' min ' + group["Soma_Duracao"][i][1] + ' seg'

        return group
    
    # Formating Money for exportExcel
    def moneytoReal(self, cost):
        a = '{:,.2f}'.format(float(cost))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        return c.replace('v', '.')


    # Write Detailed Grouping on Excel
    def writeExcel(self, data, group,file,file_to_write):

        
        data = data
        df = pds.DataFrame.from_records(data, columns=['TIPO', 'ORIGEM', 'DATA', 'HORA', 'DESTINO', 'CIDADE_DESTINO',
                                                       'DURACAO_REAL', 'CUSTO'])
        df['ORIGEM'] = pds.to_numeric(df['ORIGEM'])
        df['DESTINO'] = pds.to_numeric(df['DESTINO'])

        # copyfile(file_to_read,file_to_write)

        # if file == 'PMPG':
        #     self.file_to_write = 'E:/DSA/Workspace/Faturamento/Backup/Fechamento/Fechamento_PMPG.xlsx'

        # if file == 'FMS':
        #     self.file_to_write = 'E:/DSA/Workspace/Faturamento/Backup/Fechamento/Fechamento_FMS.xlsx'

        self.append_df_to_excel(file_to_write, df, sheet_name=group, startrow=4, header=None,
                                index=False, startcol=1)
    


    def append_df_to_excel(self, filename, df, sheet_name='Sheet1', startrow=None, startcol=None,
                           truncate_sheet=False,
                           **to_excel_kwargs):
                           
        """
        Append a DataFrame [df] to existing Excel file [filename]
        into [sheet_name] Sheet.
        If [filename] doesn't exist, then this function will create it.

        Parameters:
        filename : File path or existing ExcelWriter
                    (Example: '/path/to/file.xlsx')
        df : dataframe to save to workbook
        sheet_name : Name of sheet which will contain DataFrame.
                    (default: 'Sheet1')
        startrow : upper left cell row to dump data frame.
                    Per default (startrow=None) calculate the last row
                    in the existing DF and write to the next row...
        truncate_sheet : truncate (remove and recreate) [sheet_name]
                        before writing DataFrame to Excel file
        to_excel_kwargs : arguments which will be passed to `DataFrame.to_excel()`
                            [can be dictionary]

        Returns: None
        """

        # ignore [engine] parameter if it was passed
        global FileNotFoundError
        if 'engine' in to_excel_kwargs:
            to_excel_kwargs.pop('engine')

        writer = pds.ExcelWriter(filename, engine='openpyxl') # pylint: disable=abstract-class-instantiated

        # Python 2.x: define [FileNotFoundError] exception if it doesn't exist
        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = IOError

        try:
            # try to open an existing workbook
            writer.book = load_workbook(filename)

            # get the last row in the existing Excel sheet
            # if it was not specified explicitly
            if startrow is None and sheet_name in writer.book.sheetnames:
                startrow = writer.book[sheet_name].max_row

            # truncate sheet
            if truncate_sheet and sheet_name in writer.book.sheetnames:
                # index of [sheet_name] sheet
                idx = writer.book.sheetnames.index(sheet_name)
                # remove [sheet_name]
                writer.book.remove(writer.book.worksheets[idx])
                # create an empty sheet [sheet_name] using old index
                writer.book.create_sheet(sheet_name, idx)

            # copy existing sheets
            writer.sheets = {ws.title: ws for ws in writer.book.worksheets}
        except FileNotFoundError:
            # file does not exist yet, we will create it
            pass

        if startrow is None:
            startrow = 0

        if startcol is None:
            startcol = 0

        # write out the new sheet
        df.to_excel(writer, sheet_name, startrow=startrow, startcol=startcol, **to_excel_kwargs)

        # save the workbook
        writer.save()

   