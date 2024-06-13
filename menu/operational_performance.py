# menu/operational_performance.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildOperationalPerformace(operationalPerformace, ByOccurrence, ByWeek, checkinCheckout, allOperationalPerformaceByOccurrenceAndDate):
    tab1, tab2= st.tabs(["Resumos", "Extratos"])
    with tab1:
        container1 = st.container(border=True)
        container2 = st.container(border=True)
        with container1: 
            row1 = st.columns(2)
            with row1[0]:
                plotPizzaChart(ByOccurrence['TIPO'], ByOccurrence['QUANTIDADE'], "Tipos de Ocorrências")
                plotBarChart(ByWeek, 'SEMANA', 'QUANTIDADE', "Quantidade de ocorrêcias por semana")
            with row1[1]:
                st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>Ranking de artistas com mais ocorrências</h5>", unsafe_allow_html=True)
                st.dataframe(operationalPerformace[['RANKING','ARTISTA', 'ESTILO','QUANTIDADE']].reset_index(drop=True), hide_index=True,use_container_width=True, height=735)

        with container2:    
            checkinCheckout = checkinCheckout.rename(columns={'QUANTIDADE_CHECKIN': 'QUANTIDADE DE CHECKIN', 'QUANTIDADE_CHECKOUT': 'QUANTIDADE DE CHECKOUT',
                                'TOTAL_SHOWS': 'NÚMERO DE SHOWS'})
            
            # Calculando porcentagens
            checkinCheckout['PORCENTAGEM DE CHECKIN(%)'] = ((checkinCheckout['QUANTIDADE DE CHECKIN'] * 100) / checkinCheckout['NÚMERO DE SHOWS'])
            checkinCheckout['PORCENTAGEM DE CHECKOUT(%)'] = ((checkinCheckout['QUANTIDADE DE CHECKOUT'] * 100) / checkinCheckout['NÚMERO DE SHOWS'])
            
            # transformando valores None em 0
            checkinCheckout['PORCENTAGEM DE CHECKIN(%)'] = checkinCheckout['PORCENTAGEM DE CHECKIN(%)'].fillna(0)
            checkinCheckout['PORCENTAGEM DE CHECKOUT(%)'] = checkinCheckout['PORCENTAGEM DE CHECKOUT(%)'].fillna(0)

            # Adicionando '%' nas linhas
            checkinCheckout['PORCENTAGEM DE CHECKIN(%)'] = checkinCheckout['PORCENTAGEM DE CHECKIN(%)'].map("{:.2f}%".format)
            checkinCheckout['PORCENTAGEM DE CHECKOUT(%)'] = checkinCheckout['PORCENTAGEM DE CHECKOUT(%)'].map("{:.2f}%".format)

            plotDataframe(checkinCheckout[['ARTISTA', 'NÚMERO DE SHOWS', 'PORCENTAGEM DE CHECKIN(%)', 'PORCENTAGEM DE CHECKOUT(%)']], "Quantidade de checkin e checkout por artista")
    
    with tab2:
        # removendo valores e reodernando o dataset
        allOperationalPerformaceByOccurrenceAndDate.drop(columns=['SEMANA'], inplace=True)
        allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[['ARTISTA', 'ESTILO','ESTABELECIMENTO','DATA','TIPO']]
        
        row1 = st.columns(6)
        with row1[0]:
            type = filterReportType(allOperationalPerformaceByOccurrenceAndDate)
        with row1[1]:
            art = filterReportArtist(allOperationalPerformaceByOccurrenceAndDate)
        with row1[5]:
            st.write('') # alinhar botão
            st.write('') # alinhar botão
            buttonDowloadDash(allOperationalPerformaceByOccurrenceAndDate, "Extrato-de-Ocorrencias")
        container = st.container(border=True)
        with container:
            if type is not None:
                allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['TIPO']==type]
            if art is not None:
                allOperationalPerformaceByOccurrenceAndDate = allOperationalPerformaceByOccurrenceAndDate[allOperationalPerformaceByOccurrenceAndDate['ARTISTA']==art]

            plotDataframe(allOperationalPerformaceByOccurrenceAndDate, "Relatório completo de ocorrências")
    pass

class OperationalPerformacePage(Page):
    def render(self):
        buildOperationalPerformace(self.data['operationalPerformace'].copy(), 
                                   self.data['ByOccurrence'].copy(), 
                                   self.data['ByWeek'].copy(), 
                                   self.data['checkinCheckout'].copy(), 
                                   self.data['allOperationalPerformaceByOccurrenceAndDate'].copy())
