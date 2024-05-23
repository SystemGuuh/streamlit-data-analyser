import streamlit as st
import datetime
from utils.dbconnect import GET_PROPOSTAS_BY_ID, GET_WEEKLY_FINANCES
import pandas as pd
import numpy as np
from datetime import date
from io import BytesIO
import matplotlib.pyplot as plt

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def filterCalendarComponent():
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=90)

    d = st.date_input("Filtro de data:", (thirty_days_ago, today),
                      format="DD/MM/YYYY")
    return d

def filterEstablishmentComponent(id):
    df = GET_PROPOSTAS_BY_ID(id, None, None)
    df_sorted = df.sort_values(by='ESTABLECIMENTO')
    option = st.selectbox("Estabelecimentos:",(df_sorted['ESTABLECIMENTO'].unique()),
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

    st.line_chart(df, x=xValue, y=yValue, use_container_width=True)

def plotPizzaChart(labels, sizes, name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    fig1, ax1 = plt.subplots()
    
    # Plotar o gráfico de pizza
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=-1, counterclock=False)

    # Ajustar a cor dos textos
    for text in texts:
        text.set_color('orange')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    # Remover sombra e fundo
    fig1.patch.set_alpha(0)
    ax1.axis('equal')

    # Melhorar a legibilidade dos textos
    plt.setp(autotexts, size=5, weight="bold")
    plt.setp(texts, size=8)

    st.pyplot(fig1)

def plotBarChart(df, xValue, yValue,name):
    st.markdown(f"<h5 style='text-align: center; background-color: #ffb131; padding: 0.1em;'>{name}</h5>", unsafe_allow_html=True)
    st.bar_chart(df, x=xValue, y=yValue, use_container_width=True)

def plotMapChart(df):
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
    st.map(df)
    
def printFinanceData(df):
    row2 = st.columns(4)
    tile = row2[0].container(border=True)
    

    tile.markdown(f"<h6 style='text-align: center;'>Shows Aceitos</br>{(df['STATUS_PROPOSTA'] == 'Aceita').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[1].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Shows Cancelados</br>{(df['STATUS_PROPOSTA'] == 'Cancelada').sum()}</h6>", unsafe_allow_html=True)

    tile = row2[2].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Bruto Total</br>R$ {'{:.2f}'.format(df['VALOR_BRUTO'].sum())}</h6>", unsafe_allow_html=True)

    tile = row2[3].container(border=True)
    tile.markdown(f"<h6 style='text-align: center;'>Valor Líquido Total</br>R$ {'{:.2f}'.format(df['VALOR_LIQUIDO'].sum())}</h6>", unsafe_allow_html=True)

def filterFinanceStatus(df):
    option = st.selectbox("Status Financeiro:",(df['STATUS_FINANCEIRO'].unique()),
            index=None, placeholder="Escolha um")
    return option

def translate_day(dia):
    dias_da_semana = {
    'Monday': 'Segunda-feira',
    'Tuesday': 'Terça-feira',
    'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira',
    'Friday': 'Sexta-feira',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
    }

    return dias_da_semana[dia]

def formatFinancesDataframe(df):
    df['DIA_DA_SEMANA'] = df['DIA_DA_SEMANA'].apply(translate_day)
    df['VALOR_BRUTO'] = 'R$ ' + df['VALOR_BRUTO'].astype(str)
    df['VALOR_LIQUIDO'] = 'R$ ' + df['VALOR_LIQUIDO'].astype(str)
    
    df = df.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA', 'HORARIO_INICIO': 'HORÁRIO', 'DIA_DA_SEMANA': 'DIA DA SEMANA',
                     'VALOR_LIQUIDO': 'VALOR LÍQUIDO', 'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})

    return df

def plotFinanceWeeklyChart(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    df['VALOR_GANHO_BRUTO'] = df['VALOR_GANHO_BRUTO'].astype(int)

    with st.expander("Gráfico de barras", expanded=True):
        st.bar_chart(df[['NUMERO_SEMANA','VALOR_GANHO_BRUTO']], x='NUMERO_SEMANA', y='VALOR_GANHO_BRUTO', color=["#ff6600"])
    with st.expander("Gráfico de linhas"):
        st.line_chart(df[['NUMERO_SEMANA','VALOR_GANHO_BRUTO']], x='NUMERO_SEMANA', y='VALOR_GANHO_BRUTO', color=["#ff6600"])
    
def plotFinanceMonthlyChart(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    df['VALOR_GANHO_BRUTO'] = df[['VALOR_GANHO_BRUTO']].astype(int)
    with st.expander("Gráfico de barras", expanded=True):
        st.bar_chart(df[['NUMERO_MES','VALOR_GANHO_BRUTO']], x='NUMERO_MES', y='VALOR_GANHO_BRUTO', color=["#ffcc00"])
    with st.expander("Gráfico de linhas"):
        st.line_chart(df[['NUMERO_MES','VALOR_GANHO_BRUTO']], x='NUMERO_MES', y='VALOR_GANHO_BRUTO', color=["#ffcc00"])

def weeklyeDaysNumber(id, year):
    df = GET_WEEKLY_FINANCES(id, year)
    st.dataframe(df[['NUMERO_SEMANA', 'DIA']], hide_index=True, use_container_width=True)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def buttonDowloadDash(df, name):
    st.download_button(
    label='Baixar em Excel',
    data=to_excel(df),
    file_name=f"{name}.xlsx",
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def format_brazilian(num):
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
