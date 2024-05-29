import streamlit as st
from utils.dbconnect import GET_WEEKLY_FINANCES
import pandas as pd
from io import BytesIO
from utils.functions import *
import re

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

# Função de tradução de horas
def translate_duration(duration):
    if isinstance(duration, pd.Timedelta):
        total_seconds = duration.total_seconds()
        if total_seconds == 1800:  # 30 minutos
            return 'meia hora'
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f'{int(minutes)} minutos'
        elif total_seconds < 86400:  # menos que um dia
            hours = total_seconds // 3600
            return f'{int(hours)} hora' if hours == 1 else f'{int(hours)} horas'
        else:
            days = total_seconds // 86400
            return f'{int(days)} dia' if days == 1 else f'{int(days)} dias'
    return str(duration)

# Função para formatar os dados da tabela de finanças
def format_finances_dash(financeDash):
    copy = financeDash

    # Colocando mascara nos valores
    copy['VALOR_BRUTO'] = 'R$ ' + copy['VALOR_BRUTO'].apply(format_brazilian).astype(str)
    copy['DATA_INICIO'] = pd.to_datetime(copy['DATA_INICIO'], dayfirst=True)
    copy['DATA_FIM'] = pd.to_datetime(copy['DATA_FIM'], dayfirst=True)
    copy['DATA_INICIO'] = copy['DATA_INICIO'].dt.strftime('%d/%m/%Y')
    copy['DATA_FIM'] = copy['DATA_FIM'].dt.strftime('%d/%m/%Y')
    copy['DURACAO'] = copy['DURACAO'].apply(translate_duration)

    # Renomeando e removendo colunas
    financeDash_renamed = copy.rename(columns={'STATUS_PROPOSTA': 'STATUS PROPOSTA', 'DATA_INICIO': 'DATA INÍCIO', 'DATA_FIM': 'DATA FIM','DURACAO' : 'DURAÇÃO','DIA_DA_SEMANA': 'DIA DA SEMANA',
                    'VALOR_BRUTO': 'VALOR BRUTO', 'STATUS_FINANCEIRO': 'STATUS FINANÇEIRO'})
    new_order = ['STATUS PROPOSTA','ARTISTA','ESTABELECIMENTO','DATA INÍCIO','DATA FIM','DURAÇÃO','DIA DA SEMANA','VALOR BRUTO','STATUS FINANÇEIRO']
    financeDash_renamed = financeDash_renamed[new_order]

    return financeDash_renamed

def order_and_format_month_dataframe(df):
    # Definindo a ordem dos meses
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Criando um DataFrame com todos os meses
    all_months = pd.DataFrame({'MES': range(1, 13)})
    all_months['MES'] = pd.Categorical(all_months['MES'], categories=range(1, 13), ordered=True)
    all_months['MES'] = all_months['MES'].cat.rename_categories(month_order)

    # Mesclando os dados originais com todos os meses
    df = pd.merge(all_months, df, on='MES', how='left')

    # Ordenar o DataFrame pelo mês(index)
    df = df.sort_index()

    # Zerando os valores null
    df['VALOR_GANHO_BRUTO'] = df['VALOR_GANHO_BRUTO'].fillna(0)

    # Traduzir os meses para português
    df['MES'] = df['MES'].replace({'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março', 'April': 'Abril', 'May': 'Maio', 'June': 'Junho', 'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro', 'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'})

    return df
