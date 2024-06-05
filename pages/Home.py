import streamlit as st
from utils.components import *
from utils.menuPages import *
from utils.functions import *
from utils.dbconnect import *
from utils.user import logout
from datetime import datetime

st.set_page_config(
            page_title="Eshows-Data Analytics",
            page_icon="🎤",
            layout="wide",
        )

hide_sidebar()
fix_tab_echarts()


if 'loggedIn' not in st.session_state:
    st.switch_page("main.py")

if st.session_state['loggedIn']:

    # Define ID
    id = 31582

    # Header
    col1, col2, col3 = st.columns([9,0.7,1])

    # Caso não ache o ID de usuário
    username = GET_USER_NAME(id)
    if username.empty:
        col1.error('ID de usuário não encontrado')
    else:
        col1.write(f"## Olá, {username.iloc[0]['FULL_NAME']}")
    col2.image("./assets/imgs/eshows100x100.png")
    
    col3.write('') # serve pra alinhar o botão
    if col3.button("Logout"):
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
    
    # Pegando dados das querys
    with st.spinner('Carregando dados, por favor aguarde.'):
        try:
            generalFinances = GET_WEEKLY_FINANCES(id, datetime.now().year)
            financeDash = GET_GERAL_INFORMATION_AND_FINANCES(id)
            financeDash['DIA_DA_SEMANA'] = financeDash['DIA_DA_SEMANA'].apply(translate_day)
            artistRanking = GET_ARTIST_RANKING(id)
            reviewArtitsByHouse = GET_REVIEW_ARTIST_BY_HOUSE(id)
            averageReviewArtistByHouse = GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id)
            reviewHouseByArtist = GET_REVIEW_HOUSE_BY_ARTIST(id)
            averageReviewHouseByArtist = GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id)
            allOperationalPerformaceByOccurrenceAndDate = GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id)
            allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate
            operationalPerformace = get_report_artist(allOperationalPerformaceByOccurrenceAndDate) # ranking
            ByOccurrence = get_report_by_occurrence(allOperationalPerformaceByOccurrenceAndDate) #gráfico de pizza
            ByWeek = get_report_artist_by_week(allOperationalPerformaceByOccurrenceAndDate) #grafico de barras
            checkinCheckout = GET_ARTIST_CHECKIN_CHECKOUT(id)
            showStatement = GET_PROPOSTAS_BY_ID(id) 
            showStatement['DIA_DA_SEMANA'] = showStatement['DIA_DA_SEMANA'].apply(translate_day)
        except:
            st.error('Não foi possível carregar os dados, verifique a conexão.')

    # Aplicando filtros
    showStatement = apply_filter_in_geral_dataframe(showStatement, inputDate, inputEstablishment)
    reviewArtitsByHouse = apply_filter_in_dataframe(reviewArtitsByHouse, inputDate, inputEstablishment)
    reviewHouseByArtist = apply_filter_establishment_in_dataframe(reviewHouseByArtist, inputEstablishment) 
    averageReviewHouseByArtist = apply_filter_establishment_in_dataframe(averageReviewHouseByArtist, inputEstablishment)
    financeDash = apply_filter_in_finance_dataframe(financeDash, inputDate, inputEstablishment)
    allOperationalPerformaceByOccurrenceAndDate = apply_filter_in_report_dataframe(allOperationalPerformaceByOccurrenceAndDate, inputDate, inputEstablishment)

    # Body
    tab1, tab2, tab3, tab4, tab5= st.tabs(["DASH GERAL", "FINANCEIRO", "AVALIAÇÕES", "DESEMPENHO OPERACIONAL", "EXTRATO DE SHOWS"])
    with tab1:
        buildGeneralDash(generalFinances.copy(), financeDash.copy(), averageReviewHouseByArtist.copy(), ByOccurrence.copy(), showStatement.copy())
    with tab2:
        buildFinances(financeDash.copy(), id)
    with tab3:
        buildReview(artistRanking.copy(), reviewArtitsByHouse.copy(), averageReviewArtistByHouse.copy(), reviewHouseByArtist.copy(), averageReviewHouseByArtist.copy())
    with tab4:
        buildOperationalPerformace(operationalPerformace.copy(), ByOccurrence.copy(), ByWeek.copy(), checkinCheckout.copy(), allOperationalPerformaceByOccurrenceAndDate.copy())   
    with tab5:
        buildShowStatement(showStatement.copy())

else:
    st.switch_page("main.py")
