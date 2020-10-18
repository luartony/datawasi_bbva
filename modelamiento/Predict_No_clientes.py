import datetime
import lightgbm as lgb
import pandas as pd
import numpy as np
## Datos del formulario

ruc = '20538856674'
income_monthly_amount = 5000 # Ingresos mensuales
Fecha_nacimiento = '20/10/1994'
employees_number = 20 # número de empleados

### Data SUNAT

datos_SUNAT = pd.read_csv(path+'sample_data_sunat.csv',sep=',')

def obtener_RUC(x):
  return str(x).strip().split(' ')[0]

def obtener_fecha_inscripcion(x):
  return str(x).strip().split(',')[0]

def obtener_fecha_Inicio_Actividades(x):
  return str(x).strip().split(',')[2]

datos_SUNAT['RUC'] = datos_SUNAT['Número de RUC'].apply(lambda x: obtener_RUC(x))
datos_SUNAT['Fecha_de_Inscripcion'] = datos_SUNAT['Fecha de Inscripción'].apply(lambda x: obtener_fecha_inscripcion(x))
datos_SUNAT['Fecha_de_Inicio_de_Actividades'] = datos_SUNAT['Fecha de Inscripción'].apply(lambda x: obtener_fecha_Inicio_Actividades(x))

datos_SUNAT['Estado del Contribuyente'] = datos_SUNAT['Estado del Contribuyente'].apply(lambda x: x.split(',')[0])
datos_SUNAT['Sistema_Emision_Comprobante'] = datos_SUNAT['Sistema de Emisión de Comprobante'].apply(lambda x: str(x).strip().split(',')[0])
datos_SUNAT['Actividad de Comercio Exterior'] = datos_SUNAT['Sistema de Emisión de Comprobante'].apply(lambda x: str(x).strip().split(',')[2])
datos_SUNAT['Actividad Economica'] = datos_SUNAT['Actividad(es) Económica(s)'].apply(lambda x: str(x).strip().split(' ')[0])

def obtener_departamento(x):
  departamento = str(x).split('-')[0].strip()
  return departamento.split(' ')[-1]

def obtener_provincia(x):
  return str(x).split('-')[1].strip()

def obtener_distrito(x):
  return str(x).split('-')[2].strip()

datos_SUNAT['Departamento'] = datos_SUNAT['Dirección del Domicilio Fiscal'].apply(lambda x: obtener_departamento(x))
datos_SUNAT['Provincia'] = datos_SUNAT['Dirección del Domicilio Fiscal'].apply(lambda x: obtener_provincia(x))
datos_SUNAT['Distrito'] = datos_SUNAT['Dirección del Domicilio Fiscal'].apply(lambda x: obtener_distrito(x))

datos_SUNAT_cliente = datos_SUNAT[datos_SUNAT['RUC']==ruc].head(1).copy()

datos_SUNAT_cliente['birth_date'] = Fecha_nacimiento
datos_SUNAT_cliente['income_monthly_amount'] = income_monthly_amount
datos_SUNAT_cliente['employees_number'] = employees_number

datos_SUNAT_cliente['birth_date'] = pd.to_datetime(datos_SUNAT_cliente.birth_date, format='%d/%m/%Y')
datos_SUNAT_cliente['Fecha_de_Inscripcion'] = pd.to_datetime(datos_SUNAT_cliente.Fecha_de_Inscripcion, format='%d/%m/%Y')
datos_SUNAT_cliente['Fecha_de_Inicio_de_Actividades'] = pd.to_datetime(datos_SUNAT_cliente.Fecha_de_Inicio_de_Actividades, format='%d/%m/%Y')

datos_SUNAT_cliente['Dias_Admision'] = (datetime.datetime.utcnow() -datos_SUNAT_cliente['Fecha_de_Inscripcion']).astype('timedelta64[D]')
datos_SUNAT_cliente['Dias_Taxpayer'] = (datetime.datetime.utcnow() -datos_SUNAT_cliente['Fecha_de_Inicio_de_Actividades']).astype('timedelta64[D]')
datos_SUNAT_cliente['Edad'] = datos_SUNAT_cliente['birth_date'].apply(lambda x: 2020-int(str(x)[0:4]))

datos_SUNAT_cliente['company_economic_activity_id'] = datos_SUNAT_cliente['Actividad Economica']
datos_SUNAT_cliente = pd.merge(datos_SUNAT_cliente, Matriz_CIIU[['company_economic_activity_id','company_target_mean']],how='left',on='company_economic_activity_id')
datos_SUNAT_cliente.drop('company_economic_activity_id',axis=1,inplace=True)
datos_SUNAT_cliente.rename(columns={'company_target_mean':'company_economic_activity_id'},inplace=True)

if datos_SUNAT_cliente['Estado del Contribuyente'][0]=='ACTIVO':
  import lightgbm as lgb

  modelo_entrenado_No_cliente_cla = lgb.Booster(model_file=path+'Modelo_No_clientes_clasificacion_v1.model')
  modelo_entrenado_No_cliente_reg = lgb.Booster(model_file=path+'Modelo_No_clientes_regression_v1.model')

  prediccion_No_cliente_cla = modelo_entrenado_No_cliente_cla.predict(datos_SUNAT_cliente[informacion_no_clientes], num_iteration=modelo_entrenado_No_cliente_cla.best_iteration)
  prediccion_No_cliente_reg = modelo_entrenado_No_cliente_reg.predict(datos_SUNAT_cliente[informacion_no_clientes], num_iteration=modelo_entrenado_No_cliente_reg.best_iteration)

  se_entrega_credito_no_cliente = [1 if x>0.85 else 0 for x in prediccion_No_cliente_cla][0]
  monto_credito_no_cliente = round(prediccion_No_cliente_reg[0],0)
else:
  se_entrega_credito_no_cliente = 0
  monto_credito_no_cliente = 0

print(se_entrega_credito_no_cliente,monto_credito_no_cliente)