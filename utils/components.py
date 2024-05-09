import streamlit as st
import datetime
from utils.dbconnect import GET_PROPOSTAS_BY_ID
import pandas as pd
import numpy as np

# Tira a sidebar
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
    option = st.multiselect("Proposta da semana recorrente:",['Aceita','Recusada','Pendente','Checkin Realizado','Checkout Realizado'], ['Aceita'])
    return option

def plotDataframe(df, name):
    st.markdown(f"<h4 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h4>", unsafe_allow_html=True)
    st.dataframe(df, hide_index=1)

# build after query
def plotLineChart(df, xValue, yValue,name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)

    st.line_chart(df, x=xValue, y=yValue)

# build after query
def plotBarChart(name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({"col1": list(range(20)), "col2": np.random.randn(20), "col3": np.random.randn(20)})
    st.bar_chart(chart_data, x="col1", y=["col2", "col3"], color=["#FFB131", "#FF6600"])

def plotMapChart(df):
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    st.map(df)
    