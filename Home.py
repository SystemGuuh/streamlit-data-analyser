import streamlit as st
from utils.monday import get_mysql_connection, getDfFromQuery
from utils.queries import GET_RADAR_FROM_BD
import threading
from datetime import datetime
import pytz

#colocar para printar o horário e dia da ultima atualização do bd
def run():
    st.set_page_config(
        page_title="Eshows Data",
        page_icon="🎤",
        layout="wide"
    )
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("# Radar de Implementação")

    st.markdown(
        """
        #### Visualização dos dados do Radar de Implementação:
        - **Visão Geral do Monday:** Página para visualizar dados coletados do Radar.
        - **Hunter:** Página para visualizar dados pertinentes a Hunters.
        - **Farmer:** Página para visualizar dados pertinentes a Farmers.
        - **Implementação:** Página para visualizar dados de implantantação.
        """
    )

if __name__ == "__main__":
    run()