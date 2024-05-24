import streamlit as st
import datetime
from utils.dbconnect import GET_PROPOSTAS_BY_ID, GET_WEEKLY_FINANCES
import pandas as pd
import numpy as np
from datetime import date
from streamlit_echarts import st_echarts
from utils.functions import *
from decimal import Decimal

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# resolve o bug de carregamento dos gráficos de echart
def fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 300px;} 
   </style>
    """

    return st.markdown(streamlit_style, unsafe_allow_html=True)

def filterCalendarComponent():
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=90)

    d = st.date_input("Filtro de data:", (thirty_days_ago, today),
                      format="DD/MM/YYYY")
    return d

def filterEstablishmentComponent(id):
    df = GET_PROPOSTAS_BY_ID(id, None, None)
    df_sorted = df.sort_values(by='ESTABELECIMENTO')
    option = st.selectbox("Estabelecimentos:",(df_sorted['ESTABELECIMENTO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def filterProposalComponent():
    option = st.multiselect("Proposta da semana recorrente:",['Aceita','Cancelada','Recusada','Pendente','Checkin Realizado','Checkout Realizado'], ['Aceita', 'Cancelada'])
    return option

def filterYearChartFinances():
    current_year = date.today().year
    years = list(range(2015, current_year + 1))
    years.insert(0, "Escolha um ano:")
    option = st.selectbox("Escolha um ano:", years, index=years.index(2024))
    return option

def filterReportType(df):
    option = st.selectbox("Tipo de ocorrência:",(df['TIPO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def plotDataframe(df, name):
    st.markdown(f"<h4 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h4>", unsafe_allow_html=True)
    st.dataframe(df, hide_index=True, use_container_width=True)

def plotLineChart(df, xValue, yValue,name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    
    if df[xValue].dtype == 'object':
        # Tentar converter os valores para o tipo datetime
        try:
            df_sorted = df.sort_values(by=xValue)
            df_sorted[xValue] = pd.to_datetime(df_sorted[xValue])
            df_sorted[xValue] = df_sorted[xValue].dt.strftime('%d/%m/%Y')
        except ValueError:
            df_sorted = df

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross"
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": df_sorted[xValue].tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": df_sorted[yValue].tolist(),
                "type": "line",
                "lineStyle": {
                    "color": "#ff6600",  # Cor laranja para a linha
                    "width": 4
                },
                "areaStyle": {
                    "color": "#808080"  # Cor amarela para a área abaixo da linha
                }
            }
        ],
    }
    st_echarts(options=options, height="300px")

def plotPizzaChart(labels, sizes, name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    
    # Preparar os dados para o gráfico
    data = [{"value": size, "name": label} for size, label in zip(sizes, labels)]
    
    options = {
        "tooltip": {"trigger": "item"},
        "legend": {
            "orient": "vertical",
            "left": "left",
            "top": "top", 
            "textStyle": {
                "color": "orange"
            }
        },
        "grid": {  # Adicionado para organizar o layout
            "left": "50%", 
            "right": "50%", 
            "containLabel": True
        },
        "series": [
            {
                "name": "Quantidade",
                "type": "pie",
                "radius": "75%",
                "center": ["75%", "45%"],  # Posiciona o gráfico no meio verticalmente
                "data": data,
                "label": {
                    "show": False  # Ocultar os textos nas fatias
                },
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                    }
                },
            }
        ],
    }
    
    st_echarts(options=options, height="300px")
    
def plotBarChart(df, xValue, yValue,name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    
    if df[xValue].dtype == 'object':
        # Tentar converter os valores para o tipo datetime
        try:
            df_sorted = df.sort_values(by=xValue)
            df_sorted[xValue] = pd.to_datetime(df_sorted[xValue])
            df_sorted[xValue] = df_sorted[xValue].dt.strftime('%d/%m/%Y')
        except ValueError:
            df_sorted = df

    options = {
        "xAxis": {
            "type": "category",
            "data": df_sorted[xValue].tolist(),
        },
        "yAxis": {"type": "value"},
        "series": [
            {
                "data": df_sorted[yValue].tolist(),
                "type": "bar",
                "itemStyle": {
                    "color": "#ff6600"
                },
                "barWidth": "50%"  # Ajuste a largura das colunas aqui
            }
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "4%",
            "bottom": "3%",
            "containLabel": True
        },
        "legend": {
            "data": [yValue],
            "textStyle": {
                "color": "orange"
            }
        }
    }
    
    st_echarts(options=options, height="300px")

def plotMapChart(df):
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    st.map(df)
    
def printFinanceData(df):
    row2 = st.columns(4)
    tile = row2[0].container(border=True)

    total_brute = format_brazilian(sum(df['VALOR_BRUTO']).quantize(Decimal('0.00')))
    total_liquid = format_brazilian(sum(df['VALOR_LIQUIDO']).quantize(Decimal('0.00')))
    
    tile.markdown(f"<h6 style='text-align: center;'>Shows Aceitos</br>{(df['STATUS_PROPOSTA'] == 'Aceita').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Shows Cancelados</br>{(df['STATUS_PROPOSTA'] == 'Cancelada').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Bruto Total</br>R$ {total_brute}</h6>", unsafe_allow_html=True)

    tile = row2[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Líquido Total</br>R$ {total_liquid}</h6>", unsafe_allow_html=True)

def filterFinanceStatus(df):
    option = st.selectbox("Status Financeiro:",(df['STATUS_FINANCEIRO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def plotFinanceWeeklyChart(df):
    df['VALOR_GANHO_BRUTO'] = df['VALOR_GANHO_BRUTO'].astype(int)

    with st.expander("Gráfico de barras", expanded=True):
        plotBarChart(df, 'NUMERO_SEMANA', 'VALOR_GANHO_BRUTO', 'Valor ganho por semana')
    with st.expander("Gráfico de linhas"):
        plotLineChart(df, 'NUMERO_SEMANA', 'VALOR_GANHO_BRUTO', 'Valor ganho por semana')
    
def plotFinanceMonthlyChart(df):
    df['VALOR_GANHO_BRUTO'] = df[['VALOR_GANHO_BRUTO']].astype(int)

    with st.expander("Gráfico de barras", expanded=True):
        plotBarChart(df, 'MES', 'VALOR_GANHO_BRUTO', 'Valor ganho por mês')
    with st.expander("Gráfico de linhas"):
        plotLineChart(df, 'MES', 'VALOR_GANHO_BRUTO', 'Valor ganho por mês')

def buttonDowloadDash(df, name):
    st.download_button(
    label='Baixar em Excel',
    data=to_excel(df),
    file_name=f"{name}.xlsx",
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

