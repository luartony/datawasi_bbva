import datetime
import lightgbm as lgb
import pandas as pd
import numpy as np

ruc_cliente = '37374480882'

## RÉPLICAS

se_entrega_credito = 0
monto_credito = 0

## Clientes BBVA

Matriz_datos = pd.read_csv('Matriz_datos',sep='|')
Matriz_CIIU =pd.read_csv('Matriz_CIIU',sep='|')

Matriz_datos = Matriz_datos[Matriz_datos['taxpayer_id']==int(ruc_cliente)].head(1).copy()
Matriz_datos = pd.merge(Matriz_datos, Matriz_CIIU[['company_economic_activity_id','company_target_mean']],how='left',on='company_economic_activity_id')

Matriz_datos.drop('company_economic_activity_id',axis=1,inplace=True)
Matriz_datos.rename(columns={'company_target_mean':'company_economic_activity_id'},inplace=True)

if Matriz_datos['Tiene_target'][0]==1:
  se_entrega_credito = Matriz_datos['Flag_Credito'][0]
  monto_credito = Matriz_datos['balance_amount'][0]
else:

  import lightgbm as lgb
  Variables_clasificacion= ['Dias_Taxpayer','company_economic_activity_id','IMP_IMPOPER_mean_Or','income_monthly_amount','Dias_Admision','IMP_IMPOPER_mean_De','FEC_OPER_nunique_Or','FEC_OPER_nunique_De','Qty_Transacciones_Or','Qty_Transacciones_De','Edad','employees_number','COD_PERSONOR_nunique_De','COD_TRANSAC_nunique_Or','Diferencia_meses_registro_min']
  Variables_regression = ['IMP_IMPOPER_mean_Or', 'employees_number', 'Qty_Transacciones_Or', 'income_monthly_amount', 'Dias_Taxpayer', 'COD_TRANSAC_nunique_Or', 'ranking_2015_number_flag', 'IMP_IMPOPER_mean_De', 'ranking_2017_number_flag', 'company_economic_activity_id', 'Qty_Transacciones_De', 'ranking_2016_number_flag', 'FEC_OPER_nunique_Or', 'transferred_number_max', 'Dias_Admision']

  modelo_entrenado_cliente_cla = lgb.Booster(model_file=path+'Modelo_clientes_clasificacion_v1.model')
  modelo_entrenado_cliente_reg = lgb.Booster(model_file=path+'Modelo_clientes_regression_v1.model')

  prediccion_cliente_cla = modelo_entrenado_cliente_cla.predict(Matriz_datos[Variables_clasificacion], num_iteration=modelo_entrenado_cliente_cla.best_iteration)
  prediccion_cliente_reg = modelo_entrenado_cliente_reg.predict(Matriz_datos[Variables_regression], num_iteration=modelo_entrenado_cliente_reg.best_iteration)

  se_entrega_credito = [1 if x>0.88 else 0 for x in prediccion_cliente_cla][0]
  monto_credito = round(prediccion_cliente_reg[0],0)

print(se_entrega_credito,monto_credito)