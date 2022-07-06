# Read json data
import json
# Math operations
import numpy as np
# Regex operations
import re
# Reading and process data
import pandas as pd

def clean_data(df, json_data):

	# Flat rows
	df['_id'] = pd.json_normalize(df['_id'])
	df['createdAt'] = pd.json_normalize(df['createdAt'])
	df['updatedAt'] = pd.json_normalize(df['updatedAt'])
	# Rename duplicated value
	df['cliente'] = df['cliente'].replace({'TELEFONICA BRASIL S A': 'TELEFONICA BRASIL SA'})
	# Drop unwanted column
	df.drop(columns='__v', inplace=True)
	# Cast to datetime
	for column in [
		'referencia', 'data_vencimento', 'data_emissao', 
		'data_apresentacao', 'data_proxima_leitura',
		'createdAt', 'updatedAt',
		]: df[column] =  pd.to_datetime(df[column])

	# # Add unique key to estruturaConsumo
	# for index, id_value in enumerate(df['unique']):
	# 	df['estruturaConsumo'].iloc[index]['unique'] = id_value
	#Select metadata
	meta_columns = list(pd.json_normalize(df['estruturaConsumo']).drop(columns='leituras'))
	# Normalize values
	consumo_df = pd.json_normalize(
		df['estruturaConsumo'], 
		record_path=['leituras'],
		meta = meta_columns
	)
	# Fill empty strings with NAN
	consumo_df = consumo_df.replace(r'^\s*$', np.nan, regex=True)
	# Select columns of interest
	int_columns = [
		'saldoPonta', 'saldoForaPonta', 
		'expiraForaPonta', 'expiraPonta', 'saldoAcumulado', 
		'expiraAcumulado']
	float_columns = ['medido', 'faturado']
	date_columns = ['leituraAnterior', 'leituraAtual']
	# Apply cast
	consumo_df[int_columns]       = consumo_df[int_columns].astype('Int64')
	consumo_df[float_columns]     = consumo_df[float_columns].astype('float64')
	consumo_df['leituraAnterior'] = pd.to_datetime(consumo_df['leituraAnterior'])
	consumo_df['leituraAtual']    = pd.to_datetime(consumo_df['leituraAtual'])
	consumo_df.rename(columns={'_id.$oid':'_id.estruturaConsumo'}, inplace=True)
	# Convert data back to original format
	df['estruturaConsumo'] = consumo_df.apply(lambda x : x.to_dict(), axis=1)

	# Normalize lists with dicts
	tarifas_df = pd.json_normalize(
		json_data,					# Dado carregado com json
		record_path=['tarifas'],	# Caminho para achatar
		meta=['unique']				# Coluna de metadado
	)
	# Add new feature to classify the type of description
	tarifas_df['class_desc'] = tarifas_df['descricao'].apply(lambda x: x.split()[0])
	# Filtering description with regex
	tarifas_df['tarifa_posto'] = tarifas_df['descricao'].apply(
		lambda x: re.findall('PONTA|FORA PONTA|F PONTA|FPONTA', x))
	# Extracting values from the list
	tarifas_df['tarifa_posto'] = tarifas_df['tarifa_posto'].apply(lambda x : x[0] if len(x)>0 else 'NA')
	# Normalizing labels
	tarifas_df['tarifa_posto'] = tarifas_df['tarifa_posto'].replace({
		'F PONTA' : 'FPONTA',
		'FORA PONTA' : 'FPONTA',
	})
	tarifas_df.rename(columns={'_id.$oid':'_id.tarifa'}, inplace=True)
	# Convert data back to original format
	tarifas_list = (
		tarifas_df
		.groupby('unique')
		.apply(lambda x : x[tarifas_df.drop(columns='unique').columns].to_dict('records'))
		.reset_index()
		.rename(columns={0:'tarifas'})
	)
	# Merge dataframe
	# Dataframe with all normalized data
	return pd.merge(
		left=df.drop(columns='tarifas'),
		right=tarifas_list,
		on='unique'
	)