import streamlit as st
from utils.components import *
from utils.functions import *
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
        countEstablishments = df['ESTABELECIMENTO'].nunique()
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

# Financeiro        
def buildFinances(financeDash,id):
    year = 2024

    # Compenentes de filtragem
    row1 = st.columns([2,1,1,1,1,1])
    with row1[0]:
        proposal = filterProposalComponent()
    with row1[1]:
        status = filterFinanceStatus(financeDash)
    with row1[2]:
        year = filterYearChartFinances()
    with row1[5]:
        st.write("")
    
    st.header("DASH FINANCEIRO")
    container = st.container(border=True)

    # Plotagem dos gráficos
    with container:
        if status is not None:
            financeDash = financeDash[financeDash['STATUS_FINANCEIRO'] == status]
        if proposal is not None:
            financeDash = financeDash[financeDash['STATUS_PROPOSTA'].str.contains('|'.join(proposal))]

        printFinanceData(financeDash)

        tab1, tab2 = st.tabs(["Por período", "Por artistas"])
        weeklyFinances = GET_WEEKLY_FINANCES(id, year)
        with tab1:
            plotFinanceWeeklyChart(weeklyFinances, financeDash) # Resolver questão das ordens dos dias e meses
        with tab2:
            plotFinanceArtist(financeDash) # Adicionar coluna pra quantidade de shows
        st.divider()
        plotDataframe(format_finances_dash(financeDash.copy()), 'Lista de shows')


# Avaliação
def buildReview(artistRanking, reviewArtirtsByHouse, averageReviewArtistByHouse,reviewHouseByArtirst, averageReviewHouseByArtist):
    #formating tables
    artistRanking['MEDIA_NOTAS'] = '⭐' + artistRanking['MEDIA_NOTAS'].astype(str)
    artistRanking = artistRanking.rename(columns={'NUM_SHOWS_ARTISTA': 'NÚMERO DE SHOWS', 'MEDIA_NOTAS': 'NOTAS', 'QUANTIDADE_AVALIACOES': 'AVALIAÇÕES'})
    artistRanking = artistRanking.drop(columns=['ID'])


    tab1, tab2, tab3= st.tabs(["Ranking", "Avaliações de Artista para Estabelecimento", "Avaliações de Estabelecimento para Artista"])
    with tab1:
        container = st.container(border=True)
        with container:
            center = st.columns([2,2])
            with center[0]:
                option = st.selectbox("Buscar artista:", artistRanking['ARTISTA'],
                        index=None, placeholder="Selecione um artista") 
                plotDataframe(artistRanking[['ARTISTA', 'NOTAS', 'AVALIAÇÕES', 'NÚMERO DE SHOWS']], "Ranking")
            with center[1]:
                if option is not None:
                    st.markdown(f"<div style='margin-bottom: 10px;'><h5 padding: 0.1em;'></h5></div>", unsafe_allow_html=True)
                    with st.expander(f"🏆 Dados de artista {option}"):
                        col1, col2 = st.columns(2)
                        col1.write(f"Posição no rank: {(artistRanking[artistRanking['ARTISTA'] == option].index[0]) + 1}º Lugar")
                        col1.write(f"Estilo Principal: {artistRanking['ESTILO_PRINCIPAL'].iloc[0]}")
                        col2.write(f"E-mail: {artistRanking['EMAIL'].iloc[0]}")
                        col2.write(f"Celular: {artistRanking['CELULAR'].iloc[0]}")
                plotSideBarChart(artistRanking, 'ARTISTA', 'NOTAS', 'AVALIAÇÕES', 'Notas e Avaliações por Artista')

    with tab2:
        container = st.container(border=True)
        with container:
            row1 = st.columns([3,2])
            with row1[0]:
                reviewArtirtsByHouse = reviewArtirtsByHouse[['ARTISTA','ESTABELECIMENTO','GRUPO','NOTA', 'AVALIADOR']]
                plotDataframe(reviewArtirtsByHouse, "Avaliações das Casas")
            with row1[1]:
                plotDataframe(averageReviewArtistByHouse, "Médias de Avaliações")
            
    with tab3:
        container = st.container(border=True)
        with container:
            row2 = st.columns([3,2])
            with row2[0]:
                reviewHouseByArtirst = reviewHouseByArtirst[['ESTABELECIMENTO','GRUPO','NOTA']]
                plotDataframe(reviewHouseByArtirst, "Avaliações dos Artistas")
            with row2[1]:
                plotDataframe(averageReviewHouseByArtist, "Médias de Avaliações")

# Desempenho Operacional
def buildOperationalPerformace(operationalPerformace, pizzaChart, ByWeek, artistCheckinCheckout, extract):    
    tab1, tab2= st.tabs(["Resumos", "Extratos"])
    with tab1:
        container1 = st.container(border=True)
        container2 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(pizzaChart['TIPO'], pizzaChart['QUANTIDADE'], "Quantidade de ocorrêcias por tipo")
                plotBarChart(ByWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por semana")
            with row1[1]:
                st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>Ranking de artistas com mais ocorrências</h5>", unsafe_allow_html=True)
                st.dataframe(operationalPerformace[['RANKING','ARTISTA', 'ESTILO','QUANTIDADE']].reset_index(drop=True), hide_index=True,use_container_width=True, height=735)

        with container2:    
            artistCheckinCheckout = artistCheckinCheckout.rename(columns={'QUANTIDADE_CHECKIN': 'QUANTIDADE DE CHECKING', 'QUANTIDADE_CHECKOUT': 'QUANTIDADE DE CHECKOUT',
                                'TOTAL_CHECKIN_CHECKOUT': 'TOTAL'})
            
            artistCheckinCheckout['PORCENTAGEM DE CHECKING(%)'] = ((artistCheckinCheckout['QUANTIDADE DE CHECKING'] * 100) / artistCheckinCheckout['TOTAL']).map("{:.2f}%".format)
            artistCheckinCheckout['PORCENTAGEM DE CHECKOUT(%)'] = ((artistCheckinCheckout['QUANTIDADE DE CHECKOUT'] * 100) / artistCheckinCheckout['TOTAL']).map("{:.2f}%".format)
            
            plotDataframe(artistCheckinCheckout[['ARTISTA', 'TOTAL', 'PORCENTAGEM DE CHECKING(%)', 'PORCENTAGEM DE CHECKOUT(%)']], "Quantidade de checkin e checkout por artista")
    
    with tab2:
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(extract)
        with row1[5]:
            st.write('') # alinhar botão
            st.write('') # alinhar botão
            buttonDowloadDash(extract, "Extrato-de-Ocorrencias")
        container = st.container(border=True)
        with container:
            if type is not None:
                plotDataframe(extract[extract['TIPO']==type], "Relatório completo de ocorrências")
            else:
                plotDataframe(extract, "Relatório completo de ocorrências")

# Extrato de show
def buildShowStatement(df):
    # pegando valores
    total = df.shape[0]
    total_hours, total_minutes, total_seconds = sum_duration_from_dataframe(df)
    ticket = format_brazilian((sum(df['VALOR_BRUTO']) / total).quantize(Decimal('0.00')))
    value = format_brazilian(sum(df['VALOR_BRUTO']).quantize(Decimal('0.00')))

    # formatando df
    df_renamed = format_finances_dash(df)
    
    buttonDowloadDash(df, "Extrato-de-Shows")
    row1 = st.columns(4)

    tile = row1[0].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Total de Shows:</br>{total}</h6>", unsafe_allow_html=True)

    tile = row1[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Total de horas em shows:</br>{total_hours}h {total_minutes}m {total_seconds}s</h6>", unsafe_allow_html=True)

    tile = row1[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Transacionado:</br>R$ {value}</h6>", unsafe_allow_html=True)

    tile = row1[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Ticket Médio:</br>R$ {ticket}</h6>", unsafe_allow_html=True)
    
    

    container = st.container(border=True)
    with container:
        plotDataframe(df_renamed, "Extrato de propostas e shows")
             