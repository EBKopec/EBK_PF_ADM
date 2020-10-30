import locale
from datetime import datetime
import calendar
from fpdf import FPDF, fpdf
from tqdm.auto import tqdm
from utils import utils
import pandas as pd
import numpy as np
from administration import administrationExtensions as ae
import logging
from sqls import sqls

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
logging.basicConfig(filename='E:\Projetos\Portal\PF\EBK_PF_Adm\BackEnd\src\main.proc.administration.log',level=logging.DEBUG)
class exportPDF(FPDF):

    def __init__(self):
        super().__init__()
        self.ae = ae()
        self.mydate = datetime.now()
        self.imagem = 'E:/DSA/Workspace/Faturamento/Backup/Fechamento/logo_novafibra.png'
        #self.imagem = '/app/files/images/logo_novafibra.png'

    # header
    def headerGroup(self):
        # Logo
        self.image(self.imagem, 10, 8, 33)
        # Font
        self.set_font('Arial', size=10)
        # Move to the right
        # self.cell(80)
        # Title
        self.cell(46.5, 10)
        self.cell(97.5,10, txt='Geração da Nota Fiscal Eletrônica',align='C')
        self.set_font("helvetica", size=9)
        self.multi_cell(46.5,5,txt='Município de Ponta Grossa \nCNPJ: 76.175.884/0001-87',align='R')
        # Line Break
        self.ln(10)
        self.set_left_margin(15)
        self.set_right_margin(15)
        self.set_fill_color(206, 107, 1)
        self.set_text_color(255, 255, 255)
        self.set_font_size(9.5)
        self.cell(0, 5, 'GERAÇÃO DA NF-E ' +
                      str.capitalize(self.mydate.strftime("%B") + '/'
                                     + str(self.mydate.year)),
                      align='C', fill=1, ln=1)
        # Put the watermark
        self.set_font('Arial', 'B', 50)
        self.set_text_color(255, 192, 203)
        self.rotatedText(35, 190, 'Sem Valor Fiscal', 45)

    # Header FMS
    def header_2(self):
        # Logo
        #self.image(self.imagem, 10, 8, 33)
        # Font
        self.set_font('Arial', size=10)
        self.cell(10, 10, ln=1)
        self.cell(10, 10, ln=1)
        # self.cell(190,5, "MUNICIPIO DE PONTA GROSSA ( " + group + " )", ln=1)
        # self.set_font("helvetica", size=9)
        # self.set_text_color(102,102,102)
        # self.cell(190, 5, "Avenida Visconde de Taunay, 950 -", ln=1)
        # self.cell(190, 5, "Ronda - 84.051-900 Ponta Grossa - PR", ln=1)
        # self.set_text_color(0, 0, 0)
        # self.cell(0,6,ln=1)
        # self.multi_cell(100, 5, txt="Nova Fibra Telecom SA."
        #                             "\nRua Jandaia do sul, 659"
        #                             "\nCEP 83.324-440 - Pinhais - PR"
        #                             "\nCNPJ 03.868.136/0001-06"
        #                             "\nIE 9047082754\n", align='L')


    def rotatedText(self, x, y, txt, angle):
        #Text rotated around its origin
        self.rotate(angle,x,y)
        self.text(x,y,txt)
        self.rotate(0)

    # draw a line
    def drawBorder(self):
        self.set_draw_color(0, 0, 0)
        self.rect(9.5, 20.5, 191.5, 264.5)
        self.rect(10, 21, 190.5, 263.5)

    def drawBodyNFe(self, group, month):
        self.drawBorder()
        self.set_font("helvetica", style='BI')
        self.multi_cell(0, 5, txt='\n')
        self.cell(0, 5, ln=1)
        rescon = self.ae.resCon(group, month)
        self.set_font("helvetica", size=9, style='B')
        self.set_text_color(0, 0, 0)
        epw = self.w - 2 * self.l_margin
        col_width = epw / 4
        self.cell(col_width, self.font_size, rescon[8], ln=1)
        self.set_font("helvetica", size=9)
        self.cell(10, self.font_size)
        self.cell(col_width, self.font_size, rescon[0], ln=1)
        self.cell(10, self.font_size)
        self.cell(col_width, self.font_size, rescon[1], ln=1)
        self.cell(10, self.font_size)
        self.cell(col_width, self.font_size,
                  'Franquias:' + rescon[3] + rescon[2] + rescon[4], ln=1)
        self.cell(10, self.font_size)
        self.cell(col_width, self.font_size,
                  'Excedentes:' + rescon[6] + rescon[5] + rescon[7], ln=1)
        self.cell(10, self.font_size, ln=1)
        self.cell(10, self.font_size, ln=1)


    #Body Cover Page Demonstrative - FMS
    def drawBodyDmt(self,group, month, extPdf):
        rescon = self.ae.resCon(group, month)
        df = self.ae.dmsFMS(group, month)
        
        if df == None:
            return
        
        dfTotal = df[2].groupby(['ID_PDF'])[['CUSTO']].sum().reset_index()
        dfTotal = dfTotal.set_index('ID_PDF')
        # print(df[0][df[0].ID_PDF.eq(extPdf)].groupby(['ID_PDF'])['ORIGEM','LOCAL'])
        
        # Get first Ext and Local to PDF
        dfLocal = df[0][df[0].ID_PDF.eq(extPdf)].groupby(['ID_PDF'])[['ORIGEM','LOCAL']]
        ramal = '/-/'
        local = '/-/'
        for i,j in dfLocal:
            ramal = j['ORIGEM'].iloc[0]
            local = j['LOCAL'].iloc[0]



        # Prepare ext total value
        dfResult = dfTotal.query('ID_PDF == @extPdf')
        resultado = 0
        for i,j in dfResult.iterrows():
            resultado = j['CUSTO']

        # Prepare ext total types values
        LDN = 0
        MOVEL = 0
        LOCAL = 0
        # print(df[2][df[2].ID_PDF.eq(extPdf)][['TIPO','CUSTO']])
        for i,j in df[2][df[2].ID_PDF.eq(extPdf)][['TIPO','CUSTO']].iterrows():
            if (j['TIPO']=='LDN'):
                # print(' Tipo %s e custo %s ' % (j['TIPO'], j['CUSTO']))
                LDN = j['CUSTO']
                # print('dentro do if -> %s' % LDN)
            if (j['TIPO']=='MOVEL'):
                MOVEL = j['CUSTO']
            if (j['TIPO']=='LOCAL'):
                LOCAL = j['CUSTO']
        # print('fora do if -> %s' % LDN)

        ref = datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%m/%Y")
        year = int(datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%Y"))
        mnt = int(datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%m"))
        last_date = calendar.monthrange(year, mnt)[1]

        # Mount Header Page
        self.image(self.imagem, 10, 8, 33)
        self.set_font('Arial', size=8)
        x = self.get_x()
        y = self.get_y()
        self.set_xy(x+33,y-2)
        self.set_text_color(0, 0, 0)
        self.multi_cell(100, 3, txt="Nova Fibra Telecom S/A."
                                    "\nRua Jandaia do Sul, 659"
                                    "\nCEP 83.324-440 - Pinhais - PR"
                                    "\nCNPJ 03.868.136/0001-06 - IE 9047082754\n", align='L')

        # self.cell(155, 10)
        # self.cell(30,5,"Ramal: XXXX",ln=1)
        self.cell(10, 10, ln=1)
        x = self.get_x()
        y = self.get_y()
        self.set_xy(x,y)
        self.multi_cell(100, 4, "MUNICÍPIO DE PONTA GROSSA\n"
                                "Avenida Visconde de Taunay, 950 - Ronda\n"
                                "CEP 84.051-900 - Ponta Grossa - PR", align='L')

        self.set_text_color(0, 0, 0)
        x = self.get_x()
        y = self.get_y()
        self.set_xy(x+118,y-12)
        self.multi_cell(100,4,"Ramal: %s \n%s \n" 
                            "DATA DE EMISSÃO: 01/%s \nPERÍODO DE REFERÊNCIA: 01/%s A %s/%s"% (ramal, str(local).upper(), ref, ref, last_date, ref))
        self.cell(10, 10, ln=1)
        x = self.get_x()
        y = self.get_y()
        self.set_xy(x,y)
        self.set_font("helvetica", size=12, style='B')
        self.cell(190, 10, 'Valores', align='C' ,ln=1)
        x = self.get_x()
        y = self.get_y()

        self.set_xy(x,y+2)
        self.rect(10, y, 190, 23)
        self.set_font("helvetica", size=10, style='B')
        self.cell(150, 5, 'Valor Total: ') 
        self.set_font('helvetica', size=10)
        self.cell(40,5, str(locale.currency(resultado,grouping=True)), align='R',ln=1)
        self.set_font("helvetica", size=10)
        # Local
        self.set_font("helvetica", size=10, style='B')
        self.cell(150, 5, 'Valor das Chamadas Locais: ')
        self.set_font('helvetica', size=10)
        self.cell(40, 5,  str(locale.currency(LOCAL,grouping=True)), align='R', ln=1)
        # Mobile
        self.set_font("helvetica", size=10, style='B')
        self.cell(150, 5, 'Valor das Chamadas Móvel:')
        self.set_font('helvetica', size=10)
        self.cell(40, 5, str(locale.currency(MOVEL,grouping=True)), align='R', ln=1)
        # LDN
        self.set_font("helvetica", size=10, style='B')
        self.cell(150, 5, 'Valor das Chamadas Interurbano:')
        self.set_font('helvetica', size=10)
        self.cell(40, 5, str(locale.currency(LDN,grouping=True)), align='R', ln=1)

        # self.rect(90, 111, 101, 55)
        # self.multi_cell(101,5, 'Veja o que está sendo cobrado\n\nServiços')
        

    #Draw Body dmsRpt_SMS
    def drawBodydms(self,group, month, extPdf):
        df = self.ae.dmsFMS(group, month)
        
        if df == None:
            return
        
        if df[0][df[0].ID_PDF.eq(extPdf)].empty == False:
            # print(df[0][df[0].ID_PDF.eq(extPdf)])
            dfResult = df[0][df[0].ID_PDF.eq(extPdf)].groupby(['ORIGEM','TIPO','ID_PDF'])
            for j, k in dfResult:
                self.header_2()
                self.set_left_margin(10)
                self.set_right_margin(10)
                self.set_fill_color(206, 107, 1)
                self.set_text_color(255, 255, 255)
                self.set_font_size(9.5)
                self.set_draw_color(0, 0, 0)
                self.cell(0, 5, 'Serviços NOVA FIBRA detalhado',align='C', fill=1, ln=1)
                self.ln(4)
                self.cell(15,5, 'Origem' ,align='C', fill=1,border=1)
                self.cell(25,5, 'Tipo', align='C', fill=1,border=1)
                self.cell(30,5, 'Destino', align='C', fill=1,border=1)
                self.cell(40,5, 'Cidade de Destino',align='C', fill=1,border=1)
                self.cell(20,5, 'Data', align='C',fill=1,border=1)
                self.cell(20,5, 'Hora', align='C',fill=1,border=1)
                self.cell(20,5, 'Duração', align='C',fill=1,border=1)
                self.cell(20,5, 'Custo', align='C', fill=1,border=1,ln=1)
                # k.loc['Total'] = k[['CUSTO']].sum()
                for idx, row in k.iterrows():
                    self.set_text_color(0, 0, 0)
                    self.set_draw_color(206, 107, 1)
                    self.set_font_size(7)
                    self.set_font('Arial', style='B')
                    # self.cell(15, 4, str(idx), align='R', border='B')  # Total
                    self.cell(15, 4, str(row[1]).replace('nan',''), align='R', border='B') #Origem
                    #self.set_fill_color(255,255,255)
                    self.cell(25, 4, str(row[0]).replace('nan',''), align='L', border='B') #Tipo
                    self.set_font('Arial', style="")
                    self.cell(30, 4, str(row[4]).replace('nan',''), align='R', border='B') #Destino
                    self.set_font('Arial',style='B')
                    self.cell(40, 4, str(row[5]).replace('nan',''), align='L', border='B') #Cidade de Destino
                    self.set_font('Arial',style="")
                    self.cell(20, 4, str(row[2]).replace('nan',''), align='C', border='B') #Data
                    self.cell(20, 4, str(row[3]).replace('nan',''), align='C', border='B') #Hora
                    self.cell(20, 4, str(row[6]).replace('nan',''), align='R', border='B') #Duração
                    # self.cell(20, 4, 'R$  ' + str(round(row[7],2)), align='R', border='B', ln=1)  #Custo
                    self.cell(20, 4, 'R$  ' + str(round(row[7],2)), align='R', border='B', ln=1)  #Custo
                self.add_page()
        


        # adding the total per group
        # for j, k in df[1]:
        #     # k.loc['Total'] = k[['CUSTO']].sum()
        #     # print('K--> %s %s ' % (j,k))
        #     # Accessing each data group to print in single page by from
        #     for idx, row in k[k['ID_PDF'] == extPdf].iterrows():
        #         # print(row)
        #         self.set_text_color(0, 0, 0)
        #         self.set_draw_color(206, 107, 1)
        #         self.set_font_size(7)
        #         self.set_font('Arial', style='B')
        #         # self.cell(15, 4, str(idx), align='R', border='B')  # Total
        #         self.cell(15, 4, str(row[1]).replace('nan',''), align='R', border='B') #Origem
        #         #self.set_fill_color(255,255,255)
        #         self.cell(25, 4, str(row[0]).replace('nan',''), align='L', border='B') #Tipo
        #         self.set_font('Arial', style="")
        #         self.cell(30, 4, str(row[4]).replace('nan',''), align='R', border='B') #Destino
        #         self.set_font('Arial',style='B')
        #         self.cell(40, 4, str(row[5]).replace('nan',''), align='L', border='B') #Cidade de Destino
        #         self.set_font('Arial',style="")
        #         self.cell(20, 4, str(row[2]).replace('nan',''), align='C', border='B') #Data
        #         self.cell(20, 4, str(row[3]).replace('nan',''), align='C', border='B') #Hora
        #         self.cell(20, 4, str(row[6]).replace('nan',''), align='R', border='B') #Duração
        #         # self.cell(20, 4, 'R$  ' + str(round(row[7],2)), align='R', border='B', ln=1)  #Custo
        #         self.cell(20, 4, 'R$  ' + str(round(row[7],2)), align='R', border='B', ln=1)  #Custo
        # self.add_page()
        # self.cell(100,5, df, align='C',border=1,ln=1)
        # self.cell(ln=1)



    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class export():
    def __init__(self):
        self.groups = {'FMS': ['FMS_AIH','FMS_PAB']}
#             , 'FMS': ['SMS_AIH', 'SMS_PAB']}
        self.ae = ae()
        self.month = '20192'

# #     def summarizedReport(self):
# #         self.pdf = exportPDF()
# #         self.pdf.alias_nb_pages()
# #         self.pdf.add_page()
# #         self.pdf.headerGroup()
# #         # Fill data
# #         for index in self.groups:
# #             for value in tqdm(self.groups[index]):
# #                 self.pdf.cell(1, ln=2)
# #                 self.pdf.drawBodyNFe(value, self.month)

# #         self.pdf.output("E:/DSA/Workspace/Faturamento/Backup/Fechamento/NFe.pdf")

    def dmsRpt(self):
        getList = self.ae.sql.getListPdfs()
        df =  pd.DataFrame.from_records(self.ae.pmpg.execOperation(getList[0], getList[1]),
                                           columns=['ID_PDF']).sort_values(by=['ID_PDF'], ascending=True)
        dfList = df['ID_PDF'].tolist()
        # print(dfList)
        for index in self.groups:
            for value in tqdm(self.groups[index]):
                if (index == 'FMS'):
                    for i in range(len(dfList)):
                        pdf = exportPDF()
                        pdf.alias_nb_pages()
                        pdf.add_page()
                        pdf.drawBodyDmt(value, self.month, dfList[i])
                        pdf.add_page()
                        pdf.drawBodydms(value, self.month, dfList[i])
                        pdf.output("E:/DSA/Workspace/Faturamento/Backup/Fechamento/Teste_Grupo_Nº"+ str(dfList[i]) +"_"+ value +".pdf")


run = export()
# # run.summarizedReport()
run.dmsRpt()