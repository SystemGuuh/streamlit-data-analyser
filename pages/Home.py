import streamlit as st
from utils.components import *
from utils.dashes import *
from utils.dbconnect import getDataframeDashGeral
from utils.user import logout

st.set_page_config(
            page_title="Eshows-Data Analytics",
            page_icon="🎤",
            layout="wide",
        )

hide_sidebar()

if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

try:
    if st.session_state['loggedIn']:
    
        # Define ID
        id = 31582

        # Header
        col1, col2 = st.columns([4,1])
        # colocar nome da empresa
        col1.write("# <Nome empresa>")
        col2.image("./assets/imgs/eshows-logo.png", width=100)
        col2.button('Logout', key='Logout', on_click=logout())
        

        # Nav
        st.divider()
        col4, col5, col6 = st.columns([1, 3, 1])
        with col4:
            inputDate = filterCalendarComponent()
        # colocar nome da empresa
        col5.markdown("<h3 style='text-align: center;'>Dash Empresa - Resumo</h3>", unsafe_allow_html=True)
        with col6:
            inputEstablishment = filterEstablishmentComponent(id)
        df = getDataframeDashGeral(id, inputDate, inputEstablishment) 
        #Body
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["DASH GERAL", "DASH ANALÍTICO CORPORATIVO MENSAL", "DASH TEMPORAL", "DASH ANALÍTICO", "DASH POR CASA", "CONTROLE DE LANÇAMENTOS"])
        with tab1:
            buildGeneralDash(df)
        with tab2:
            buildCorporativeDash(df)
        with tab3:
            buildTemporalDash(df)
        with tab4:
            buildAnaliticsDash(df)
        with tab5:
            buildByHouseDash(df)
        with tab6:
            buildReleaseControl(df)
    else:
        st.switch_page("main.py")

except KeyError:
    st.switch_page("main.py")