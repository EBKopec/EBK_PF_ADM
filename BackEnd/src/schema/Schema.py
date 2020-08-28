from marshmallow import fields, validates, ValidationError
from flask_marshmallow import Marshmallow
from flask import request
ma = Marshmallow()

def configure(app):
    ma.init_app(app)

class controle_agrupamento_bkpSchema(ma.Schema):
    class Meta:
        fields = ('linha', 'user_group_id', 'tipo_linha', 'data_envio_nova', 'data_validacao_cliente', 'data_cancelamento', 'status', 'data_alteracao','Grupo', 'Quantidade', 'PROPORCIONAL','RAMAIS_ATIVOS','ATIVADOS_MES','EM_ATIVACAO','DESCONECTADOS','DATA')

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('USER_ID', 'USER_DESC', 'USER_CODE', 'USER_GROUP_ID', 'ACTIVATION_DATE', 'EXPIRATION_DATE', 'ENABLED_DATE', 'User_Group')

class TarifaSchema(ma.Schema):
    class Meta:
        fields = ('USER_ID', 'TIPO_ID', 'CUSTO', 'DATA_ALTERACAO', 'FRANQUIA_MIN', 'FRANQUIA_VALOR', 'VALOR_RAMAL', 'BATCH_ID')

class TipoSchema(ma.Schema):
    class Meta:
        fields = ('ID', 'TIPO', 'DATA_ALTERACAO','TIPO_DESC')

class FaresSchema(ma.Schema):
    class Meta:
        fields = ('GRUPO','USER_CODE','CALL_TYPE','COST','MIN_TELEPHONE_FRANCHISE','VALUES_TELEPHONE_FRANCHISE','VALUE_EXTENSION','TYPE_CALL_ID')

class BackupsSchema(ma.Schema):
    class Meta:
        fields = ('MES_FATURAMENTO_ID', 'MES_ID', 'FATURAMENTO_ID', 'BATCH_ID', 'TIPO', 'ORIGEM', 'DATA', 'HORA', 'DESTINO', 'CIDADE_DESTINO', 'DURACAO_REAL', 'CUSTO_ORIGINAL', 'CUSTO', 'USER_ID', 'USER_DESC', 'DISTRIBUTOR_ID','QTY','BACKUP')

class ResumeConsumeSchema(ma.Schema):
    class Meta:
        fields = ( 'mes_id', 'group', 'ramal_ativo', 'valor_ramal', 'parcial',\
                    'faturar_ramais', 'franquias', 'excedentes', 'total_faturar', 'ldn_minutes',\
                    'ldn_values', 'local_minutes', 'local_values', 'movel_minutes', 'movel_values', 'ldn_minutes_exc',\
                    'ldn_values_exc', 'local_minutes_exc', 'local_values_exc', 'movel_minutes_exc', 'movel_values_exc', 'ldn_total_m', \
                    'ldn_total_valor', 'local_total_m', 'local_total_valor', 'movel_total_m', \
                    'movel_total_valor', 'total')

class SrcUtilsSchema(ma.Schema):
    class Meta:
        fields = ('type_file', 'src_utils', 'src_utils_desc', 'src_change_date')


class VwsSchema(ma.Schema):
    class Meta:
        fields = ('MES_FATURAMENTO_ID', 'MES_ID', 'ID', 'USER_ID', 'AGRUPAMENTO', 'TIPO', 'ORIGEM', 'DATA', 'HORA', 'DESTINO', 'CIDADE_DESTINO', 'DURACAO_REAL', 'CUSTO', 'VALIDAR_AGRUPAMENTO', 'VALIDAR_HORA')

class backupDoneSchema(ma.Schema):
    class Meta:
        fields = ('table_schema', 'table_name', 'table_rows', 'create_time')

class ApplicationUsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email')

class AnoMesSchema(ma.Schema):
    class Meta:
        fields = ('id_ano', 'id_mes', 'ano', 'mes')


# Init Schema
ext_schema = controle_agrupamento_bkpSchema()
exts_schema = controle_agrupamento_bkpSchema(many = True)
users_schema = UsersSchema(many = True)

tarifa_Schema = TarifaSchema()
tarifas_schema = TarifaSchema(many = True)

type_schema = TipoSchema()
types_schema = TipoSchema(many = True)

fares_schema = FaresSchema(many = True)

backup_Schema = BackupsSchema()
backups_Schema = BackupsSchema(many = True)
backupDone_Schema = backupDoneSchema(many = True)

resume_Schema = ResumeConsumeSchema(many = True)

src_utils_Schema = SrcUtilsSchema()

vws_Schema = VwsSchema(many = True)


app_users_Schema = ApplicationUsersSchema()

anoMes_Schema = AnoMesSchema(many = True)