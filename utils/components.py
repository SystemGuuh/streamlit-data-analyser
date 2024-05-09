import streamlit as st
import datetime
from utils.dbconnect import GET_PROPOSTAS_BY_ID

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

def filterProposalComponent(id):
    df = GET_PROPOSTAS_BY_ID(id)
    option = st.multiselect("Proposta da semana recorrente:",['Aceita','Buraco','Checkin Realizado','Chekout Relaziado', 'Pedente'], ['Aceita'])
    return option