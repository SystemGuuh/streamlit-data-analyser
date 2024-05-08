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
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)

    d = st.date_input("Filtro de data:", (thirty_days_ago, today),
                      format="DD.MM.YYYY")
    return d


def filterEstablishmentComponent():
    option = st.selectbox("Filtro de estabelecimentos:",("Email", "Home phone", "Mobile phone"),
            index=None, placeholder="Escolha um")
    return option