import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

#arrumar login

# Dash Geral
def buildGeneralDash(monthlyFinances, financeDash, averageReviewHouseByArtist, pizzaChart, showStatement):
    # pegando valores
    artists = len(pd.unique(showStatement['ARTISTA']))
    stablishment = len(pd.unique(showStatement['ESTABELECIMENTO']))
    total = showStatement.shape[0]
    total_hours, total_minutes, total_seconds = sum_duration_from_dataframe(showStatement)
    ticket = 0 if total == 0 else  format_brazilian((sum(showStatement['VALOR_BRUTO']) / total).quantize(Decimal('0.00')))
    value = format_brazilian(Decimal(sum(showStatement['VALOR_BRUTO'])).quantize(Decimal('0.00')))

    # Printando valores em containers
    row1 = st.columns(6)

    tile = row1[0].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Artistas</br>{artists}</p>", unsafe_allow_html=True)

    tile = row1[1].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Estabelecimentos</br>{stablishment}</p>", unsafe_allow_html=True)

    tile = row1[2].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Total de Shows</br>{total}</p>", unsafe_allow_html=True)

    tile = row1[3].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Horas em Shows</br>{total_hours}h {total_minutes}m {total_seconds}s</p>", unsafe_allow_html=True)

    tile = row1[4].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Valor Transacionado</br>R$ {value}</p>", unsafe_allow_html=True)

    tile = row1[5].container(border=True)
    tile.markdown(f"<p style='text-align: center;'>Ticket Médio</br>R$ {ticket}</p>", unsafe_allow_html=True)
    
    container = st.container(border=True)
    with container:
        row2 = st.columns([3,2])
        with row2[0]:
            plotGeneralFinanceChart(monthlyFinances)
            #plotPizzaChart(pizzaChart['TIPO'], pizzaChart['QUANTIDADE'], "Resumo de ocorrêcias por tipo")
        with row2[1]:
            plotGeneralFinanceArtist(financeDash)
        plotDataframe(averageReviewHouseByArtist, "Satisfação do Estabelecimento")
        
# Financeiro        
def buildFinances(financeDash, weeklyFinances,id):

    # Componentes de filtragem [REMOVIDOS]
    # row1 = st.columns([2,1,1,1,1,1])
    # with row1[0]:
    #    proposal = filterProposalComponent()
    # with row1[1]:
    #    status = filterFinanceStatus(financeDash)
    # with row1[2]:
    #    year = filterYearChartFinances()
    
    # Plotagem dos gráficos
    printFinanceData(financeDash)
    container = st.container(border=True)
    with container:
        tab1, tab2 = st.tabs(["Por período", "Por artistas"])
        with tab1:
            plotFinanceCharts(weeklyFinances, financeDash)
        with tab2:
            plotFinanceArtist(financeDash)
        st.divider()
        plotDataframe(format_finances_dash(financeDash.copy()), 'Lista de shows')

# Avaliação
def buildReview(artistRanking, reviewArtirtsByHouse, averageReviewArtistByHouse,reviewHouseByArtirst, averageReviewHouseByArtist):
    #formatando tabelas
    artistRanking = artistRanking.rename(columns={'NUM_SHOWS_ARTISTA': 'NÚMERO DE SHOWS', 'MEDIA_NOTAS': 'MÉDIA', 'QUANTIDADE_AVALIACOES': 'NÚMERO DE AVALIAÇÕES'})


    tab1, tab2, tab3= st.tabs(["Ranking", "Avaliações de Estabelecimento para Artista", "Avaliações de Artista para Estabelecimento"])
    with tab1:
        container = st.container(border=True)
        with container:
            center = st.columns([2,2])
            with center[0]:
                artistRanking_sorted = artistRanking.sort_values(by='ARTISTA')
                option = st.selectbox("Buscar artista:", artistRanking_sorted['ARTISTA'],
                        index=None, placeholder="Selecione um artista") 
                plotDataframe(artistRanking[['ARTISTA', 'MÉDIA', 'NÚMERO DE AVALIAÇÕES', 'NÚMERO DE SHOWS']], "Ranking")
            with center[1]:
                if option is not None:
                    st.markdown("<p style='padding-top:0.2em'></p>", unsafe_allow_html=True)
                    with st.expander(f"🏆 Dados de artista {option}"):
                        col1, col2 = st.columns(2)
                        col1.write(f"Posição no rank: {(artistRanking[artistRanking['ARTISTA'] == option].index[0]) + 1}º Lugar")
                        col1.write(f"Estilo Principal: {artistRanking['ESTILO_PRINCIPAL'].iloc[0]}")
                        col2.write(f"E-mail: {artistRanking['EMAIL'].iloc[0]}")
                        col2.write(f"Celular: {artistRanking['CELULAR'].iloc[0]}")
                    plotSideBarChart(artistRanking, 'ARTISTA', 'MÉDIA', 'NÚMERO DE AVALIAÇÕES', 'Notas e Avaliações por Artista')
                else:
                    st.markdown("<p style='padding-top:4.3em'></p>", unsafe_allow_html=True)
                    plotSideBarChart(artistRanking, 'ARTISTA', 'MÉDIA', 'NÚMERO DE AVALIAÇÕES', 'Notas e Avaliações por Artista')

    with tab2:
        container = st.container(border=True)
        with container:
            row1 = st.columns([2,2])
            with row1[0]:
                reviewArtirtsByHouse = reviewArtirtsByHouse[['ARTISTA','ESTABELECIMENTO','NOTA', 'AVALIADOR']]
                plotDataframe(reviewArtirtsByHouse, "Avaliações Recentes")
            with row1[1]:
                averageReviewArtistByHouse_sorted = averageReviewArtistByHouse.sort_values(by='NÚMERO DE SHOWS', ascending=False)
                plotDataframe(averageReviewArtistByHouse_sorted, "Satisfação média do artista")
            
    with tab3:
        container = st.container(border=True)
        with container:
            row2 = st.columns([2,2])
            with row2[0]:
                reviewHouseByArtirst = reviewHouseByArtirst[['ESTABELECIMENTO','NOTA']]
                plotDataframe(reviewHouseByArtirst, "Avaliações Recentes")
            with row2[1]:
                plotDataframe(averageReviewHouseByArtist, "Satisfação média do estabelecimento")

# Desempenho Operacional
def buildOperationalPerformace(operationalPerformace, pizzaChart, ByWeek, artistCheckinCheckout, extract):    
    tab1, tab2= st.tabs(["Resumos", "Extratos"])
    with tab1:
        container1 = st.container(border=True)
        container2 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(pizzaChart['TIPO'], pizzaChart['QUANTIDADE'], "Tipos de Ocorrências")
                plotBarChart(ByWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por semana")
            with row1[1]:
                st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>Ranking de artistas com mais ocorrências</h5>", unsafe_allow_html=True)
                st.dataframe(operationalPerformace[['RANKING','ARTISTA', 'ESTILO','QUANTIDADE']].reset_index(drop=True), hide_index=True,use_container_width=True, height=735)

        with container2:    
            artistCheckinCheckout = artistCheckinCheckout.rename(columns={'QUANTIDADE_CHECKIN': 'QUANTIDADE DE CHECKIN', 'QUANTIDADE_CHECKOUT': 'QUANTIDADE DE CHECKOUT',
                                'TOTAL_SHOWS': 'NÚMERO DE SHOWS'})
            
            artistCheckinCheckout['PORCENTAGEM DE CHECKIN(%)'] = ((artistCheckinCheckout['QUANTIDADE DE CHECKIN'] * 100) / artistCheckinCheckout['NÚMERO DE SHOWS']).map("{:.2f}%".format)
            artistCheckinCheckout['PORCENTAGEM DE CHECKOUT(%)'] = ((artistCheckinCheckout['QUANTIDADE DE CHECKOUT'] * 100) / artistCheckinCheckout['NÚMERO DE SHOWS']).map("{:.2f}%".format)
            
            plotDataframe(artistCheckinCheckout[['ARTISTA', 'NÚMERO DE SHOWS', 'PORCENTAGEM DE CHECKIN(%)', 'PORCENTAGEM DE CHECKOUT(%)']], "Quantidade de checkin e checkout por artista")
    
    with tab2:
        # removendo valores e reodernando o dataset
        extract.drop(columns=['SEMANA'], inplace=True)
        extract = extract[['ARTISTA', 'ESTILO','ESTABELECIMENTO','DATA','TIPO']]
        
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
        ticket = 0 if total == 0 else  format_brazilian((sum(df['VALOR_BRUTO']) / total).quantize(Decimal('0.00')))
        value = format_brazilian(Decimal(sum(df['VALOR_BRUTO'])).quantize(Decimal('0.00')))

        # formatando df
        df_renamed = format_finances_dash(df)
        
        buttonDowloadDash(df, "Extrato-de-Shows")
        row1 = st.columns(4)

        tile = row1[0].container(border=True)
        tile.markdown(f"<p style='text-align: center;'>Total de Shows</br>{total}</p>", unsafe_allow_html=True)

        tile = row1[1].container(border=True)
        tile.markdown(f"<p style='text-align: center;'>Total de Horas em Shows</br>{total_hours}h {total_minutes}m {total_seconds}s</p>", unsafe_allow_html=True)

        tile = row1[2].container(border=True)
        tile.markdown(f"<p style='text-align: center;'>Valor Transacionado</br>R$ {value}</p>", unsafe_allow_html=True)

        tile = row1[3].container(border=True)
        tile.markdown(f"<p style='text-align: center;'>Ticket Médio</br>R$ {ticket}</p>", unsafe_allow_html=True)
        
        

        container = st.container(border=True)
        with container:
            plotDataframe(df_renamed, "Extrato de propostas e shows")
             