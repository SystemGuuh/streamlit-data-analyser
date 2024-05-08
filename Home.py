import streamlit as st
from utils.components import *

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

    st.divider()
    col4, col5, col6 = st.columns([1, 3, 1])
    with col4:
        inputDate = filterCalendarComponent()
    col5.markdown("<h3 style='text-align: center;'>Dash Empresa - Resumo</h3>", unsafe_allow_html=True)
    with col6:
        inputEstablishment = filterEstablishmentComponent()


if __name__ == "__main__":
    run()