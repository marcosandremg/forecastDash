import models
from tqdm.auto import tqdm
import json
import pandas as pd
import os
import epmwebapi as epm
import pytz
from datetime import datetime,timedelta
import warnings
warnings.filterwarnings('ignore')

def getAirTemp(startTime:str, endTime:str, connection: epm.EpmConnection):
    startTime = datetime.strptime(startTime, '%Y%m%d').replace(hour=3,minute=0,second=0,microsecond=0)
    endTime = datetime.strptime(endTime, '%Y%m%d').replace(hour=3,minute=0,second=0,microsecond=0)
    with open(models.getpathSuporte() + "P11 -Weather_EPM_Bia.txt") as f:
        pyrp = json.load(f)

    pyrhName = "_TEMPA"# + "-MET-"
    matchingPYRP = [s for s in pyrp if pyrhName in s['name']]
    body = [id['id'] for id in matchingPYRP]
    dfname = pd.DataFrame(matchingPYRP)

    try:
        data = connection.getDataObjects(body)
    except:
        print("\n\n¨¨¨¨¨¨¨¨¨¨¨¨¨¨\nA VPN está conectada?\n¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n")
    
    query_period = epm.QueryPeriod(startTime, endTime)
    process_interval = timedelta(hours=1)
    aggregate_details = epm.AggregateDetails(process_interval, epm.AggregateType.TimeAverage2)
    
    MeasureNameIDPot = []

    for responseJSON in data:  # data: { 'UFV_PIR_PIR02_MV1_PYRP-1-1_Measurements_IrdCmp' = <epmwebapi.basicvariable.BasicVariable object at 0x000001640D54E190>}
        name = (dfname[dfname['id'] == responseJSON]).values[0][0]
        type = "AmbientAirTemperature"

        if data[responseJSON] != None:
            dataAux = data[responseJSON].historyReadAggregate(aggregate_details, query_period)

            events = {}
            for event in dataAux:
                timestamp = event[1].strftime("%d/%m/%Y %H:%M:%S")
                events[timestamp] = str(event[0])

            MeasureNameIDPot.append({'name': name, 'type': type, 'id': responseJSON, 'measures': events})
    
    df = pd.DataFrame(MeasureNameIDPot)
    df_measures = pd.DataFrame(d['measures'] for d in MeasureNameIDPot).transpose()
    df_measures.columns = df['name'].values
    df_measures.index = pd.to_datetime(df_measures.index, dayfirst=True) - timedelta(hours=3)
    df_measures = df_measures.astype(float)
    
    df_measures[df_measures.values<0]=0
    df_measures = df_measures.apply(lambda row: row.fillna(row.mean()), axis=1)
    prefixos = sorted(set(col.split('_')[0] for col in df_measures.columns))

    # Criar um novo DataFrame para armazenar as médias
    combined_avg = pd.DataFrame()
    
    for prefixo in prefixos:
        # Encontrar todas as colunas que começam com o prefixo seguido de '-'
        cols = [col for col in df_measures.columns if prefixo in col]

        if len(cols) > 1:
            # Calcular a média se houver múltiplas colunas
            combined_avg[prefixo] = df_measures[cols].mean(axis=1)
        else:
            # Manter o valor único se houver apenas uma coluna
            combined_avg[prefixo] = df_measures[cols[0]]
    
    # Ordenar as colunas numericamente por prefixo
    combined_avg = combined_avg.reindex(
        sorted(combined_avg.columns, key=lambda x: int(x[1:])), 
        axis=1
    )
    
    return combined_avg