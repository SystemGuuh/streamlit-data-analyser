import streamlit as st
from utils.components import *
from utils.menuPages import *
from utils.dbconnect import *
from utils.user import logout

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

    df = GET_PROPOSTAS_BY_ID(id, inputDate, inputEstablishment) 
    df['DIA_DA_SEMANA'] = df['DIA_DA_SEMANA'].apply(translate_day)

    # Dataframe vazio
    if df.empty:
        col1.warning('Parace que você não permissão para visualizar dados de casas.')

    #Body
    tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["DASH GERAL", "COMPARATIVO MENSAL", "AVALIAÇÕES", "DESEMPENHO OPERACIONAL", "FINANCEIRO", "EXTRATO DE SHOWS"])
    with tab1:
        # página
        buildGeneralDash(df)
    with tab2:
        # página
        buildComparativeDash(df)
    with tab3:
        # tabelas usadas
        artistRanking = GET_ARTIST_RANKING(id)
        reviewArtitsByHouse = GET_REVIEW_ARTIST_BY_HOUSE(id, inputDate, inputEstablishment)
        averageReviewArtistByHouse = GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id)
        reviewHouseByArtist = GET_REVIEW_HOUSE_BY_ARTIST(id)
        averageReviewHouseByArtist = GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id)

        # página
        buildReview(artistRanking, reviewArtitsByHouse, averageReviewArtistByHouse, reviewHouseByArtist, averageReviewHouseByArtist)
    with tab4:
        # tabelas usadas
        allOperationalPerformaceByOccurrenceAndDate = GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id, inputDate, inputEstablishment)
        operationalPerformace = get_report_artist(allOperationalPerformaceByOccurrenceAndDate) # ranking
        ByOccurrence = get_report_by_occurrence(allOperationalPerformaceByOccurrenceAndDate) #gráfico de pizza
        ByWeek = get_report_artist_by_week(GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id, None, inputEstablishment)) #grafico de barras
        checkinCheckout = GET_ARTIST_CHECKIN_CHECKOUT(id)

        # página
        buildOperationalPerformace(operationalPerformace, ByOccurrence, ByWeek, checkinCheckout, allOperationalPerformaceByOccurrenceAndDate)
    with tab5:
        # tabelas usadas
        financeDash = GET_GERAL_INFORMATION_AND_FINANCES(id, inputDate, inputEstablishment)

        # página
        buildFinances(financeDash, id)
    with tab6:
        # tabelas usadas
        showStatement = GET_PROPOSTAS_BY_ID(id, inputDate, inputEstablishment) 
        showStatement['DIA_DA_SEMANA'] = showStatement['DIA_DA_SEMANA'].apply(translate_day)
        
        # página
        buildShowStatement(showStatement)
else:
    st.switch_page("main.py")
