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

def apply_filter_establishment_in_dataframe(df, establishment):
    if establishment is not None:
        df = df[df['ESTABELECIMENTO'] == establishment]

    return df

def apply_filter_in_dataframe(df, date, establishment):
    if len(date) > 1 and date[0] is not None and date[1] is not None:
        startDate = pd.Timestamp(date[0])
        endDate = pd.Timestamp(date[1])
        df = df.dropna(subset=['DATA_AVALIACAO'])
    
        df = df[df['DATA_AVALIACAO'] >= startDate]
        df = df[df['DATA_AVALIACAO'] <= endDate]

    if establishment is not None:
        df = df[df['ESTABELECIMENTO'] == establishment]

    df = df.rename(columns={'COMENTARIO': 'COMENTÁRIO', 'EMAIL_AVALIADOR':'E-MAIL DO AVALIADOR', 'DATA_PROPOSTA':'DATA DA PROPOSTA'
                                    ,'DATA_AVALICAO':'DATA DA AVALIAÇÃO'})

    return df

def apply_filter_in_finance_dataframe(df, date, establishment):
    if date is not None:
        if len(date) > 1 and date[0] is not None and date[1] is not None:
            startDate = pd.Timestamp(date[0])
            endDate = pd.Timestamp(date[1])
            df = df.dropna(subset=['DATA_INICIO'])
        
            df = df[df['DATA_INICIO'] >= startDate]
            df = df[df['DATA_FIM'] <= endDate]

    if establishment is not None:
        df = df[df['ESTABELECIMENTO'] == establishment]

    return df

def apply_filter_in_report_dataframe(df, date, establishment):
    if  date is not None:
        if len(date) > 1 and date[0] is not None and date[1] is not None:
            startDate = pd.Timestamp(date[0])
            endDate = pd.Timestamp(date[1])
            df = df.dropna(subset=['DATA'])
        
            df = df[pd.to_datetime(df['DATA']) >= startDate]
            df = df[pd.to_datetime(df['DATA']) <= endDate]

        df['DATA'] = pd.to_datetime(df['DATA']) 
        df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y')

    if establishment is not None:
        df = df[df['ESTABELECIMENTO'] == establishment]
  
    return df

def apply_filter_in_geral_dataframe(df, date=None, establishment=None):
    if date is not None:
        if len(date) > 1 and date[0] is not None and date[1] is not None:
            startDate = pd.Timestamp(date[0])
            endDate = pd.Timestamp(date[1])
            df = df.dropna(subset=['DATA_INICIO', 'DATA_FIM'])
        
            df = df[pd.to_datetime(df['DATA_INICIO']) >= startDate]
            df = df[pd.to_datetime(df['DATA_FIM']) <= endDate]

    if establishment is not None:
        df = df[df['ESTABELECIMENTO'] == establishment]

    df['DATA_INICIO'] = pd.to_datetime(df['DATA_INICIO'], dayfirst=True)
    df['DATA_FIM'] = pd.to_datetime(df['DATA_FIM'], dayfirst=True)

    df['DURACAO'] = (df['DATA_FIM'] - df['DATA_INICIO']).apply(
        lambda x: f"{x.components.hours}h {x.components.minutes}m {x.components.seconds}s"
    )
    
    df['DATA_INICIO'] = df['DATA_INICIO'].dt.strftime('%d/%m/%Y')
    df['DATA_FIM'] = df['DATA_FIM'].dt.strftime('%d/%m/%Y')

    return df

def get_report_artist(df):
    df['QUANTIDADE'] = df.groupby('ARTISTA')['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['ARTISTA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    df_grouped['RANKING'] = df_grouped['QUANTIDADE'].rank(method='first', ascending=False).astype(int)
    df_grouped = df_grouped.reset_index(drop=True)

    return df_grouped

def get_report_by_occurrence(df):
    df['QUANTIDADE'] = df.groupby(['TIPO'])['ARTISTA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['TIPO'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped

def get_report_artist_by_week(df):
    df['QUANTIDADE'] = df.groupby('SEMANA')['SEMANA'].transform('count')
    df_grouped = df.drop_duplicates(subset=['SEMANA'])
    df_grouped = df_grouped.sort_values(by='QUANTIDADE', ascending=False)
    return df_grouped

# QUERIES - colocar em outro arquivo

@st.cache_data # Extrato
def GET_PROPOSTAS_BY_ID(id, date, establishment):
    df =  getDfFromQuery(f"""
                    SELECT DISTINCT
                        P.ID AS ID_PROPOSTA,
                        CASE 
                            WHEN S.DESCRICAO IS NULL THEN "Cancelada"
                            ELSE S.DESCRICAO
                        END AS STATUS_PROPOSTA,
                        C.NAME AS ESTABELECIMENTO,
                        A.NOME AS ARTISTA,
                        DATA_INICIO AS DATA_INICIO,
                        DATA_FIM AS DATA_FIM,
                        DAYNAME(DATA_INICIO) AS DIA_DA_SEMANA,
                        P.VALOR_BRUTO,
                        SF.DESCRICAO AS STATUS_FINANCEIRO
                        
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
                        AND GU.FK_USUARIO = {id}
                        """)
    return apply_filter_in_geral_dataframe(df, date, establishment)

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
                            C.NAME AS ESTABELECIMENTO,
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

# Avaliações - Avaliações da casa
def GET_REVIEW_HOUSE_BY_ARTIST(id, establishment):
    df = getDfFromQuery(f"""SELECT
                        C.NAME AS ESTABELECIMENTO,
                        GC.GRUPO_CLIENTES AS GRUPO,
                        AC.NOTA,
                        AC.COMENTARIO AS 'COMENTÁRIO'

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

    return apply_filter_establishment_in_dataframe(df, establishment) 

# Avaliações - Avaliações de artista
def GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id):
    return getDfFromQuery(f"""
                        SELECT
                        A.NOME AS ARTISTA,
                        IFNULL(ROUND(AVG(AV.NOTA), 2),'0') AS 'MÉDIA DE NOTAS',
                        COUNT(DISTINCT AV.ID) AS 'QUANTIDADE DE AVALIAÇÕES',
                        COUNT(P.FK_CONTRATADO) AS 'NÚMERO DE SHOWS'

                        FROM T_PROPOSTAS P
                        LEFT JOIN T_AVALIACAO_ATRACOES AV ON (P.ID = AV.FK_PROPOSTA)
                        LEFT JOIN ADMIN_USERS AU ON (AU.ID = AV.LAST_USER)
                        INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                        INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                        LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                        LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                        WHERE
                        GU.STATUS = 1
                        AND GU.FK_USUARIO = 31582
                        AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                        GROUP BY
                        A.ID, A.NOME
                        ORDER BY 'MÉDIA DE NOTAS' DESC, 'QUANTIDADE DE AVALIAÇÕES' DESC;
    """)

# Avaliações - Avaliações da casa
def GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id, establishment):
    df = getDfFromQuery(f"""SELECT
                            C.NAME AS ESTABELECIMENTO,
                            IFNULL(ROUND(AVG(AC.NOTA), 2),'0') AS 'MÉDIA NOTAS',
                            COUNT(DISTINCT AC.ID) AS 'QUANTIDADE DE AVALIAÇÕES',
                            COUNT(P.FK_CONTRANTE) AS 'NÚMERO DE SHOWS'

                            FROM T_PROPOSTAS P
                            LEFT JOIN T_AVALIACAO_CASAS AC ON (P.ID = AC.FK_PROPOSTA)
                            LEFT JOIN ADMIN_USERS AU ON (AU.ID = AC.LAST_USER)
                            INNER JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE)
                            INNER JOIN T_ATRACOES A ON (A.ID = P.FK_CONTRATADO)
                            LEFT JOIN T_GRUPOS_DE_CLIENTES GC ON (GC.ID = C.FK_GRUPO)
                            LEFT JOIN T_GRUPO_USUARIO GU ON GU.FK_COMPANY = C.ID

                            WHERE 
                            GU.STATUS = 1
                            AND GU.FK_USUARIO = {id}
                            AND P.FK_STATUS_PROPOSTA IN (100,101,103,104)
                            GROUP BY
                            C.ID, C.NAME
                            ORDER BY
                            'MÉDIA NOTAS' DESC, 'QUANTIDADE DE AVALIAÇÕES' DESC;
    """)

    return apply_filter_establishment_in_dataframe(df, establishment)

# Avaliações - Rancking
def GET_ARTIST_RANKING(id):
    return  getDfFromQuery(f"""
                            SELECT
                            A.ID,
                            A.NOME AS ARTISTA,
                            ROUND(AVG(AV.NOTA), 2) AS MEDIA_NOTAS,
                            COUNT(DISTINCT AV.ID) AS QUANTIDADE_AVALIACOES,
                            COUNT(P.FK_CONTRATADO) AS NUM_SHOWS_ARTISTA,
                            EM.DESCRICAO AS ESTILO_PRINCIPAL,
                            A.EMAIL AS EMAIL,
                            A.CELULAR AS CELULAR
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
                            LEFT JOIN 
                            T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
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
                        C.NAME AS ESTABELECIMENTO,
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
                            DATE_ADD(DATE(P.DATA_INICIO), INTERVAL(2-DAYOFWEEK(P.DATA_INICIO)) DAY) AS NUMERO_SEMANA,
                            DATE_FORMAT(DATE_ADD(P.DATA_INICIO, INTERVAL(2-DAYOFWEEK(P.DATA_INICIO)) DAY), '%d-%m-%Y') AS DIA,
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

@st.cache_data # Desempenho Operacional
def GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id, date, establishment):
    df = getDfFromQuery(f"""
                            SELECT
                            A.NOME AS ARTISTA,
                            DATE(OA.DATA_OCORRENCIA) AS DATA,
                            DATE_ADD(DATE(OA.DATA_OCORRENCIA), INTERVAL(2-DAYOFWEEK(OA.DATA_OCORRENCIA)) DAY) AS SEMANA,
                            TIPO.TIPO AS TIPO,
                            EM.DESCRICAO AS ESTILO,
                            C.NAME AS ESTABELECIMENTO
                            FROM 
                            T_OCORRENCIAS_AUTOMATICAS OA
                            LEFT JOIN T_PROPOSTAS P ON P.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_PROPOSTAS'
                            LEFT JOIN T_NOTAS_FISCAIS NF ON NF.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND NF.TIPO = 'NF_UNICA'
                            LEFT JOIN T_NOTAS_FISCAIS NF2 ON NF2.ID = OA.TABLE_ID AND OA.TABLE_NAME = 'T_NOTAS_FISCAIS' AND (NF2.TIPO = 'NF_SHOW_ANTECIPADO' OR NF2.TIPO = 'NF_SHOW_SOZINHOS')
                            INNER JOIN T_ATRACOES A ON A.ID = OA.FK_ATRACAO
                            INNER JOIN T_TIPOS_OCORRENCIAS TIPO ON TIPO.ID = OA.FK_TIPO_OCORRENCIA
                            LEFT JOIN T_FECHAMENTOS F ON F.ID = NF.FK_FECHAMENTO
                            LEFT JOIN T_PROPOSTAS P2 ON P2.ID = NF2.FK_PROPOSTA
                            LEFT JOIN T_COMPANIES C ON (C.ID = P.FK_CONTRANTE OR C.ID = F.FK_CONTRATANTE OR C.ID = P2.FK_CONTRANTE)
                            LEFT JOIN T_ESTILOS_MUSICAIS EM ON A.FK_ESTILO_PRINCIPAL = EM.ID
                            WHERE 
                            C.ID IN (SELECT GU.FK_COMPANY FROM T_GRUPO_USUARIO GU WHERE GU.FK_USUARIO = {id} AND GU.STATUS = 1)
                            AND C.ID NOT IN (102,343,632,633)
                    """)

    return apply_filter_in_report_dataframe(df, date, establishment)

def GET_ARTIST_CHECKIN_CHECKOUT(id):
    return getDfFromQuery(f"""
                            SELECT
                            A.NOME AS ARTISTA,
                            COUNT(CASE WHEN S.DESCRICAO = 'Checkin Realizado' THEN 1 END) AS QUANTIDADE_CHECKIN,
                            COUNT(CASE WHEN S.DESCRICAO = 'Checkout Realizado' THEN 1 END) AS QUANTIDADE_CHECKOUT,
                            (COUNT(CASE WHEN S.DESCRICAO = 'Checkin Realizado' THEN 1 END) + COUNT(CASE WHEN S.DESCRICAO = 'Checkout Realizado' THEN 1 END)) AS TOTAL_CHECKIN_CHECKOUT
                            FROM T_PROPOSTAS P
                            LEFT JOIN T_COMPANIES C ON (P.FK_CONTRANTE = C.ID)
                            LEFT JOIN T_ATRACOES A ON (P.FK_CONTRATADO = A.ID)
                            LEFT JOIN T_PROPOSTA_STATUS S ON (P.FK_STATUS_PROPOSTA = S.ID)
                            INNER JOIN T_GRUPO_USUARIO GU ON GU.FK_USUARIO = P.FK_USUARIO 
                            AND GU.STATUS = 1
                            AND GU.FK_PERFIL IN (100,101)
                            WHERE P.TESTE = 0 
                            AND P.FK_CONTRANTE IS NOT NULL 
                            AND P.FK_CONTRATADO IS NOT NULL 
                            AND P.DATA_INICIO IS NOT NULL 
                            AND P.FK_USUARIO = {id}
                            GROUP BY 
                                A.NOME
                            ORDER BY 
                                TOTAL_CHECKIN_CHECKOUT DESC;
                          """)
