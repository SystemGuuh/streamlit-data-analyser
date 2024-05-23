import streamlit as st
from utils.components import *
from utils.dbconnect import GET_WEEKLY_FINANCES
from decimal import Decimal

# Dash Geral
def buildGeneralDash(df):
    container = st.container(border=True)
    with container:
        # Values
        row1 = st.columns(6)

        showNumbers = df.shape[0]
        trasactionValue = round(df['VALOR_BRUTO'].sum(), 2)
        countEstablishments = df['ESTABLECIMENTO'].nunique()
        averageTicket = round(df['VALOR_BRUTO'].mean(), 2)

        if showNumbers > 0: meanShowsByHouse = round((showNumbers / countEstablishments), 2)
        else: meanShowsByHouse=0
        
        distinctArtists = df['ARTISTA'].nunique()
        
        # Page
        tile = row1[0].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Número de Shows</br>{showNumbers}</h6>", unsafe_allow_html=True)

        tile = row1[1].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Valor Transacionado</br>R$ {trasactionValue}</h6>", unsafe_allow_html=True)

        tile = row1[2].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Estabelecimentos</br>{countEstablishments}</h6>", unsafe_allow_html=True)

        tile = row1[3].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Ticket Médio</br>R$ {averageTicket}</h6>", unsafe_allow_html=True)

        tile = row1[4].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Média de Shows por Casa</br>{meanShowsByHouse}</h6>", unsafe_allow_html=True)

        tile = row1[5].container(border=True)
        tile.markdown(f"<h6 style='text-align: center;'>Artistas Distintos</br>{distinctArtists}</h6>", unsafe_allow_html=True)

        # Body
        plotDataframe(df, "Dash Geral")

# GMV total
# Lista de shows
# Shows por artista
# Investimento por dia da semana
# Ticket médio por artista
# Compativo por casa
# Comparativo Mensal
def buildComparativeDash(df):
    st.header("DASH ANALÍTICO COMPARATIVO MENSAL")

    tab1, tab2, tab3 = st.tabs(["CORPORATIVO MENSAL 1", "CORPORATIVO MENSAL 2", "CORPORATIVO MENSAL 3"])
    with tab1:
        container = st.container(border=True)
        with container:
            st.write('building...')
    with tab2:
        container = st.container(border=True)
        with container:
            st.write('building...')
    with tab3:
        container = st.container(border=True)
        with container:
            st.write('building...')

# Avaliação
def buildReview(artistRanking, reviewArtirtsByHouse, averageReviewArtistByHouse,reviewHouseByArtirst, averageReviewHouseByArtist):
    #formating tables
    artistRanking['MEDIA_NOTAS'] = '⭐' + artistRanking['MEDIA_NOTAS'].astype(str)
    artistRanking = artistRanking.rename(columns={'NUM_SHOWS_ARTISTA': 'NÚMERO DE SHOWS', 'MEDIA_NOTAS': 'NOTAS', 'QUANTIDADE_AVALIACOES': 'AVALIAÇÕES'})
    artistRanking = artistRanking.drop(columns=['ID'])


    tab1, tab2= st.tabs(["Ranking", "Avaliações de casas e artistas"])
    with tab1:
        container = st.container(border=True)
        with container:
            center = st.columns([2,2])
            with center[0]: 
                plotDataframe(artistRanking[['ARTISTA', 'NOTAS', 'AVALIAÇÕES', 'NÚMERO DE SHOWS']], "Ranking")
            with center[1]:
                with st.expander("🏆 1º Artista mais bem avaliado"):
                    col1, col2 = st.columns(2)
                    col1.write(f"Nome: {artistRanking['ARTISTA'].iloc[0]}")
                    col1.write(f"Estilo Principal: {artistRanking['ESTILO_PRINCIPAL'].iloc[0]}")
                    col2.write(f"E-mail: {artistRanking['EMAIL'].iloc[0]}")
                    col2.write(f"Celular: {artistRanking['CELULAR'].iloc[0]}")

                with st.expander("🏆 2º Artista mais bem avaliado"):
                    col1, col2 = st.columns(2)
                    col1.write(f"Nome: {artistRanking['ARTISTA'].iloc[1]}")
                    col1.write(f"Estilo Principal: {artistRanking['ESTILO_PRINCIPAL'].iloc[1]}")
                    col2.write(f"E-mail: {artistRanking['EMAIL'].iloc[1]}")
                    col2.write(f"Celular: {artistRanking['CELULAR'].iloc[1]}")

                with st.expander("🏆 3º Artista mais bem avaliado"):
                    col1, col2 = st.columns(2)
                    col1.write(f"Nome: {artistRanking['ARTISTA'].iloc[2]}")
                    col1.write(f"Estilo Principal: {artistRanking['ESTILO_PRINCIPAL'].iloc[2]}")
                    col2.write(f"E-mail: {artistRanking['EMAIL'].iloc[2]}")
                    col2.write(f"Celular: {artistRanking['CELULAR'].iloc[2]}")


    with tab2:
        container = st.container(border=True)
        with container:
            with st.expander("Avaliações sobre artistas", expanded=True):
                row1 = st.columns([3,2])
                with row1[0]:
                    plotDataframe(reviewArtirtsByHouse, "Avaliações das Casas Sobre os Artistas")
                with row1[1]:
                    plotDataframe(averageReviewArtistByHouse, "Médias de Avaliações das Casas Sobre os Artistas")
            
            with st.expander("Avaliações sobre casas"):
                row2 = st.columns([3,2])
                with row2[0]:
                    plotDataframe(reviewHouseByArtirst, "Avaliações dos Artistas Sobre as Casas")
                with row2[1]:
                    plotDataframe(averageReviewHouseByArtist, "Médias de Avaliações dos Artistas Sobre as Casas")

# Desempenho Operacional
def buildOperationalPerformace(operationalPerformace, pizzaChart, allOperationalPerformaceByOccurrenceAndDate, artistCheckinCheckout):    
    tab1, tab2, tab3, tab4= st.tabs(["Ranking de artistas com mais ocorrências", "Ranking por tipo de ocorrência", "Histórico de ocorrências por semana", "Quantiade de checkin e chekout por artista"])
    with tab1:
        plotPizzaChart(pizzaChart['TIPO'], pizzaChart['QUANTIDADE'], "Quantidade de ocorrêcias por tipo")
        plotDataframe(operationalPerformace, "Ranking de artistas com ocorrências")
    with tab2:
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(pizzaChart)
        container = st.container(border=True)
        with container:
            if type is not None:
                plotDataframe(pizzaChart[pizzaChart['TIPO']==type], "Relatório de ocorrências com artistas")
            else:
                plotDataframe(pizzaChart, "Relatório de ocorrências com artistas")
    with tab3:
        plotDataframe(allOperationalPerformaceByOccurrenceAndDate, "Todos relatórios de ocorrências com artistas por data")
    with tab4:
        artistCheckinCheckout = artistCheckinCheckout.rename(columns={'QUANTIDADE_CHECKIN': 'QUANTIDADE DE CHECKING', 'QUANTIDADE_CHECKOUT': 'QUANTIDADE DE CHECKOUT',
                      'TOTAL_CHECKIN_CHECKOUT': 'TOTAL'})

        plotDataframe(artistCheckinCheckout, "Quantidade de checkin e checkout por artista")

# Financeiro        
def buildFinances(df, id):
    row1 = st.columns([2,1,1,1,1,1])
    with row1[0]:
        proposal = filterProposalComponent()
    with row1[1]:
        status = filterFinanceStatus(df)
    with row1[2]:
        year = filterYearChartFinances()
    with row1[5]:
        st.write("")
        with st.popover("Consultar semana"):
            weeklyeDaysNumber(id, year)
    
    st.header("DASH FINANCEIRO")
    container = st.container(border=True)
    with container:
        if status is not None:
            df = df[df['STATUS_FINANCEIRO'] == status]
        if proposal is not None:
            df = df[df['STATUS_PROPOSTA'].str.contains('|'.join(proposal))]

        printFinanceData(df)
        tab1, tab2 = st.tabs(["SEMANAL", "MENSAL"])
        with tab1:
            plotFinanceWeeklyChart(id, year)
        with tab2:
            plotFinanceMonthlyChart(id, year)

        df = formatFinancesDataframe(df)
        plotDataframe(df, "Dados Financeiros Semanais")

# Extrato de show
def buildShowStatement(df):
    # getting values
    total = df.shape[0]
    # hours = round((df['DURACAO'].sum().total_seconds() / 3600),2)
    hours = 0
    ticket = format_brazilian((sum(df['VALOR_BRUTO']) / total).quantize(Decimal('0.00')))
    value = format_brazilian(sum(df['VALOR_BRUTO']).quantize(Decimal('0.00')))

    # formating
    df['VALOR_BRUTO'] = 'R$ ' + df['VALOR_BRUTO'].apply(format_brazilian).astype(str)
    df = df.drop(columns=['ID_PROPOSTA'])
    df_renamed = df
    df_renamed = df_renamed.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA INÍCIO', 'DATA_FIM': 'DATA FIM','DIA_DA_SEMANA': 'DIA DA SEMANA',
                      'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})

    row1 = st.columns(4)

    tile = row1[0].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Total de Shows:</br>{total}</h6>", unsafe_allow_html=True)

    tile = row1[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Total de horas em shows:</br>{hours} Horas</h6>", unsafe_allow_html=True)

    tile = row1[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Transacionado:</br>R$ {value}</h6>", unsafe_allow_html=True)

    tile = row1[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Ticket Médio:</br>R$ {ticket}</h6>", unsafe_allow_html=True)
    
    buttonDowloadDash(df, "Extrato-de-Shows")

    container = st.container(border=True)
    with container:
        plotDataframe(df_renamed, "Extrato de propostas e shows")
             