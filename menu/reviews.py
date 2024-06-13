# menu/review.py
import streamlit as st
from utils.components import *
from utils.functions import *
from decimal import Decimal

from menu.page import Page

def buildReview(artistRanking, reviewArtistByHouse, averageReviewArtistByHouse, reviewHouseByArtist, averageReviewHouseByArtist):
    artistRanking = artistRanking.rename(columns={'NUM_SHOWS_ARTISTA': 'NÚMERO DE SHOWS', 'MEDIA_NOTAS': 'MÉDIA', 'QUANTIDADE_AVALIACOES': 'NÚMERO DE AVALIAÇÕES'})

    tab1, tab2, tab3= st.tabs(["Ranking", "Avaliações de Estabelecimento para Artista", "Avaliações de Artista para Estabelecimento"])
    with tab1:
        container = st.container(border=True)
        with container:
            center = st.columns([2,2])
            with center[0]:
                option = filterReportArtist(artistRanking) 
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
                reviewArtistByHouse = reviewArtistByHouse[['ARTISTA','ESTABELECIMENTO','NOTA', 'AVALIADOR', 'COMENTÁRIO', 'DATA']]
                plotDataframe(reviewArtistByHouse, "Avaliações Recentes")
            with row1[1]:
                averageReviewArtistByHouse_sorted = averageReviewArtistByHouse.sort_values(by='NÚMERO DE SHOWS', ascending=False)
                plotDataframe(averageReviewArtistByHouse_sorted, "Satisfação média do artista")
            
    with tab3:
        container = st.container(border=True)
        with container:
            row2 = st.columns([2,2])
            with row2[0]:
                reviewHouseByArtist = reviewHouseByArtist[['ESTABELECIMENTO','NOTA']]
                plotDataframe(reviewHouseByArtist, "Avaliações Recentes")
            with row2[1]:
                plotDataframe(averageReviewHouseByArtist, "Satisfação média do estabelecimento")
    pass

class ReviewPage(Page):
    def render(self):
        buildReview(self.data['artistRanking'].copy(), 
                    self.data['reviewArtistByHouse'].copy(), 
                    self.data['averageReviewArtistByHouse'].copy(), 
                    self.data['reviewHouseByArtist'].copy(), 
                    self.data['averageReviewHouseByArtist'].copy())
