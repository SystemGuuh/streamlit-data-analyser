import streamlit as st
import datetime
from utils.dbconnect import GET_PROPOSTAS_BY_ID, GET_WEEKLY_FINANCES
import pandas as pd
import numpy as np
from datetime import date
import altair as alt


def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def filterCalendarComponent():
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=90)

    d = st.date_input("Filtro de data:", (thirty_days_ago, today),
                      format="DD/MM/YYYY")
    return d

def filterEstablishmentComponent(id):
    df = GET_PROPOSTAS_BY_ID(id)
    option = st.selectbox("Estabelecimentos:",(df['CASA'].unique()),
            index=None, placeholder="Escolha um")
    return option

def filterProposalComponent():
    option = st.multiselect("Proposta da semana recorrente:",['Aceita','Cancelada','Recusada','Pendente','Checkin Realizado','Checkout Realizado'], ['Aceita', 'Cancelada'])
    return option

def filterYearChartFinances():
    current_year = date.today().year
    years = list(range(2015, current_year + 1))
    years.insert(0, "Escolha um ano:")
    option = st.selectbox("Escolha um ano:", years, index=years.index(2024))
    return option

def plotDataframe(df, name):
    st.markdown(f"<h4 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h4>", unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)

def plotLineChart(df, xValue, yValue,name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)

    st.line_chart(df, x=xValue, y=yValue)

def plotBarChart(name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({"col1": list(range(20)), "col2": np.random.randn(20), "col3": np.random.randn(20)})
    st.bar_chart(chart_data, x="col1", y=["col2", "col3"], color=["#FFB131", "#FF6600"])

def plotMapChart(df):
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    st.map(df)
    
def printFinanceData(df):
    row2 = st.columns(4)
    tile = row2[0].container(border=True)
    

    tile.markdown(f"<h6 style='text-align: center;'>Shows Aceitos</br>{(df['STATUS_PROPOSTA'] == 'Aceita').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Shows Cancelados</br>{(df['STATUS_PROPOSTA'] == 'Cancelada').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Bruto Total</br>R$ {'{:.2f}'.format(df['VALOR_BRUTO'].sum())}</h6>", unsafe_allow_html=True)

    tile = row2[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Líquido Total</br>R$ {'{:.2f}'.format(df['VALOR_LIQUIDO'].sum())}</h6>", unsafe_allow_html=True)

def filterFinanceStatus(df):
    option = st.selectbox("Status Financeiro:",(df['STATUS_FINANCEIRO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def tranlate_day(dia):
    dias_da_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
    }

    return dias_da_semana[dia]

def formatFinancesDataframe(df):
    df['DIA_DA_SEMANA'] = df['DIA_DA_SEMANA'].apply(tranlate_day)
    df['VALOR_BRUTO'] = 'R$ ' + df['VALOR_BRUTO'].astype(str)
    df['VALOR_LIQUIDO'] = 'R$ ' + df['VALOR_LIQUIDO'].astype(str)
    
    df = df.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA', 'HORARIO_INICIO': 'HORÁRIO', 'DIA_DA_SEMANA': 'DIA DA SEMANA',
                     'VALOR_LIQUIDO': 'VALOR LÍQUIDO', 'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})

    return df

def plotFinanceWeeklyChart(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    df['VALOR_GANHO_BRUTO'] = df['VALOR_GANHO_BRUTO'].astype(int)

    with st.expander("Gráfico de barras", expanded=True):
        st.bar_chart(df[['NUMERO_SEMANA','VALOR_GANHO_BRUTO']], x='NUMERO_SEMANA', y='VALOR_GANHO_BRUTO', color=["#ff6600"])
    with st.expander("Gráfico de linhas"):
        st.line_chart(df[['NUMERO_SEMANA','VALOR_GANHO_BRUTO']], x='NUMERO_SEMANA', y='VALOR_GANHO_BRUTO', color=["#ff6600"])
    
def plotFinanceMonthlyChart(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    df['VALOR_GANHO_BRUTO'] = df['VALOR_GANHO_BRUTO'].astype(int)
    df = df.groupby('NUMERO_MES').sum().reset_index()
    with st.expander("Gráfico de barras", expanded=True):
        st.bar_chart(df[['NUMERO_MES','VALOR_GANHO_BRUTO']], x='NUMERO_MES', y='VALOR_GANHO_BRUTO', color=["#ffcc00"])
    with st.expander("Gráfico de linhas"):
        st.line_chart(df[['NUMERO_MES','VALOR_GANHO_BRUTO']], x='NUMERO_MES', y='VALOR_GANHO_BRUTO', color=["#ffcc00"])

def weeklyeDaysNumber(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    st.dataframe(df[['NUMERO_SEMANA', 'DIA']], hide_index=True, use_container_width=True)
