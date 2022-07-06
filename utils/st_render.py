

import streamlit as st
from utils.css_style import h1_style, h2_style, hr_style, link_style

import plotly.express as px



def show_dashboard_page():
	pass

def show_description_page():

	st.markdown(h1_style('Descrição do Desafio'), unsafe_allow_html=True)

	st.markdown(f'''
.  
	''', unsafe_allow_html=True)

	st.markdown(h1_style('Contextualização dos Dados'), unsafe_allow_html=True)

	st.markdown(f'''
As informacões a seguir foram retiradas através de consultas no site da 
{link_style("Energisa", "https://www.energisa.com.br/")} e da 
{link_style("Agência Nacional de Energia Elétrica (ANEEL)", 
"https://www.gov.br/aneel/pt-br/centrais-de-conteudos/glossario")}.  
	''', unsafe_allow_html=True)

	st.markdown('''
### Termos gerais

**Consumo**: Quantidade de energia consumida em um mês, em KWH.  
**Demanda**: Potência ativa a ser obrigatória e continuamente 
disponibilizada pela distribuidora, em KW.  

**Postos tarifários**  
Períodos de tempo do dia definidos pela distribuidora.  
- Ponta: 3 horas consecutivas, onde o consumo de energia pela rede é maior.
A tarifa nesse período é mais cara.
- Fora de Ponta: demais horas do dia, a tarifa é mais barata.  

**TE**: Tarifa de Energia (KWh)  
**TUSD**: Tarifa de Uso do Sistema de Distribuição  

**Energia consumida**: parcelas $TE$ e $TUSD_{energia}$ em $R$/KWh$  
**Demanda contratada**: apenas a parcela $TUSD_{demanda}$ em $R$/KW$  
  
<font color='#1696D2'>*Tarifa Azul*
- $TUSD_{energia}$ única
- $TUSD_{demanda}$ Ponta/FPonta
- $TE$ Ponta/FPonta</font>  

<font color='#55B748'>*Tarifa Verde*
- $TUSD_{energia}$ Ponta/FPonta
- $TUSD_{demanda}$ única
- $TE$ Ponta/FPonta</font>  

Em resumo, a tarifa azul é mais atraente para locais que tem a necessidade de consumir mais energia
no período de Ponta, pois dependendo da consecionária, a tarifa $TUSD_{energia}$ 
única costuma ser igual a $TUSD_{energia}$ FPonta. Por outro lado, a tarifa verde é 
interessante para locais que conseguem economizar energia no período de Ponta ou que necessitem 
de uma demanda maior..  
	''', unsafe_allow_html=True)

	st.markdown('''
  ### Signifcado das labels do campo *leituras*:  

- KWH: Consumo, $TUSD_{energia}$
- KW: Demanda de potência medida, $TUSD_{demanda}$
- KVA: Energia reativa, [cobrada caso fator de potência < 0.92](http://www2.aneel.gov.br/aplicacoes/audiencia/arquivo/2012/065/resultado/ren2013569.pdf)  
- ERE: Energia reativa excedente  
- DRE: Demanda reativa excedente  
- INJ: Quantidade de energia elétrica injetada nas redes do sistema  
- ULTP: Ultrapasagem da demanda contratada
	''', unsafe_allow_html=True)

	st.markdown('''
### Visualizando as labels mais comuns da coluna *descricao* em *tarifas*  
Algumas descrições pertencem à categoria do posto **Ponta/FPonta**:  
- Consumo;  
- Demanda medida;
- Demanda não consumida; 
- Demanda ultrapassada;
- Demanda reativa excedente. 

Outras são inependentes dessa classificação:
- Energia ativa injetada;
- Energia reativa excedente.
	''', unsafe_allow_html=True)

	st.markdown('''
### Questões a serem analisadas:
- Consumo (KWh) é maior na PONTA ou FPONTA?  
- Demanda contratada (KW) está sendo utilizada acima ou abaixo?  
- Relação entre a diferença do valor faturado e o valor medido. Se o valor medido for maior, 
qual o motivo do faturado ser menor? E no caso contrário? Existe algum comportamento comum para cada caso?
- Como se comporta a fatura onde há alto valor medido de energia injetada(INJ)? 
Essa energia é proveniente de geração própria?  
	''', unsafe_allow_html=True)




