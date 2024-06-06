import streamlit as st
from utils.components import *
from utils.menuPages import *
from utils.functions import *
from utils.dbconnect import *
from utils.user import logout

st.set_page_config(
            page_title="Relatórios Eshows",
            page_icon="./assets/imgs/eshows-logo100x100.png",
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
    col4, empty, col5, col6 = st.columns([1, 1, 3, 2])
    with col4:
        inputDate = filterCalendarComponent()
    col5.markdown("<h3 style='text-align: center;'>Relatórios do Estabelecimento</h3>", unsafe_allow_html=True)
    with col6:
        inputEstablishment = filterEstablishmentComponent(id)
    
    # Pegando dados das querys
    with st.spinner('Carregando dados, por favor aguarde.'):
        try:
            generalFinances = GET_WEEKLY_FINANCES(id)
            financeDash = GET_GERAL_INFORMATION_AND_FINANCES(id)
            
            artistRanking = apply_filter_in_dataframe( GET_ARTIST_RANKING(id), inputDate, inputEstablishment)
            reviewArtitsByHouse = apply_filter_in_dataframe( GET_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
            averageReviewArtistByHouse = apply_filter_in_dataframe( GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
            reviewHouseByArtist = apply_filter_in_dataframe( GET_REVIEW_HOUSE_BY_ARTIST(id), None, inputEstablishment)
            averageReviewHouseByArtist = apply_filter_in_dataframe( GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id), None, inputEstablishment)
            allOperationalPerformaceByOccurrenceAndDate = apply_filter_in_dataframe( GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id), inputDate, inputEstablishment)
            operationalPerformace = apply_filter_in_dataframe( get_report_artist(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
            ByOccurrence = apply_filter_in_dataframe( get_report_by_occurrence(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
            ByWeek = apply_filter_in_dataframe( get_report_artist_by_week(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
            checkinCheckout = apply_filter_in_dataframe( GET_ARTIST_CHECKIN_CHECKOUT(id), inputDate, inputEstablishment)
            showStatement = apply_filter_in_dataframe( GET_PROPOSTAS_BY_ID(id), inputDate, inputEstablishment) 
            weeklyFinances = apply_filter_in_dataframe( GET_WEEKLY_FINANCES(id), inputDate, inputEstablishment)

            financeDash['DIA_DA_SEMANA'] = financeDash['DIA_DA_SEMANA'].apply(translate_day)
            showStatement['DIA_DA_SEMANA'] = showStatement['DIA_DA_SEMANA'].apply(translate_day)
            
        except:
            st.error('Não foi possível carregar os dados, verifique a conexão.')

    # Body
    tab1, tab2, tab3, tab4, tab5= st.tabs(["DASH GERAL", "FINANCEIRO", "AVALIAÇÕES", "DESEMPENHO OPERACIONAL", "EXTRATO DE SHOWS"])
    with tab1:
        buildGeneralDash(generalFinances.copy(), financeDash.copy(), averageReviewHouseByArtist.copy(), ByOccurrence.copy(), showStatement.copy())
    with tab2:
        buildFinances(financeDash.copy(), weeklyFinances.copy(), id)
    with tab3:
        buildReview(artistRanking.copy(), reviewArtitsByHouse.copy(), averageReviewArtistByHouse.copy(), reviewHouseByArtist.copy(), averageReviewHouseByArtist.copy())
    with tab4:
        buildOperationalPerformace(operationalPerformace.copy(), ByOccurrence.copy(), ByWeek.copy(), checkinCheckout.copy(), allOperationalPerformaceByOccurrenceAndDate.copy())   
    with tab5:
        buildShowStatement(showStatement.copy())

else:
    st.switch_page("main.py")
