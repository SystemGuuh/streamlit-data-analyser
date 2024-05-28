import streamlit as st
from utils.dbconnect import GET_WEEKLY_FINANCES
import pandas as pd
from io import BytesIO
from utils.functions import *

# Função para criar um dicionário com dias da semana
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

# Função para formartar datafram de finanças
def formatFinancesDataframe(df):
    df['DIA_DA_SEMANA'] = df['DIA_DA_SEMANA'].apply(translate_day)
    df['VALOR_BRUTO'] = 'R$ ' + df['VALOR_BRUTO'].astype(str)
    df['VALOR_LIQUIDO'] = 'R$ ' + df['VALOR_LIQUIDO'].astype(str)
    
    df = df.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA', 'HORARIO_INICIO': 'HORÁRIO', 'DIA_DA_SEMANA': 'DIA DA SEMANA',
                     'VALOR_LIQUIDO': 'VALOR LÍQUIDO', 'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})

    return df

# Função para converter o arquivo para excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# Função para transformar valores em dinheiro
def format_brazilian(num):
        return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função para converter o tempo no formato "Xh Ym Zs" para timedelta
def parse_duration(duration_str):
    hours, minutes, seconds = 0, 0, 0
    if 'h' in duration_str:
        hours = int(duration_str.split('h')[0].strip())
        duration_str = duration_str.split('h')[1].strip()
    if 'm' in duration_str:
        minutes = int(duration_str.split('m')[0].strip())
        duration_str = duration_str.split('m')[1].strip()
    if 's' in duration_str:
        seconds = int(duration_str.split('s')[0].strip())
    return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)

# Função para somar coluna DURACAO e devolver o valor total de horas, minutos e segundos 
def sum_duration_from_dataframe(df):
    temp = df['DURACAO'].apply(parse_duration)
    total_duration = temp.sum()
    total_seconds = int(total_duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return hours, minutes, seconds

# Função para formatar os dados da tabela de finanças
def format_finances_dash(financeDash):
    copy = financeDash
    copy['VALOR_BRUTO'] = 'R$ ' + copy['VALOR_BRUTO'].apply(format_brazilian).astype(str)
    financeDash_renamed = copy.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA INÍCIO', 'DATA_FIM': 'DATA FIM','DURACAO' : 'DURAÇÃO','DIA_DA_SEMANA': 'DIA DA SEMANA',
                    'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})
    new_order = ['STATUS PROPOSTA','ARTISTA','ESTABELECIMENTO','DATA INÍCIO','DATA FIM','DURAÇÃO','DIA DA SEMANA','VALOR BRUTO','STATUS FINANÇEIRO']
    financeDash_renamed = financeDash_renamed[new_order]

    return financeDash_renamed