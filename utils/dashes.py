import streamlit as st
from utils.dbconnect import GET_PROPOSTAS_BY_ID_AND_DATE

def buildGeneralDash(id, date):
    st.header("DASH GERAL")
    container = st.container(border=True)
    with container:
        # Values
        row1 = st.columns(6)
        startDate = date[0]
        endDate = date[1]
        #ver questao do filtro de data
        df = GET_PROPOSTAS_BY_ID_AND_DATE(id, startDate, endDate)
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

def buildCorporativeDash():
    st.header("DASH ANALÍTICO CORPORATIVO MENSAL")

    tab1, tab2, tab3 = st.tabs(["CORPORATIVO MENSAL 1", "CORPORATIVO MENSAL 2", "CORPORATIVO MENSAL 3"])
    with tab1:
        st.header("CORPORATIVO MENSAL - 1")
    with tab2:
        st.header("CORPORATIVO MENSAL - 2")
    with tab3:
        st.header("CORPORATIVO MENSAL - 3")
        

    container = st.container(border=True)
    with container:
        st.write("show dataset")

def buildTemporalDash():
    st.header("DASH TEMPORAL")

def buildAnaliticsDash():
    st.header("DASH ANALÍTICO")

def buildByHouseDash():
    st.header("DASH POR CASA")

    tab1, tab2 = st.tabs(["CASA 1", "CASA 2"])
    with tab1:
        st.header("1 - Dash por casa")
    with tab2:
        st.header("2 - Dash por casa")

def buildReleaseControl():
    st.header("DASH TEMPORAL")