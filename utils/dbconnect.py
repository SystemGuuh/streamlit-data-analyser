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

def convert_date(row):
    try:
        row['DATA_INICIO'] = datetime.strptime(row['DATA_INICIO'], '%d/%m/%y').date()
        row['DATA_FIM'] = datetime.strptime(row['DATA_FIM'], '%d/%m/%y').date()
    except ValueError:
        row['DATA_INICIO'] = None
        row['DATA_FIM'] = None 
    return row

def apply_filter_in_dataframe(df, date, establishment):
    if len(date) > 1 and date[0] is not None and date[1] is not None:
        startDate = pd.Timestamp(date[0])
        endDate = pd.Timestamp(date[1])
        df = df.dropna(subset=['DATA_AVALIACAO'])
    
        df = df[df['DATA_AVALIACAO'] >= startDate]
        df = df[df['DATA_AVALIACAO'] <= endDate]

    if establishment is not None:
        df = df[df['CASA'] == establishment]

    return df

def apply_filter_in_finance_dataframe(df, date, establishment):
    if len(date) > 1 and date[0] is not None and date[1] is not None:
        startDate = pd.Timestamp(date[0])
        endDate = pd.Timestamp(date[1])
        df = df.dropna(subset=['DATA_INICIO'])
    
        df = df[df['DATA_INICIO'] >= startDate]
        df = df[df['DATA_FIM'] <= endDate]

    if establishment is not None:
        df = df[df['CASA'] == establishment]

    return df

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

@st.cache_data
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

@st.cache_data # Avaliações - Avaliações da casa
def GET_REVIEW_ARTIST_BY_HOUSE(id, date, establishment):
    df = getDfFromQuery(f"""SELECT
                            A.NOME AS ARTISTA,
                            C.NAME AS CASA,
                            GC.GRUPO_CLIENTES AS GRUPO,
                            AV.NOTA,
                            AV.COMENTARIO,
                            AU.FULL_NAME AS AVALIADOR,
                            AU.LOGIN AS EMAIL_AVALIADOR,
                            P.DATA_INICIO AS DATA_PROPOSTA,
                            AV.LAST_UPDATE AS DATA_AVALIACAO

                            FROM T_AVALIACAO_ATRACOES AV
                            INNER JOIN T_PROPOSTAS P ON (P.ID = AV.FK_PROPOSTA)
                            LEFT JOIN ADMIN_USERS AU ON (AU.ID = AV.LAST_USER)
                            INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                            INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                            LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                            LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                            WHERE
                            GU.STATUS = 1
                            AND GU.FK_USUARIO = {id}
                        """)
    
    return apply_filter_in_dataframe(df, date, establishment)

@st.cache_data # Avaliações - Avaliações da casa
def GET_REVIEW_HOUSE_BY_ARTIST(id):
    return getDfFromQuery(f"""SELECT
                        C.NAME AS CASA,
                        GC.GRUPO_CLIENTES AS GRUPO,
                        AC.NOTA,
                        AC.COMENTARIO

                        FROM T_AVALIACAO_CASAS AC
                        INNER JOIN T_PROPOSTAS P ON (P.ID = AC.FK_PROPOSTA)
                        LEFT JOIN ADMIN_USERS AU ON (AU.ID = AC.LAST_USER)
                        INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                        INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                        LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                        LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                        WHERE 
                        GU.STATUS = 1
                        AND GU.FK_USUARIO = {id}
                        AND AC.NOTA > 0
                        """)   

@st.cache_data # Avaliações - Avaliações da casa
def GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id):
    return getDfFromQuery(f"""SELECT
                            A.NOME AS ARTISTA,
                            ROUND(AVG(AV.NOTA), 2) AS MEDIA_NOTAS,
                            COUNT(DISTINCT AV.ID) AS QUANTIDADE_AVALIACOES,
                            COUNT(P.FK_CONTRATADO) AS NUM_SHOWS_ARTISTA

                            FROM T_AVALIACAO_ATRACOES AV
                            INNER JOIN T_PROPOSTAS P ON (P.ID = AV.FK_PROPOSTA)
                            LEFT JOIN ADMIN_USERS AU ON (AU.ID = AV.LAST_USER)
                            INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                            INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                            LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                            LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                            WHERE
                            GU.STATUS = 1
                            AND GU.FK_USUARIO = {id}
                            GROUP BY
                            A.ID, A.NOME
                            ORDER BY
                            MEDIA_NOTAS DESC, QUANTIDADE_AVALIACOES DESC;
    """)

@st.cache_data # Avaliações - Avaliações da casa
def GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id):
    return getDfFromQuery(f"""SELECT
                            C.NAME AS CASA,
                            ROUND(AVG(AC.NOTA), 2) AS MEDIA_NOTAS,
                            COUNT(DISTINCT AC.ID) AS QUANTIDADE_AVALIACOES,
                            COUNT(P.FK_CONTRANTE) AS NUM_SHOWS_CASA

                            FROM T_AVALIACAO_CASAS AC
                            INNER JOIN T_PROPOSTAS P ON (P.ID = AC.FK_PROPOSTA)
                            LEFT JOIN ADMIN_USERS AU ON (AU.ID = AC.LAST_USER)
                            INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                            INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                            LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                            LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                            WHERE 
                            GU.STATUS = 1
                            AND GU.FK_USUARIO = {id}
                            AND AC.NOTA > 0
                            GROUP BY
                            C.ID, C.NAME
                            ORDER BY
                            MEDIA_NOTAS DESC, QUANTIDADE_AVALIACOES DESC;
    """)

# Avaliações - Rancking
def GET_ARTIST_RANKING(id):
    return  getDfFromQuery(f"""#RANCKIG DE ARTISTAS
                        SELECT
                        A.ID,
                        A.NOME AS ARTISTA,
                        ROUND(AVG(AV.NOTA), 2) AS MEDIA_NOTAS,
                        COUNT(DISTINCT AV.ID) AS QUANTIDADE_AVALIACOES,
                        COUNT(P.FK_CONTRATADO) AS NUM_SHOWS_ARTISTA
                    FROM
                        T_AVALIACAO_ATRACOES AV
                    INNER JOIN
                        T_PROPOSTAS P ON P.ID = AV.FK_PROPOSTA
                    INNER JOIN
                        T_COMPANIES C ON C.ID = P.FK_CONTRANTE
                    INNER JOIN
                        T_ATRACOES A ON A.ID = P.FK_CONTRATADO
                    LEFT JOIN
                        T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID
                    WHERE
                        GU.STATUS = 1
                        AND GU.FK_USUARIO = {id}
                        AND A.ID NOT IN (12166)
                    GROUP BY
                        A.ID, A.NOME
                    ORDER BY
                        MEDIA_NOTAS DESC, QUANTIDADE_AVALIACOES DESC;
                        """)

@st.cache_data # Financeiro
def GET_GERAL_INFORMATION_AND_FINANCES(id, date, establishment):
    df =getDfFromQuery(f"""
                        SELECT
                        S.DESCRICAO AS STATUS_PROPOSTA,
                        SF.DESCRICAO AS STATUS_FINANCEIRO,
                        C.NAME AS CASA,
                        A.NOME AS ARTISTA,
                        P.DATA_INICIO AS DATA_INICIO,
                        P.DATA_FIM AS DATA_FIM,
                        TIMEDIFF(P.DATA_FIM, P.DATA_INICIO) AS DURACAO,
                        DAYNAME(P.DATA_INICIO) AS DIA_DA_SEMANA,
                        P.VALOR_BRUTO,
                        P.VALOR_LIQUIDO,
                        F.ID AS ID_FECHAMENTO,
                        F.DATA_INICIO AS INICIO_FECHAMENTO,
                        F.DATA_FIM AS FIM_FECHAMENTO

                        FROM T_PROPOSTAS P
                        INNER JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                        INNER JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                        LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                        INNER JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID
                        INNER JOIN T_FECHAMENTOS F ON F.ID = P.FK_FECHAMENTO
                        LEFT JOIN T_PROPOSTA_STATUS_FINANCEIRO SF ON (P.FK_STATUS_FINANCEIRO = SF.ID)

                        WHERE 
                        P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                        AND GU.FK_USUARIO = {id}
                        """)
    
    return apply_filter_in_finance_dataframe(df, date, establishment)

@st.cache_data # Financeiro
def GET_WEEKLY_FINANCES(id, year):
    return getDfFromQuery(f"""
                        SELECT
                            MONTHNAME(P.DATA_INICIO) AS MES,
                            MONTH(P.DATA_INICIO) AS NUMERO_MES,
                            WEEK(P.DATA_INICIO) AS NUMERO_SEMANA,
                            DATE_FORMAT(DATE_ADD(P.DATA_INICIO, INTERVAL(1-DAYOFWEEK(P.DATA_INICIO)) DAY), '%d-%m-%Y') AS DIA,
                            SUM(P.VALOR_BRUTO) AS VALOR_GANHO_BRUTO,
                            SUM(P.VALOR_LIQUIDO) AS VALOR_GANHO_LIQUIDO   
                        FROM 
                            T_PROPOSTAS P
                            INNER JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                            INNER JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID
                        WHERE 
                            P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                            AND GU.FK_USUARIO = {id}
                            AND YEAR(P.DATA_INICIO) = {year}
                        GROUP BY 
                            YEAR(P.DATA_INICIO), WEEK(P.DATA_INICIO)
                        ORDER BY
                            YEAR(P.DATA_INICIO), WEEK(P.DATA_INICIO) ASC
                          """)



