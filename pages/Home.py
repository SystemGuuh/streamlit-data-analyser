import streamlit as st
from utils.components import *
from utils.functions import *
from data.get_data import get_dashbords_data
from utils.user import logout

# resolver modularização
from menu.general_dash import GeneralDashPage
from menu.finances import FinancesPage
from menu.reviews import ReviewPage
from menu.operational_performance import OperationalPerformacePage
from menu.show_statement import ShowStatementPage

st.set_page_config(
            page_title="Relatórios Eshows",
            page_icon="./assets/imgs/eshows-logo100x100.png",
            layout="wide",
        )


fix_tab_echarts()


if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

if st.session_state['loggedIn']:
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']
    user_id = 25666

    # Header
    col1, col2, col3 = st.columns([9,0.7,1])

    # Caso não ache o ID de usuário
    if user_name is None:
        col1.error('ID de usuário não encontrado')
    else:
        col1.write(f"## Olá, {user_name}")
    col2.image("./assets/imgs/eshows100x100.png")
    
    col3.write('') # serve pra alinhar o botão
    if col3.button("Logout"):
        logout()
        st.switch_page("main.py")
    
    # Nav
    st.divider()
    col4, empty, col5, col6 = st.columns([1, 1, 3, 2])
    with col4:
        inputDate = filterCalendarComponent()
    col5.markdown("<h3 style='text-align: center;'>Relatórios do Estabelecimento</h3>", unsafe_allow_html=True)
    with col6:
        inputEstablishment = filterEstablishmentComponent(user_id)
    
    # Pegando dados das querys
    with st.spinner('Carregando dados, por favor aguarde.'):
        try:
            data = get_dashbords_data(user_id, inputDate, inputEstablishment)
        except Exception as e:
            st.error(f'Não foi possível carregar os dados, verifique a conexão. Erro: {e}')
            data = None

    # Body
    tab1, tab2, tab3, tab4, tab5= st.tabs(["DASH GERAL", "FINANCEIRO", "AVALIAÇÕES", "DESEMPENHO OPERACIONAL", "EXTRATO DE SHOWS"])
    with tab1:
        try:
            page = GeneralDashPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab2:
        try:
            page = FinancesPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab3:
        try:
            page = ReviewPage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab4:
        try:
            page = OperationalPerformacePage(data)
            page.render()
        except Exception as e:
            st.error(f'Não foi possível carregar a página. Erro: {e}')
    with tab5:
        #try:
            page = ShowStatementPage(data)
            page.render()
        #except Exception as e:
        #    st.error(f'Não foi possível carregar a página. Erro: {e}')

else:
    st.switch_page("main.py")
