from data.dbconnect import *
from utils.functions import *

def get_username(id):
    return GET_USER_NAME(id)
    
def get_geral_information_and_finances(id):
    return GET_PROPOSTAS_BY_ID(id)

# Retorna os dados de cada dataframe num dicionário
def get_dashbords_data(id, inputDate=None, inputEstablishment=None):
    # pega dados e já aplica filtro se tiver
    generalFinances = apply_filter_in_dataframe(GET_WEEKLY_FINANCES(id), inputDate, inputEstablishment)
    financeDash = apply_filter_in_dataframe(GET_GERAL_INFORMATION_AND_FINANCES(id), inputDate, inputEstablishment)
    artistRanking = apply_filter_in_dataframe( GET_ARTIST_RANKING(id), inputDate, inputEstablishment)
    reviewArtistByHouse = apply_filter_in_dataframe( GET_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
    averageReviewArtistByHouse = apply_filter_in_dataframe( GET_AVAREGE_REVIEW_ARTIST_BY_HOUSE(id), inputDate, inputEstablishment)
    reviewHouseByArtist = apply_filter_in_dataframe( GET_REVIEW_HOUSE_BY_ARTIST(id), None, inputEstablishment)
    averageReviewHouseByArtist = apply_filter_in_dataframe( GET_AVAREGE_REVIEW_HOUSE_BY_ARTIST(id), None, inputEstablishment)
    allOperationalPerformaceByOccurrenceAndDate = apply_filter_in_dataframe( GET_ALL_REPORT_ARTIST_BY_OCCURRENCE_AND_DATE(id), inputDate, inputEstablishment)
    operationalPerformace = apply_filter_in_dataframe( get_report_artist(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
    ByOccurrence = apply_filter_in_dataframe( get_report_by_occurrence(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
    ByWeek = apply_filter_in_dataframe( get_report_artist_by_week(allOperationalPerformaceByOccurrenceAndDate.copy()), inputDate, inputEstablishment)
    downloadShowStatement = GET_PROPOSTAS_BY_ID(id)
    showStatement = apply_filter_in_dataframe( downloadShowStatement, inputDate, inputEstablishment) 
    weeklyFinances = apply_filter_in_dataframe( GET_WEEKLY_FINANCES(id), inputDate, inputEstablishment)

    financeDash['DIA_DA_SEMANA'] = financeDash['DIA_DA_SEMANA'].apply(translate_day)
    showStatement['DIA_DA_SEMANA'] = showStatement['DIA_DA_SEMANA'].apply(translate_day)

    # Dicionário com dados de entrada
    data = {
        'generalFinances': generalFinances,
        'financeDash': financeDash,
        'averageReviewHouseByArtist': averageReviewHouseByArtist,
        'ByOccurrence': ByOccurrence,
        'downloadShowStatement': downloadShowStatement,
        'showStatement': showStatement,
        'weeklyFinances': weeklyFinances,
        'artistRanking': artistRanking,
        'reviewArtistByHouse': reviewArtistByHouse,
        'averageReviewArtistByHouse': averageReviewArtistByHouse,
        'reviewHouseByArtist': reviewHouseByArtist,
        'operationalPerformace': operationalPerformace,
        'ByWeek': ByWeek,
        'allOperationalPerformaceByOccurrenceAndDate': allOperationalPerformaceByOccurrenceAndDate,
        'id': id
    }

    return data