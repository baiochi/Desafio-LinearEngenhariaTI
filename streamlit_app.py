##################################
#			IMPORTS
##################################

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

if   app_mode == dashboard_page:
	show_dashboard_page()
elif app_mode == description_page:
	show_description_page()