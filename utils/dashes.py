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

def buildComparativeDash(df):
    st.header("DASH ANALÍTICO COMPARATIVO MENSAL")

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
        
def buildReview(artistRanking, reviewArtirtsByHouse, reviewHouseByArtirst):
    #formating tables
    artistRanking['MEDIA_NOTAS'] = '⭐' + artistRanking['MEDIA_NOTAS'].astype(str)
    artistRanking = artistRanking.rename(columns={'NUM_SHOWS_ARTISTA': 'NÚMERO DE SHOWS', 'MEDIA_NOTAS': 'NOTAS', 'QUANTIDADE_AVALIACOES': 'AVALIAÇÕES'})
    artistRanking = artistRanking.drop(columns=['ID'])
    reviewArtirtsByHouse = reviewArtirtsByHouse.drop(columns=['ID_AVALIACAO', 'ID_PROPOSTA', 'GRUPO'])
    reviewHouseByArtirst = reviewHouseByArtirst.drop(columns=['ID_AVALIACAO', 'ID_PROPOSTA', 'GRUPO'])


    tab1, tab2= st.tabs(["Rancking", "Avaliações de casas e artistas"])
    with tab1:
        center = st.columns([1.5,2,1])
        with center[0]: 
            plotDataframe(artistRanking, "Ranking")
    with tab2:
        container = st.container(border=True)
        with container:
            with st.expander("Avaliações sobre artistas", expanded=True):
                row1 = st.columns(2)
                with row1[0]:
                    plotDataframe(reviewArtirtsByHouse, "Avaliações das Casas Sobre os Artistas")
                with row1[1]:
                    plotDataframe(reviewArtirtsByHouse, "Médias de Avaliações das Casas Sobre os Artistas")
            
            with st.expander("Avaliações sobre casas"):
                row2 = st.columns(2)
                with row2[0]:
                    plotDataframe(reviewHouseByArtirst, "Avaliações dos Artistas Sobre as Casas")
                with row2[1]:
                    plotDataframe(reviewHouseByArtirst, "Médias de Avaliações dos Artistas Sobre as Casas")

def buildOperationalPerformace(df):
    container = st.container(border=True)
    with container:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df)
        with col2:
            plotMapChart(df)

        st.dataframe(df)

def buildFinances(df):
    #formating tables
    df['VALOR_BRUTO'] = 'R$ ' + df['VALOR_BRUTO'].astype(str)
    df['VALOR_LIQUIDO'] = 'R$ ' + df['VALOR_LIQUIDO'].astype(str)
    df = df.drop(columns=['ID_PROPOSTA', 'ID_CASA', 'ID_ARTISTA'])


    st.header("DASH FINANCEIRO")
    tab1, tab2 = st.tabs(["SEMANAL", "MENSAL"])
    with tab1:
        printFinanceData(df)
        container = st.container(border=True)
        with container:
          plotDataframe(df, "Dados Financeiros Semanais")

    with tab2:
        container = st.container(border=True)
        with container:
            st.dataframe(df)  

def buildShowStatement(df):
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

def buildCompleteView(df):
    row1 = st.columns(4)
    row2 = st.columns(4)

    tile = row1[0].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row1[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row1[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row1[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row2[0].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row2[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row2[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)

    tile = row2[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Mais detalhes</br></h6>", unsafe_allow_html=True)
    
    container = st.container(border=True)
    with container:
        col1, col2, col3 = st.columns(3)
        with col1:
            plotDataframe(df, "Ranking - Experiência da Casa")
        with col2:
            plotDataframe(df, "Ranking - Experiência do Artista")
        with col3:
            plotDataframe(df, "Histórico por Semana - Experiência do Artistas")
        
        with st.expander("Ver Avaliações dos Artistas Sobre as Casas"):
            plotDataframe(df, "Avaliações dos Artistas Sobre as Casas")
        with st.expander("Ver Avaliações dos Gestores das Casas Sobre os Artistas"):
            plotDataframe(df, "Avaliações dos Gestores das Casas Sobre os Artistas")
             