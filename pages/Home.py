import streamlit as st
from utils.components import *
from utils.dashes import *
from utils.dbconnect import *
from utils.user import logout

st.set_page_config(
            page_title="Eshows-Data Analytics",
            page_icon="🎤",
            layout="wide",
        )

hide_sidebar()

if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

if st.session_state['loggedIn']:

    # Define ID
    id = 31582

    # Header
    col1, col2 = st.columns([4,1])

    # Caso não ache o ID de usuário
    username = GET_USER_NAME(id)
    if username.empty:
        col1.error('ID de usuário não encontrado')
    else:
        col1.write(f"## Olá, {username.iloc[0]['FULL_NAME']}")
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    if col2.button("Logout"):
        logout()
        st.switch_page("main.py")
    
    # Nav
    st.divider()
    col4, col5, col6 = st.columns([1, 3, 1])
    with col4:
        inputDate = filterCalendarComponent()
    col5.markdown("<h3 style='text-align: center;'>Dash Empresa - Resumo</h3>", unsafe_allow_html=True)
    with col6:
        inputEstablishment = filterEstablishmentComponent(id)
    df = getDataframeDashGeral(id, inputDate, inputEstablishment) 

    # Dataframe vazio
    if df.empty:
        col1.warning('Parace que você não permissão para visualizar dados de casas.')

    #Body
    tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["DASH GERAL", "COMPARATIVO MENSAL", "AVALIAÇÕES", "DESEMPENHO OPERACIONAL", "FINANCEIRO", "EXTRATO DE SHOWS"])
    with tab1:
        buildGeneralDash(df)
    with tab2:
        buildComparativeDash(df)
    with tab3:
        artistRanking = GET_ARTIST_RANKING(id)
        reviewArtitsByHouse = GET_REVIEW_ARTIST_BY_HOUSE(id, inputDate, inputEstablishment)
        averageReviewArtistByHouse = GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id)
        reviewHouseByArtist = GET_REVIEW_HOUSE_BY_ARTIST(id)
        averageReviewHouseByArtist = GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id)
        buildReview(artistRanking, reviewArtitsByHouse, averageReviewArtistByHouse, reviewHouseByArtist, averageReviewHouseByArtist)
    with tab4:
        operationalPerformace = GET_REPORT_ARTIST(id)
        buildOperationalPerformace(operationalPerformace)
    with tab5:
        financeDash = GET_GERAL_INFORMATION_AND_FINANCES(id, inputDate, inputEstablishment)
        buildFinances(financeDash, id)
    with tab6:
        buildShowStatement(df)
else:
    st.switch_page("main.py")
