import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime

def get_mysql_connection():
    mysql_config = st.secrets["mysql"]
    # Create MySQL connection
    conn = mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database'],
        user=mysql_config['username'],
        password=mysql_config['password']
    )    
    return conn

def execute_query(query):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Obter nomes das colunas
    column_names = [col[0] for col in cursor.description]
    
    # Obter resultados
    result = cursor.fetchall()
    
    cursor.close()
    return result, column_names

def getDfFromQuery(consulta):
    result, column_names = execute_query(consulta)
    return pd.DataFrame(result, columns=column_names)

# query para retornar propostas por data
def GET_PROPOSTAS_BY_ID_AND_DATE(id, startDate, endDate):
    return getDfFromQuery(f"""SELECT
                            P.ID AS ID_PROPOSTA,
                            CASE 
                                WHEN S.DESCRICAO IS NULL THEN "Cancelada"
                                ELSE S.DESCRICAO
                            END AS STATUS_PROPOSTA,
                            C.NAME AS CASA,
                            A.NOME AS ARTISTA,
                            DATE_FORMAT(DATA_INICIO, '%d/%m/%y') AS DATA_INICIO, 
                            DATE_FORMAT(DATA_INICIO, '%H:%i') AS HORARIO_INICIO,
                            DATE_FORMAT(DATA_FIM, '%d/%m/%y') AS DATA_FIM, 
                            DATE_FORMAT(DATA_FIM, '%H:%i') AS HORARIO_FIM,
                            TIMEDIFF(DATA_FIM, DATA_INICIO) AS DURACAO,
                            DAYNAME(DATA_INICIO) AS DIA_DA_SEMANA,
                            P.VALOR_BRUTO,
                            P.VALOR_LIQUIDO,
                            P.VALOR_BRUTO_OCULTO,
                            SF.DESCRICAO AS STATUS_FINANCEIRO,
                            F.FONTE,
                            P.B2C,
                            P.ADIANTAMENTO,
                            C.ID AS ID_CASA,
                            A.ID AS ID_ARTISTA,
                            P.FK_USUARIO,
                            GU.FK_USUARIO
                        FROM T_PROPOSTAS P
                        LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                        LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                        LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                        LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
                        LEFT JOIN T_FONTE F ON (F.ID = P.FK_FONTE)
                        INNER JOIN T_GRUPO_USUARIO GU ON GU.FK_USUARIO = P.FK_USUARIO
                        WHERE P.TESTE = 0 
                            AND P.FK_CONTRANTE IS NOT NULL 
                            AND P.FK_CONTRATADO IS NOT NULL 
                            AND P.DATA_INICIO IS NOT NULL 
                            AND P.FK_USUARIO = {id}
                            AND P.DATA_INICIO >= '{startDate}'
                            AND P.DATA_FIM <= '{endDate}'
                            AND GU.STATUS = 1
                            AND GU.FK_PERFIL IN (100,101)
                        """)

# query para retornar propostas por id
@st.cache_data
def GET_PROPOSTAS_BY_ID(id):
    return getDfFromQuery(f"""
                    SELECT DISTINCT
                        P.ID AS ID_PROPOSTA,
                        CASE 
                            WHEN S.DESCRICAO IS NULL THEN "Cancelada"
                            ELSE S.DESCRICAO
                        END AS STATUS_PROPOSTA,
                        C.NAME AS CASA,
                        A.NOME AS ARTISTA,
                        DATE_FORMAT(DATA_INICIO, '%d/%m/%y') AS DATA_INICIO, 
                        DATE_FORMAT(DATA_INICIO, '%H:%i') AS HORARIO_INICIO,
                        DATE_FORMAT(DATA_FIM, '%d/%m/%y') AS DATA_FIM, 
                        DATE_FORMAT(DATA_FIM, '%H:%i') AS HORARIO_FIM,
                        TIMEDIFF(DATA_FIM, DATA_INICIO) AS DURACAO,
                        DAYNAME(DATA_INICIO) AS DIA_DA_SEMANA,
                        P.VALOR_BRUTO,
                        P.VALOR_LIQUIDO,
                        SF.DESCRICAO AS STATUS_FINANCEIRO,
                        C.ID AS ID_CASA,
                        A.ID AS ID_ARTISTA
                        
                    FROM T_PROPOSTAS P
                    LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                    LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                    LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                    LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)
                    INNER JOIN T_GRUPO_USUARIO GU ON GU.FK_USUARIO = P.FK_USUARIO 
                            AND GU.STATUS = 1
                        AND GU.FK_PERFIL IN (100,101)
                        
                    WHERE P.TESTE = 0 
                        AND P.FK_CONTRANTE IS NOT NULL 
                        AND P.FK_CONTRATADO IS NOT NULL 
                        AND P.DATA_INICIO IS NOT NULL 
                        AND P.FK_USUARIO = {id}
                        """)

@st.cache_data
def GET_USER_NAME(id):
    return getDfFromQuery(f"""SELECT 
                            TGU.FK_USUARIO,
                            AU.FULL_NAME
                            FROM T_GRUPO_USUARIO TGU
                            INNER JOIN ADMIN_USERS AU ON TGU.FK_USUARIO = AU.ID
                            WHERE
                                TGU.FK_USUARIO = {id}
                            GROUP BY AU.ID
                          """)

def convert_date(row):
    try:
        row['DATA_INICIO'] = datetime.strptime(row['DATA_INICIO'], '%d/%m/%y').date()
        row['DATA_FIM'] = datetime.strptime(row['DATA_FIM'], '%d/%m/%y').date()
    except ValueError:
        row['DATA_INICIO'] = None
        row['DATA_FIM'] = None 
    return row

def getDataframeDashGeral(id, date, establishment):
    df = GET_PROPOSTAS_BY_ID(id)
    if len(date) > 1 and date[0] is not None and date[1] is not None:
        startDate = date[0]
        endDate = date[1]
        df = df.apply(convert_date, axis=1)
        df = df.dropna(subset=['DATA_INICIO'])
        
        df = df[df['DATA_INICIO'] >= startDate]
        df = df[df['DATA_FIM'] <= endDate]

    if establishment is not None:
        df = df[df['CASA'] == establishment]
    
    return df

