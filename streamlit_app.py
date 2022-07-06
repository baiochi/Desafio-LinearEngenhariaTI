##################################
#			IMPORTS
##################################

# Read json data
import json
# Math operations
import numpy as np
# Regex operations
import re
# Reading and process data
import pandas as pd
# Data visualization
import plotly.express as px
# Custom plot configurations
from utils.urban_layout import CATEGORICAL_GROUPS, LAYOUT_SPECS, SHADES
# Web rendering API
import streamlit as st
from utils.css_style import h1_style, h2_style, hr_style, link_style
from utils.st_render import show_dashboard_page, show_description_page

##################################
#		 PAGE CONFIGURATION
##################################

st.set_page_config(
	page_title='Desafio Linear Engenharia TI', 
	#page_icon=open_image('img/favicon.png'), 
	layout='wide')

# if '' not in st.session_state:
#     st.session_state[''] = False
# st.session_state

##################################
#			LOAD DATA
##################################
df = pd.read_json('data/consumo.json')
with open('data/consumo.json', 'r') as file:
	json_data = json.load(file)

##################################
#			DATA CLEANING
##################################
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
# Add unique key to estruturaConsumo
for index, id_value in enumerate(df['unique']):
	df['estruturaConsumo'].iloc[index]['unique'] = id_value
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
# Convert data back to original format
tarifas_list = (
	tarifas_df
	.groupby('unique')
	.apply(lambda x : x[tarifas_df.drop(columns='unique').columns].to_dict('records'))
	.reset_index()
	.rename(columns={0:'tarifas'})
)
# Merge dataframe
# Dataframe com todos dados normalizados
norm_df = pd.merge(
	left=df.drop(columns='tarifas'),
	right=tarifas_list,
	on='unique'
)


##################################
#			SIDE BAR
##################################

dashboard_page	 = 'Dashboard'
description_page = 'Sobre'

app_mode = st.sidebar.selectbox(label='Escolha a página',
	options=[
		dashboard_page,
		description_page,
	])




##################################
#			MAIN PAGE
##################################

# Main title
st.markdown(h1_style('Desafio Linear Engenharia TI') + hr_style(), unsafe_allow_html=True)

# Mode title
st.markdown(h2_style(f'{app_mode}'), unsafe_allow_html=True)

if   app_mode == dashboard_page:
	show_dashboard_page()
elif app_mode == description_page:
	show_description_page()