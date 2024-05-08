import streamlit as st
import datetime

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
    today = datetime.datetime.now()
    year = today.year
    jan_1 = datetime.date(year, 1, 1)
    dec_31 = datetime.date(year, 12, 31)

    d = st.date_input("Filtro de data:",(jan_1, datetime.date(year, 1, 7)),
        jan_1, dec_31, format="DD.MM.YYYY")
    return d

def filterEstablishmentComponent():
    option = st.selectbox("Filtro de estabelecimentos:",("Email", "Home phone", "Mobile phone"),
            index=None, placeholder="Escolha um")
    return option