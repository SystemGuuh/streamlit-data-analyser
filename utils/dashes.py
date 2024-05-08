import streamlit as st

def buildGeneralDash():
    st.header("DASH GERAL")
    container = st.container(border=True)
    with container:
        row1 = st.columns(6)

        tile = row1[0].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Núm. de Shows</h6>", unsafe_allow_html=True)

        tile = row1[1].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Valor Transacionado</h6>", unsafe_allow_html=True)

        tile = row1[2].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Estabelecimentos</h6>", unsafe_allow_html=True)

        tile = row1[3].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Ticket Médio</h6>", unsafe_allow_html=True)

        tile = row1[4].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Média de Shows por Casa</h6>", unsafe_allow_html=True)

        tile = row1[5].container(border=True)
        tile.markdown("<h6 style='text-align: center;'>Artistas Distintos</h6>", unsafe_allow_html=True)

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