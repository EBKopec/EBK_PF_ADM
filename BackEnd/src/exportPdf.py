import locale
from datetime import datetime
import calendar
from fpdf import FPDF, fpdf
from tqdm.auto import tqdm
from utils import utils
import pandas as pd
import numpy as np
from administration import administrationExtensions as ae

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class exportPDF(FPDF):

    def __init__(self):
        super().__init__()
        self.ae = ae()
        self.mydate = datetime.now()
        self.imagem = 'E:/DSA/Workspace/Faturamento/Backup/Fechamento/logo_novafibra.png'

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
        self.image(self.imagem, 10, 8, 33)
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
    def drawBodyDmt(self,group, month):
        rescon = self.ae.resCon(group, month)
        ref = datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%B/%Y")
        year = int(datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%Y"))
        mnt = int(datetime.strftime(pd.to_datetime(utils.monthId(month) + '01'), "%m"))
        last_date = ""
        if (calendar.monthrange(year, mnt)[1] > 30):
            last_date = 30
        elif(calendar.monthrange(year, mnt)[1] < 30):
            last_date = 28

        # print('Mês de referência %s %s' % (ref, last_date));
        self.cell(190, 5, "MUNICIPIO DE PONTA GROSSA ( " + group + " )", ln=1)
        self.set_font("helvetica", size=9)
        self.set_text_color(102, 102, 102)
        self.cell(190, 5, "Avenida Visconde de Taunay, 950 -", ln=1)
        self.cell(190, 5, "Ronda - 84.051-900 Ponta Grossa - PR", ln=1)
        self.set_text_color(0, 0, 0)
        self.cell(0, 6, ln=1)
        self.multi_cell(100, 5, txt="Nova Fibra Telecom SA."
                                    "\nRua Jandaia do sul, 659"
                                    "\nCEP 83.324-440 - Pinhais - PR"
                                    "\nCNPJ 03.868.136/0001-06"
                                    "\nIE 9047082754\n", align='L')
        self.cell(50, 5, ln=1)
        self.cell(50, 5)
        x = self.get_x()
        y = self.get_y()
        self.multi_cell(30,5,'Mês de Referência\n %s' % ref,border=1)
        self.set_xy(x+50,y)
        self.multi_cell(31,5, 'Data do Vencimento\n %s/%s' % (last_date, ref),border=1)
        self.set_xy(x+100,y)
        self.multi_cell(31, 5, 'Valor da sua Conta\n ' +
                        rescon[15], border=1)
        self.cell(0, 20, ln=1)
        self.cell(80, 5)
        self.set_font("helvetica", size=10, style='B')
        self.rect(90, 111, 101, 55)
        self.multi_cell(101,5, 'Veja o que está sendo cobrado\n\nServiços')
        self.set_font("helvetica", size=10)
        # Local
        self.cell(80, 5)
        self.cell(45, 5, 'Chamadas locais para Fixo')
        self.cell(56, 5,  str(rescon[11]), align='R', ln=1)
        self.cell(80, 5)
        self.cell(45, 5, 'Valor')
        self.cell(56, 5, str(rescon[12]), align='R', ln=1)
        self.ln(5)
        # Mobile
        self.cell(80, 5)
        self.cell(45, 5, 'Chamadas locais para Móvel')
        self.cell(56, 5, str(rescon[13]), align='R', ln=1)
        self.cell(80, 5)
        self.cell(45, 5, 'Valor')
        self.cell(56, 5, str(rescon[14]), align='R', ln=1)
        self.ln(5)
        # LDN
        self.cell(80, 5)
        self.cell(45, 5, 'Chamadas locais para Interurbano')
        self.cell(56, 5, str(rescon[9]), align='R', ln=1)
        self.cell(80, 5)
        self.cell(45, 5, 'Valor')
        self.cell(56, 5, str(rescon[10]), align='R', ln=1)

    #Draw Body dmsRpt_SMS
    def drawBodydms(self,group, month):
        df = self.ae.dmsFMS(group, month)
        self.header_2()
        self.set_left_margin(10)
        self.set_right_margin(10)
        self.set_fill_color(206, 107, 1)
        self.set_text_color(255, 255, 255)
        self.set_font_size(9.5)
        self.set_draw_color(0, 0, 0)
        self.cell(0, 5, 'Serviços NOVA FIBRA detalhado ',align='C', fill=1, ln=1)
        self.ln(4)
        self.cell(15,5, 'Origem' ,align='C', fill=1,border=1)
        self.cell(25,5, 'Tipo', align='C', fill=1,border=1)
        self.cell(30,5, 'Destino', align='C', fill=1,border=1)
        self.cell(40,5, 'Cidade de Destino',align='C', fill=1,border=1)
        self.cell(20,5, 'Data', align='C',fill=1,border=1)
        self.cell(20,5, 'Hora', align='C',fill=1,border=1)
        self.cell(20,5, 'Duração', align='C',fill=1,border=1)
        self.cell(20,5, 'Custo', align='C', fill=1,border=1,ln=1)

        # Accessing the whole dataframe
        for j, k in df[1]:
            # adding the total per group
            k.loc['Total'] = k[['CUSTO']].sum()
            # Accessing each data group to print in single page by from
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
                self.cell(20, 4, 'R$  ' + str(round(row[7],2)),align='R', border='B', ln=1)  #Custo
            self.add_page()
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


# class export():
#     def __init__(self):
#         self.groups = {'PMPG': ['PMPG', 'SME_ESCOLA', 'SME_CMEI']
#             , 'FMS': ['SMS_AIH', 'SMS_PAB']}
#         self.ae = ae()
#         self.month = '20206'

#     def summarizedReport(self):
#         self.pdf = exportPDF()
#         self.pdf.alias_nb_pages()
#         self.pdf.add_page()
#         self.pdf.headerGroup()
#         # Fill data
#         for index in self.groups:
#             for value in tqdm(self.groups[index]):
#                 self.pdf.cell(1, ln=2)
#                 self.pdf.drawBodyNFe(value, self.month)

#         self.pdf.output("E:/DSA/Workspace/Faturamento/Backup/Fechamento/NFe.pdf")

#     def dmsRpt(self):
#         for index in self.groups:
#             for value in tqdm(self.groups[index]):
#                 pdf = exportPDF()
#                 pdf.alias_nb_pages()
#                 pdf.add_page()
#                 pdf.header_2()
#                 pdf.drawBodyDmt(value, self.month)
#                 pdf.add_page()
#                 pdf.drawBodydms(value, self.month)
#                 pdf.output("E:/DSA/Workspace/Faturamento/Backup/Fechamento/Demonstrativo_"+ value +".pdf")


# run = export()
# run.summarizedReport()
# run.dmsRpt()