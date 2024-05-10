import streamlit as st
from utils.components import *

def buildGeneralDash(df):
    container = st.container(border=True)
    with container:
        # Values
        row1 = st.columns(6)

        showNumbers = df.shape[0]
        trasactionValue = round(df['VALOR_BRUTO'].sum(), 2)
        countEstablishments = df['CASA'].nunique()
        averageTicket = round(df['VALOR_LIQUIDO'].mean(), 2)

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

def buildCorporativeDash(df):
    st.header("DASH ANALÍTICO CORPORATIVO MENSAL")

    tab1, tab2, tab3 = st.tabs(["CORPORATIVO MENSAL 1", "CORPORATIVO MENSAL 2", "CORPORATIVO MENSAL 3"])
    with tab1:
        container = st.container(border=True)
        with container:
            st.dataframe(df, hide_index=1)
            plotDataframe(df, "Valores por dia da semana")
    with tab2:
        container = st.container(border=True)
        with container:
            chart_data = df[["ARTISTA", "VALOR_BRUTO", "VALOR_LIQUIDO"]]
            st.line_chart(chart_data, x="ARTISTA", y=("VALOR_BRUTO", "VALOR_LIQUIDO"))

            plotDataframe(df, "Dados por establecimento/mês")
    with tab3:
        container = st.container(border=True)
        with container:
            chart_data = df[["ARTISTA", "VALOR_BRUTO", "VALOR_LIQUIDO"]]
            st.line_chart(chart_data, x="ARTISTA", y=("VALOR_BRUTO", "VALOR_LIQUIDO"))
            plotDataframe(df, "Dados por establecimento/mês")
        
def buildTemporalDash(df):
    container = st.container(border=True)
    with container:
        chart_data = df[["ARTISTA", "VALOR_BRUTO", "VALOR_LIQUIDO"]]
        plotLineChart(chart_data, "ARTISTA", ["VALOR_BRUTO", "VALOR_LIQUIDO"], "Número de shows e custo total")

        col1, col2 = st.columns(2)
        with col1:
            plotBarChart("Estilos principais dos artistas")
        with col2:
            st.dataframe(df)

def buildAnaliticsDash(df):
    container = st.container(border=True)
    with container:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df)
        with col2:
            plotMapChart(df)

        st.dataframe(df)

def buildByHouseDash(df):
    st.header("DASH POR CASA")

    tab1, tab2 = st.tabs(["CASA 1", "CASA 2"])
    with tab1:
        container = st.container(border=True)
        with container:
            # Values
            row1 = st.columns(5)

            showNumbers = df.shape[0]
            transactionValue = round(df['VALOR_BRUTO'].sum(), 2)
            averageTicket = round(df['VALOR_LIQUIDO'].mean(), 2)
            musicalStyles = 1 #calcular com query

            
            distinctArtists = df['ARTISTA'].nunique()
            
            # Page
            tile = row1[0].container(border=True)
            tile.markdown(f"<h6 style='text-align: center;'>Número de Shows</br>{showNumbers}</h6>", unsafe_allow_html=True)

            tile = row1[1].container(border=True)
            tile.markdown(f"<h6 style='text-align: center;'>Artistas Distintos</br>{distinctArtists}</h6>", unsafe_allow_html=True)

            tile = row1[2].container(border=True)
            tile.markdown(f"<h6 style='text-align: center;'>Valor Transacionado</br>R$ {transactionValue}</h6>", unsafe_allow_html=True)

            tile = row1[3].container(border=True)
            tile.markdown(f"<h6 style='text-align: center;'>Ticket Médio</br>R$ {averageTicket}</h6>", unsafe_allow_html=True)

            tile = row1[4].container(border=True)
            tile.markdown(f"<h6 style='text-align: center;'>Estilos Musicais</br>{musicalStyles}</h6>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                plotDataframe(df, "Primeira Quinzena")
            with col2:
                plotDataframe(df, "Segunda Quinzena")

    with tab2:
        container = st.container(border=True)
        with container:
            plotDataframe(df, "Extrato de Shows")  

def buildReleaseControl(df):
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        filterProposal = filterProposalComponent()
    with col3:
        st.info('⚠️ Filtro de data não será aplicado!')
    
    # Fazer filtro de proposta
    container = st.container(border=True)
    with container:
        df_filtrado = df[df['STATUS_PROPOSTA'].str.contains('|'.join(filterProposal))]
        plotDataframe(df_filtrado, "Controle Lançamentos da semana corrente")