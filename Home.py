import streamlit as st
from utils.components import *
from utils.pages.dashGeral import buildDashGeral
from utils.pages.dashAnaliticoCorporativo1 import buildDashAnaliticoCorporativo1

#colocar para printar o horário e dia da ultima atualização do bd
def run():
    st.set_page_config(
        page_title="Eshows-Data Analytics",
        page_icon="🎤",
        layout="wide"
    )

    hide_sidebar()
    
    # Header
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("# Dash Clientes - <Nome empresa>")

    # Nav
    st.divider()
    col4, col5, col6 = st.columns([1, 3, 1])
    with col4:
        inputDate = filterCalendarComponent()
    col5.markdown("<h3 style='text-align: center;'>Dash Empresa - Resumo</h3>", unsafe_allow_html=True)
    with col6:
        inputEstablishment = filterEstablishmentComponent()

    #Body
    tab1, tab2, tab3, tab4 = st.tabs(["DASH GERAL", "DASH ANALÍTICO CORPORATIVO MENSAL", "DASH ANALÍTICO CORPORATIVO MENSAL", "DASH ANALÍTICO CORPORATIVO MENSAL"])
    with tab1:
        buildDashGeral()
    with tab2:
        buildDashAnaliticoCorporativo1()
    with tab3:
        st.header("DASH ANALÍTICO CORPORATIVO MENSAL")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    with tab4:
        st.header("DASH ANALÍTICO CORPORATIVO MENSAL")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    
    


if __name__ == "__main__":
    run()