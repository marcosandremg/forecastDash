# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:43:49 2024

@author: pepereira
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
from numba import jit
import sys
#main_path=r'C:\Users\pepereira\OneDrive - EDF Renouvelables\Área de Trabalho\Avaliações'
#sys.path.append(main_path)
import os
base_path = os.path.dirname(__file__)
#from getPYRP_EPM_2df import *
#from getAirTemp_EPM_2df import *
#from getWindSpeed_EPM_2df import *
#from models import *
from API_TempoOK_vAttila import get_forecast_values_range, get_observed_values_range
from API_Way2 import get_Energy_MTD, get_Energy_custom
import plotly.graph_objs as go
import altair as alt
import math
import numpy as np
import calendar
import plotly.io as pio
pio.renderers.default = "browser"

st.set_page_config(layout="wide")

# hide_streamlit_style = """
#     <style>
#     [data-testid="stToolbarActionButtonIcon"] {
#         visibility: hidden;
#         height: 0;
#     }
#     [data-testid="stToolbarActionButtonIcon"]::before {
#         visibility: hidden;
#         display: none;
#     }
#     footer {visibility: hidden;}
#     #MainMenu {visibility: hidden;}
#     </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# hide_streamlit_style = """
#     <style>
#     [data-testid="stToolbar"] {
#         visibility: hidden;
#         height: 0;
#     }
#     footer {visibility: hidden;}
#     #MainMenu {visibility: hidden;}
#     </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#dark = '''
#<style>
#    .stApp {
#    background-color: #0E1117;
#    }
#</style>
#'''
#st.markdown(dark, unsafe_allow_html=True)


df_climatologia_hourly = pd.read_excel(os.path.join(base_path, "Climatologia_hourly.xlsx"),index_col=0) # pd.read_excel(main_path+r'/Climatologia_hourly.xlsx',index_col=0)

df_climatologia_hourly = df_climatologia_hourly.sort_index(ascending=True)
df_climatologia_hourly.index = df_climatologia_hourly.index - timedelta(hours=3)
agg_dict = {col: 'sum' if col == 'PIR' else 'mean' for col in df_climatologia_hourly.columns}
df_climatologia = df_climatologia_hourly.resample('1d').agg(agg_dict)
df_climatologia['PIR']=df_climatologia['PIR']/1000
df_climatologia_hourly['PIR']=df_climatologia_hourly['PIR']/1000
dfbu = pd.read_excel(os.path.join(base_path, "dReferences_2025.xlsx"), index_col=0, sheet_name='BU_for_BI') # pd.read_excel(main_path+r'/dReferences_2025.xlsx', index_col=0, sheet_name='BU_for_BI')
dfbu_BU = dfbu.pivot_table(index='Date', columns='Name SPE', values='BU_CDG') # antigo: values='P75 POI'
dfGA_FLN = pd.read_excel(os.path.join(base_path, "Metodologia BI Performance e Gestão de Energia 1 rev.xlsx"),sheet_name='FLN',nrows=55)
dfGA_SDS = pd.read_excel(os.path.join(base_path, "Metodologia BI Performance e Gestão de Energia 1 rev.xlsx"),sheet_name='SDS',nrows=115)
dfGA_PIR = pd.read_excel(os.path.join(base_path, "Metodologia BI Performance e Gestão de Energia 1 rev.xlsx"),sheet_name='PIR',nrows=12)

dfGA = pd.concat([dfGA_FLN, dfGA_SDS, dfGA_PIR], ignore_index=True)

piraporas = ["0"+str(i) if i < 10 else str(i) for i in range(1,12)]
dfarea = pd.read_excel(os.path.join(base_path, "Pirapora - Area efetiva por inversor.xlsx"))
for i in piraporas:
    dfarea[i] = dfarea[dfarea['Inversor'].str.contains(('P'+i +'-'))]['area modulo'].sum() #area modulo #area eff celula
dfarea = (dfarea[piraporas].iloc[0]).to_frame()
dfarea.columns = ['Area']
dfarea.columns = ['P'+col for col in dfarea.columns]
dfarea = dfarea.T

# Constantes do módulo / inversor
a = -3.47
b = -0.0594
dT = 3
n_stc = 16.56/100
inv_eff = 98.08/100

potNominal = [30889.95, 38308.65, 38308.65, 38308.65, 38310.45, 38310.45, 38310.45, 30851.1, 38310.45, 38310.45, 30860.85]
potNominalAC = [27.0,   31.0,     31.0,     31.0,     31.0,     31.0,     31.0,     27.0,    31.0,     31.0,     27.0]




mapping_dict = {
    "SP01": "São Januário I",
    "SP04": "São Januário IV",
    "SP13": "São Januário XIII",
    "SP14": "São Januário XIV",
    "SP03": "São Januário III",
    "SP05": "São Januário V",
    "SP06": "São Januário VI",
    "SP10": "São Januário X",
    "SP11": "São Januário XI",
    "SDS II": "Serra do Seridó II",
    "SDS III": "Serra do Seridó III",
    "SDS IV": "Serra do Seridó IV",
    "SDS VI": "Serra do Seridó VI",
    "SDS VII": "Serra do Seridó VII",
    "SDS IX": "Serra do Seridó IX",
    "SDS X": "Serra do Seridó X",
    "SDS XI": "Serra do Seridó XI",
    "SDS XII": "Serra do Seridó XII",
    "SDS XIV": "Serra do Seridó XIV",
    "SDS XVI": "Serra do Seridó XVI",
    "SDS XVII": "Serra do Seridó XVII",
    "V1": "Pirapora I",
    "P2": "Pirapora II",
    "P3": "Pirapora III",
    "P4": "Pirapora IV",
    "P5": "Pirapora V",
    "P6": "Pirapora VI",
    "P7": "Pirapora VII",
    "V2": "Pirapora VIII",
    "P9": "Pirapora IX",
    "P10": "Pirapora X",
    "P11": "Pirapora XI",
    "Pirapora 1": "Pirapora I",
    "Pirapora 2": "Pirapora II",
    "Pirapora 3": "Pirapora III",
    "Pirapora 4": "Pirapora IV",
    "Pirapora 5": "Pirapora V",
    "Pirapora 6": "Pirapora VI",
    "Pirapora 7": "Pirapora VII",
    "Pirapora 8": "Pirapora VIII",
    "Pirapora 9": "Pirapora IX",
    "Pirapora 10": "Pirapora X",
    "Pirapora 11": "Pirapora XI",
}
reversed_mapping = {v: k for k, v in mapping_dict.items()}

spe2complexo= {
    'São Januário I': 'FLN1', 'São Januário IV': 'FLN1', 'São Januário XIII': 'FLN1',
    'São Januário XIV': 'FLN1', 'São Januário III': 'FLN2', 'São Januário V': 'FLN2',
    'São Januário VI': 'FLN2', 'São Januário X': 'FLN2', 'São Januário XI': 'FLN2',
    'Serra do Seridó II': 'SDS1', 'Serra do Seridó III': 'SDS1', 'Serra do Seridó IV': 'SDS1',
    'Serra do Seridó VI': 'SDS1', 'Serra do Seridó VII': 'SDS1', 'Serra do Seridó IX': 'SDS1',
    'Serra do Seridó X': 'SDS2', 'Serra do Seridó XI': 'SDS2', 'Serra do Seridó XII': 'SDS2',
    'Serra do Seridó XIV': 'SDS2', 'Serra do Seridó XVI': 'SDS2', 'Serra do Seridó XVII': 'SDS2',
    'Pirapora I': 'PIR3', 'Pirapora II': 'PIR2', 'Pirapora III': 'PIR2', 'Pirapora IV': 'PIR2',
    'Pirapora V': 'PIR1', 'Pirapora VI': 'PIR1', 'Pirapora VII': 'PIR1', 'Pirapora VIII': 'PIR3',
    'Pirapora IX': 'PIR1', 'Pirapora X': 'PIR1', 'Pirapora XI': 'PIR3'
}

for fase in set(spe2complexo.values()):
    spes_fase = sorted([key for key, value in spe2complexo.items() if fase in value])
    dfbu_BU[fase+'_BU'] = dfbu_BU[spes_fase].sum(axis=1)
#    dfbu_p90[fase+'_P90'] = dfbu_p90[spes_fase].sum(axis=1)


#ativo = 'FLN'


@jit
def cp(v,fase):
    if 'FLN' in fase:
        if 3 <= v <= 8.5:
            power = 4349.2928604/(1 + math.pow(math.e ,(7.9112779 - v)/1.4317702))
        elif 8.5 < v <= 10.5:
            power = 4600/(1 + math.pow(math.e ,(8.212039221 - v)))
        elif 10.5 < v <=11.5:
            power = 4386.782208/(1 + math.pow(math.e ,(5.611457323 - v)/1.764969868))
        elif 11.5 < v <= 18:
            power = 4200
        elif v < 3:
            power = 0
        else:
            power = 4402.467298/(1 + math.pow(math.e ,(v - 23.30035999)/1.858648486))
        if power > 4200:
            power=4200
        return power
    elif fase == 'SDS1':
        if v<=3:
            power = 0
        elif 3 < v < 20.5:
            power = 5856.57/(1 + math.pow(math.e ,(8.2760306 - v)/1.37764))
        else:
            power = 12396.71/(1 + math.pow(math.e ,(v-17.87018)/11.78177))
        if power > 5500:
            power = 5500
        return power
    elif fase == 'SDS2':
        if v<=3:
            power = 0
        elif 3 < v < 20.5:
            power = 5856.57/(1 + math.pow(math.e ,(8.2760306 - v)/1.37764))
        else:
            power = 6100/(1 + math.pow(math.e ,(v-24.534234)/2.233808))
        if power > 5800:
            power = 5800
        return power


eolicas =  [
  {'name': 'SP06', 'id': 12, 'lat': -10.424213064142668, 'lon': -40.46361655175965, 'fase': 'FLN2','wtgs': 9},
  {'name': 'SP03', 'id': 13, 'lat': -10.359941859252485, 'lon': -40.45256195253639, 'fase': 'FLN2','wtgs': 8},
  {'name': 'SP05', 'id': 14, 'lat': -10.299101712848284, 'lon': -40.437232528419536, 'fase': 'FLN2','wtgs': 10},
  {'name': 'SP10', 'id': 15, 'lat': -10.27526002323199, 'lon': -40.43426983040704, 'fase': 'FLN2','wtgs': 10},
  {'name': 'SP11', 'id': 16, 'lat': -10.25274784368419, 'lon': -40.42790784243588, 'fase': 'FLN2','wtgs': 10},
  {'name': 'SP01', 'id': 17, 'lat': -10.332480509734934, 'lon': -40.43694472381592, 'fase': 'FLN1','wtgs': 8},
  {'name': 'SP13', 'id': 18, 'lat': -10.35568050926975, 'lon': -40.438791726953376, 'fase': 'FLN1','wtgs': 10},
  {'name': 'SP14','id': 19,'lat': -10.375928375087696,'lon': -40.449662319793234,'fase': 'FLN1','wtgs': 10},
  {'name': 'SP04', 'id': 20, 'lat': -10.393554423439161,'lon': -40.46099546218671,'fase': 'FLN1','wtgs': 7},
  {'name': 'SDA I', 'id': 22, 'lat': -14.778523333333332, 'lon': -42.570750000000004, 'fase': 'SDA1','wtgs': 0},
  {'name': 'SDA II', 'id': 23, 'lat': -14.799179, 'lon': -42.571557999999996, 'fase': 'SDA1','wtgs': 0},
  {'name': 'SDA III', 'id': 24, 'lat': -14.83373, 'lon': -42.556934444444444, 'fase': 'SDA1','wtgs': 0},
  {'name': 'SDA IV', 'id': 25, 'lat': -14.817663, 'lon': -42.583366999999996, 'fase': 'SDA1','wtgs': 0},
  {'name': 'SDA V', 'id': 26, 'lat': -14.833058, 'lon': -42.588356, 'fase': 'SDA1','wtgs': 0},
  {'name': 'SDA VI', 'id': 27, 'lat': -14.802158, 'lon': -42.598371, 'fase': 'SDA1','wtgs': 0},
  {'name': 'Serra do Seridó II', 'id': 28, 'lat': -6.98025, 'lon': -36.76081, 'fase': 'SDS1','wtgs': 3},
  {'name': 'Serra do Seridó III', 'id': 29, 'lat': -6.97782, 'lon': -36.79, 'fase': 'SDS1','wtgs': 8},
  {'name': 'Serra do Seridó IV', 'id': 30, 'lat': -6.95413, 'lon': -36.77816, 'fase': 'SDS1','wtgs': 8},
  {'name': 'Serra do Seridó IX', 'id': 31, 'lat': -7.01218, 'lon': -36.81053, 'fase': 'SDS1','wtgs': 9},
  {'name': 'Serra do Seridó VI', 'id': 32, 'lat': -6.9891, 'lon': -36.79852, 'fase': 'SDS1','wtgs': 8},
  {'name': 'Serra do Seridó VII', 'id': 33, 'lat': -7.00256, 'lon': -36.77758, 'fase': 'SDS1','wtgs': 8},
  {'name': 'Serra do Seridó X', 'id': 34, 'lat': -7.04068, 'lon': -36.74961, 'fase': 'SDS2','wtgs': 6},
  {'name': 'Serra do Seridó XI', 'id': 35, 'lat': -7.01507, 'lon': -36.82414, 'fase': 'SDS2','wtgs': 8},
  {'name': 'Serra do Seridó XII', 'id': 36, 'lat': -7.04114, 'lon': -36.8059, 'fase': 'SDS2','wtgs': 7},
  {'name': 'Serra do Seridó XIV', 'id': 37, 'lat': -6.94012, 'lon': -36.79549, 'fase': 'SDS2','wtgs': 6},
  {'name': 'Serra do Seridó XVI', 'id': 38, 'lat': -7.04213, 'lon': -36.77123, 'fase': 'SDS2','wtgs': 8},
  {'name': 'Serra do Seridó XVII', 'id': 39, 'lat': -7.02068, 'lon': -36.75019, 'fase': 'SDS2','wtgs': 6},
  {'name': 'Pirapora 5','id': 7,'lat': -17.41391571533239,'lon': -44.8927668060647,'fase': 'PIR1','wtgs': 0},
  {'name': 'Pirapora 6','id': 8,'lat': -17.415052744369707,'lon': -44.89861017136228,'fase': 'PIR1','wtgs': 0},
  {'name': 'Pirapora 7','id': 9,'lat': -17.415257591338026,'lon': -44.90346246228107,'fase': 'PIR1','wtgs': 0},
  {'name': 'Pirapora 9','id': 11,'lat': -17.412901280322725,'lon': -44.91571878578695,'fase': 'PIR1','wtgs': 0},
  {'name': 'Pirapora 10','id': 2,'lat': -17.41390097568513,'lon': -44.9218728299955,'fase': 'PIR1','wtgs': 0},
  {'name': 'Pirapora 2','id': 4,'lat': -17.41336351927182,'lon': -44.87748351150745,'fase': 'PIR2','wtgs': 0},
  {'name': 'Pirapora 3','id': 5,'lat': -17.41552962565598,'lon': -44.88298176121369,'fase': 'PIR2','wtgs': 0},
  {'name': 'Pirapora 4','id': 6,'lat': -17.415739693564923,'lon': -44.88756260272471,'fase': 'PIR2','wtgs': 0},
  {'name': 'Pirapora 1','id': 1,'lat': -17.406276542457285,'lon': -44.88622578500049,'fase': 'PIR3','wtgs': 0},
  {'name': 'Pirapora 8','id': 10,'lat': -17.412482009504227,'lon': -44.90884257943179,'fase': 'PIR3','wtgs': 0},
  {'name': 'Pirapora 11','id': 3,'lat': -17.403474104448275,'lon': -44.91373579403826,'fase': 'PIR3','wtgs': 0}
]

solar_complexes = [{'name': 'Pirapora','id': 1, 'lat': -17.41272, 'lon': -44.89888}]
eolicas_complexes = [{'name': 'Folha Larga Norte','id': 2,  'lat': -10.3378, 'lon': -40.44383, 'fase': 'FLN', 'wtgs': 82},
                     {'name': 'Serra das Almas', 'id': 3, 'lat': -14.81088, 'lon': -42.57872, 'fase': 'SDA', 'wtgs': 0},
                     {'name': 'Serra do Seridó - Fase 1', 'id': 4, 'lat': -6.98726, 'lon': -36.78935, 'fase': 'SDS1', 'wtgs': 44},
                     {'name': 'Serra do Seridó - Fase 2', 'id': 5, 'lat': -7.0184, 'lon': -36.78478, 'fase': 'SDS2', 'wtgs': 41}]


spes_em_fases = {}
for eolica in eolicas:
    fase = eolica['fase']
    if fase in spes_em_fases:
        spes_em_fases[fase] += 1
    else:
        spes_em_fases[fase] = 1
#print(spes_em_fases)


prev_vars = ['wind_speed', 'precipitation']
obs_vars = ['wind_speed']
first_day = datetime.now().replace(day=1)
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
today = datetime.now().strftime('%Y%m%d')
upper_date = (first_day.replace(day=calendar.monthrange(first_day.year, first_day.month)[1])).strftime('%Y%m%d')
first_day = first_day.strftime('%Y%m%d')


@st.cache_data
def get_info_ativo(ativo:str=None):
    # df_fcst = get_forecast_values_range('daily', first_day, upper_date, 'complexes') # get_forecast_values_range('wind', prev_vars, 'daily', first_day, upper_date, 'complexes',)
    # df_obs = get_observed_values_range('daily', first_day, yesterday, division='complexes') # get_observed_values_range('wind', obs_vars, 'daily', first_day, yesterday, 'complexes',)
    
    df_fcst_hourly = get_forecast_values_range('hourly', first_day, upper_date, 'complexes') #Retorna os valores previstos
    df_obs_hourly = get_observed_values_range('hourly', first_day, yesterday, division='complexes') #Retorna os valores Observados
    
    agg_dict = {col: 'mean' if 'wind_speed' in col else 'sum' for col in df_fcst_hourly.columns}
    df_fcst = df_fcst_hourly.resample('1d').agg(agg_dict)
    agg_dict = {col: 'mean' if 'wind_speed' in col else 'sum' for col in df_obs_hourly.columns}
    df_obs = df_obs_hourly.resample('1d').agg(agg_dict)
    
    
    # Busca dados EPM (Pirapora):
    #connection = models.login_EPM()
    #pyrp = getPYRP(first_day, today, connection)
    #temp = getAirTemp(first_day, today, connection)
    #ws = getWindSpeed(first_day, today, connection)
#    pyrp = df_fcst_hourly['Pirapora_gpoa'].to_frame()
    pyrp_replicado = pd.concat(
        [df_fcst_hourly['Pirapora_gpoa'].rename(f'P{i}') 
         for i in range(1, 12)],
        axis=1
    )
#    temp = df_fcst_hourly['Pirapora_air_temperature'].to_frame()
    temp_replicado = pd.concat(
        [df_fcst_hourly['Pirapora_air_temperature'].rename(f'P{i}') 
         for i in range(1, 12)],
        axis=1
    )
#    ws = df_fcst_hourly['Pirapora_wind_speed'].to_frame()
    ws_replicado = pd.concat(
        [df_fcst_hourly['Pirapora_wind_speed'].rename(f'P{i}') 
         for i in range(1, 12)],
        axis=1
    )
    potNominal_df = pd.DataFrame([[v/1000 for v in potNominal]] * pyrp_replicado.shape[0], columns=pyrp_replicado.columns, index=pyrp_replicado.index)
    potNominalAC_df = pd.DataFrame([[v for v in potNominalAC]] * pyrp_replicado.shape[0], columns=pyrp_replicado.columns, index=pyrp_replicado.index)
    # IEC-61724:
    dftmod = pyrp_replicado * (np.exp(a + (b * ws_replicado)) + dT/1000) + temp_replicado
    cftmod = 1 - (0.41/100) * (dftmod - 25)
    potdc_exp = (pyrp_replicado*1000 * cftmod*n_stc).mul(dfarea.values,axis=1)/1000000            
    potdc_exp = potdc_exp.where(potdc_exp <= potNominal_df, other=potNominal_df)                
    potac_exp = potdc_exp * 0.9312 # POI
    potac_exp = potac_exp.where(potac_exp <= potNominalAC, other=potNominalAC)
    potac_exp['PIR1'] = potac_exp[['P5','P6','P7','P9','P10']].sum(axis=1)
    potac_exp['PIR2'] = potac_exp[['P2','P3','P4']].sum(axis=1)
    potac_exp['PIR3'] = potac_exp[['P1','P8','P11']].sum(axis=1)
    potac_exp_daily = potac_exp.resample('1d').sum()
    
    # .applymap(lambda x: str(x).replace('.',',')).to_clipboard()
    
    
    nome_map = {
        'Folha Larga Norte': 'FLN',
        'Serra das Almas': 'SDA',
        'Serra do Seridó - Fase 1': 'SDS1',
        'Serra do Seridó - Fase 2': 'SDS2',
        'Pirapora': 'PIR'
    }
    df_fcst.columns = [ col.replace(orig, novo) for col in df_fcst.columns for orig, novo in nome_map.items() if orig in col]
    df_fcst_hourly.columns = [ col.replace(orig, novo) for col in df_fcst_hourly.columns for orig, novo in nome_map.items() if orig in col]
    df_obs.columns = [ col.replace(orig, novo) for col in df_obs.columns for orig, novo in nome_map.items() if orig in col]
    df_obs_hourly.columns = [ col.replace(orig, novo) for col in df_obs_hourly.columns for orig, novo in nome_map.items() if orig in col]
    
    
    df_fcst_subparks = get_forecast_values_range('daily', first_day, upper_date, 'subparks') # get_forecast_values_range('wind', ['wind_speed'], 'daily', first_day, upper_date, 'subparks')
    
    limit_on_month = df_obs_hourly.index[-1].strftime('%Y-%m-%d')
    
    df_eneatw2 = get_Energy_custom(df_obs.index[0],df_obs.index[-1] ) # get_Energy_MTD()
    
    
    
    # wind_speed_cols = df_fcst_subparks.filter(regex='_wind_speed$', axis=1)
    # wind_speed_cols = df_fcst_subparks.filter(regex='^(?!.*PIR).*_wind_speed$', axis=1)
    wind_speed_cols = [col for col in df_fcst_subparks.columns if ('_wind_speed' in col) and ('Pirapora' not in col)]
    wind_speed_cols = df_fcst_subparks[wind_speed_cols]

    df_exp_prod = pd.DataFrame()
    for column in wind_speed_cols.columns:
        column_xpower = column.replace('_wind_speed','_power')
        spe_name = column.split('_')[0]
        
        n_wtgs = [s['wtgs'] for s in eolicas if s['name'] == spe_name][0]
        fase = [s['fase'] for s in eolicas if s['name'] == spe_name][0]
#        breakpoint()
        df_exp_prod[column_xpower] = wind_speed_cols[column].apply(lambda v: cp(v, fase)) * n_wtgs * 24 * (1-1.5/100) * (1-3.5/100) / 1000

    df_exp_prod = df_exp_prod.loc[df_fcst.index[0]:(df_obs.index[0].normalize() + pd.offsets.MonthEnd(0)).replace(hour=23)]
    df_exp_prod_remain_month = df_exp_prod.resample('1d').sum()
    
    df_exp_prod_remain_month = pd.concat([df_exp_prod_remain_month,potac_exp_daily],axis=1)
    
    df_energy_mtd = (df_eneatw2.resample('1d').sum()/1000) # * 0.96 #.filter(regex=ativo) * 0.965    -------------> verificar se é ponto atualizado
    
    df_fcst['SDS_wind_speed'] = df_fcst[['SDS1_wind_speed', 'SDS2_wind_speed']].mean(axis=1)
    df_fcst['SDS_precipitation'] = df_fcst[['SDS1_precipitation', 'SDS2_precipitation']].mean(axis=1)
    df_fcst_hourly['SDS_wind_speed'] = df_fcst_hourly[['SDS1_wind_speed', 'SDS2_wind_speed']].mean(axis=1)
    df_fcst_hourly['SDS_precipitation'] = df_fcst_hourly[['SDS1_precipitation', 'SDS2_precipitation']].mean(axis=1)
    df_obs['SDS_wind_speed'] = df_obs[['SDS1_wind_speed', 'SDS2_wind_speed']].mean(axis=1)
    df_obs_hourly['SDS_wind_speed'] = df_obs_hourly[['SDS1_wind_speed', 'SDS2_wind_speed']].mean(axis=1)
    
    fases = set(spe2complexo.values())
    for fase in fases:        
        df_energy_mtd = pd.merge( df_energy_mtd , dfbu_BU[fase+'_BU'], left_index=True, right_index=True, how='left')
        #df_energy_mtd = pd.merge( df_energy_mtd , dfbu_p90[fase+'_P90'], left_index=True, right_index=True, how='left')
    df_energy_mtd.columns = df_energy_mtd.columns.str.replace('Serido', 'Seridó', regex=False)
    df_eneatw2.rename(columns={'Vazante I':'Pirapora I', 'Vazante II':'Pirapora VIII', 'Vazante III':'Pirapora XI'}, inplace=True)
    return df_fcst, df_obs, df_eneatw2, limit_on_month, df_exp_prod_remain_month, df_energy_mtd, df_fcst_hourly, df_obs_hourly
#df_fcst, df_obs, df_eneatw2, limit_on_month, df_exp_prod_remain_month, df_energy_mtd, df_fcst_hourly, df_obs_hourly = get_info_ativo()

# df_eneatw2['Serra do Serido X'].to_frame().applymap(lambda x: str(x).replace('.',',')).to_clipboard()
# df_eneatw2['Serra do Serido X'].to_frame().resample('1d').sum().applymap(lambda x: str(x).replace('.',',')).to_clipboard()

# # Criação de traços para o gráfico
@st.cache_data
def make_lines_weather(ativo, show_hourly):
    df_fcst_used = df_fcst_hourly if show_hourly else df_fcst
    df_obs_used = df_obs_hourly if show_hourly else df_obs
    df_climat_used = df_climatologia_hourly if show_hourly else df_climatologia
    max_y_rain_scale = 20 if show_hourly else 80

    if ativo == 'PIR':
        resource_suffix = '_ghi'
        resource_axis_title = 'GHI [Wh/m²]' if show_hourly else 'GHI [kWh/m²]'
        resource_axis_lim = 1.2 if show_hourly else 10
    else:
        resource_suffix = '_wind_speed'
        resource_axis_title = 'Velocidade do vento [m/s]'
        resource_axis_lim = 14
    if show_hourly:
        start_idx = df_obs_used.index[0].strftime('%Y-%m-%d %H:%M:%S')
        end_idx = df_fcst_used.index[-1].replace(hour=23).strftime('%Y-%m-%d %H:%M:%S')
    else:
        start_idx = df_obs_used.index[0].strftime('%Y-%m-%d')
        end_idx = df_fcst_used.index[-1].strftime('%Y-%m-%d')
    
    trace_fcst = go.Scatter(
        x=df_fcst_used.index, 
        y=df_fcst_used[ativo + resource_suffix], 
        mode='lines', 
        name='Previsão',
        line=dict(color='grey', dash='dash', width=4) # Linha tracejada azul claro
    )
#    breakpoint()
    
    trace_climat = go.Scatter(
        x=df_climat_used.loc[start_idx : end_idx].index, 
        y=df_climat_used.loc[start_idx : end_idx, ativo], 
        mode='lines', 
        name='Climatologia',
        line=dict(color='darkorange') # Linha tracejada azul claro
    )
    
    trace_precip = go.Bar(
        x=df_fcst_used.index, 
        y=df_fcst_used[ativo + '_precipitation'], 
        name='Chuva',
        marker=dict(color='blue'),
        yaxis='y2'
    )
    
    trace_obs = go.Scatter(
        x=df_obs_used.index, 
        y=df_obs_used[ativo + resource_suffix], 
        mode='lines', 
        name='Realizado',
        line=dict(color='white')
    )
    
    # Criação da figura que inclui os traços e o layout
    fig = go.Figure(data=[trace_obs, trace_fcst, trace_climat, trace_precip])
    
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True,
                thickness=0.1,  # Espessura do slider
               # bgcolor='lightgray'
            ),
            type='date'
        ),
        yaxis=dict(
            title=resource_axis_title,
            range=[0, resource_axis_lim]
        ),
        yaxis2=dict(
            title='Taxa de Precipitação [mm]',
            overlaying='y', # Especifica que o eixo y2 será sobreposto ao eixo y
            side='right', # Posiciona o eixo y2 à direita
            range=[0, max_y_rain_scale]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
#    fig.show()
    
    return fig
#make_lines_weather('SDS')

def make_gauge_energy(fase):
    this_month_str = pd.to_datetime('today').normalize().strftime('%Y-%m')
    
    if fase=='FLN1':
        trf='TRF01_FLN'
    elif fase=='FLN2':
        trf='TRF02_FLN'
    elif fase=='SDS1':
        trf='TRF01_SDS'
    elif fase=='SDS2':
        trf='TRF02_SDS'
    elif fase=='PIR1':
        trf='SE Pirapora TR01'
    elif fase=='PIR2':
        trf='SE Pirapora TR03 (F2)'
    elif fase=='PIR3':
        trf='SE Pirapora TR02 (F3)'
    
    arcWidth=20
    distanceBetweenBoth=5
    innerRadiusOutside=100
    outerRadiusOutside=innerRadiusOutside+arcWidth
    cornerRadius=50
    theta=3.66
    theta2=6.28+2.62
    
    outerRadiusInside=innerRadiusOutside-distanceBetweenBoth   # Raio externo do arco externo
    innerRadiusInside=outerRadiusInside-arcWidth  # Raio interno do arco externo
    
    
    geracao_mtd = df_energy_mtd[trf].sum() / 1000
    bu_mtd = df_energy_mtd[fase + '_BU'].sum() / 1000
    max_value = dfbu_BU.loc[this_month_str, fase + '_BU'].sum()/1000
    
    if geracao_mtd < bu_mtd:
        color_net = '#E74C3C' # vermelho
    else:
        color_net = '#27AE60' # verde
    color_bu = '#4c4c4c' # cinza
        
    data = pd.DataFrame({
        'category': ['Geração MTD', 'BU MTD'],
        'value': [geracao_mtd, bu_mtd]
    })
    # Criar gráfico com dois arcos (sem config)
    outer_arc = alt.Chart(data[data['category'] == 'Geração MTD']).mark_arc(
        innerRadius=innerRadiusOutside,  # Raio interno do arco externo
        outerRadius=outerRadiusOutside,   # Raio externo do arco externo
        cornerRadius=cornerRadius,
        theta=theta,  # Ângulo inicial rad -> 0rad -> 12h
        theta2=theta2,
    ).encode(
        theta=alt.Theta('value:Q', scale=alt.Scale(domain=[0, max_value], range=[theta, theta2])),
        color=alt.value(color_net)  # Cor fixa para Geração MTD
    )
    # Criar arco vazio de fundo (apenas borda)
    background_outer_arc = alt.Chart(pd.DataFrame({'dummy': [0]})).mark_arc(
        innerRadius=innerRadiusOutside,  # Raio interno do arco externo
        outerRadius=outerRadiusOutside,   # Raio externo do arco externo
        cornerRadius=cornerRadius,  # Arredondamento dos cantos
        fillOpacity=0,    # Sem preenchimento
        stroke='white',   # Cor da borda
        strokeWidth=1,     # Largura da borda
        strokeOpacity=0.15,
        theta=theta,  # Ângulo inicial rad -> 0rad -> 12h
        theta2=theta2,
    )
    
    inner_arc = alt.Chart(data[data['category'] == 'BU MTD']).mark_arc(
        innerRadius=innerRadiusInside,  # Raio interno do arco externo
        outerRadius=outerRadiusInside,   # Raio externo do arco externo
        cornerRadius=cornerRadius,
        theta=theta,  # Ângulo inicial rad -> 0rad -> 12h
        theta2=theta2,
    ).encode(
        theta=alt.Theta('value:Q', scale=alt.Scale(domain=[0, max_value], range=[3.66, 6.28+2.62])),
        color=alt.value(color_bu),
    )
    # Criar arco vazio de fundo (apenas borda)
    background_inner_arc = alt.Chart(pd.DataFrame({'dummy': [0]})).mark_arc(
        innerRadius=innerRadiusInside,  # Raio interno do arco externo
        outerRadius=outerRadiusInside,  # Mesmo raio externo do arco principal
        cornerRadius=cornerRadius,  # Arredondamento dos cantos
        fillOpacity=0,    # Sem preenchimento
        stroke='white',   # Cor da borda
        strokeWidth=1,     # Largura da borda
        strokeOpacity=0.1,
        theta=theta,  # Ângulo inicial rad -> 0rad -> 12h
        theta2=theta2,
    )
    
    # Adicionar texto no centro
    geracao_text = alt.Chart(pd.DataFrame({'value': [geracao_mtd]})).mark_text(
        text=f"{round(geracao_mtd,1)} GWh",  # Texto com o valor de geração
        fontSize=20,           # Tamanho da fonte
        fontWeight='bold',     # Peso da fonte
        color='white',           # Cor do texto,
        align='center',
    )
    deviation_text = alt.Chart(pd.DataFrame({'dummy': [0]})).mark_text(
        text=f"{round((geracao_mtd/bu_mtd-1)*100,1)}%",  # Texto com o valor de geração
        fontSize=15,           # Tamanho da fonte
        fontWeight='bold',     # Peso da fonte
        color=color_net,           # Cor do texto,
        align='center',           # Cor do texto
        #baseline="bottom",
        yOffset=30
    )
    title_text = alt.Chart(pd.DataFrame({'dummy': [0]})).mark_text(
        text=f"{fase}",  # Texto com o valor de geração
        fontSize=15,           # Tamanho da fonte
#        fontWeight='bold',     # Peso da fonte
        color='white',           # Cor do texto,
        align='center',
        yOffset=-30
    )
    
    # Combinar os arcos em camadas
    chart = alt.layer(background_outer_arc,outer_arc,geracao_text,deviation_text,background_inner_arc,inner_arc,title_text).properties(
        height=275,
        width=300,
#        title="Comparação: Geração MTD x BU MTD"
    )#.configure(background='#39414a')
    
    # Salvar como HTML e abrir no navegador
    # output_file = "chart.html"
    # chart.save(output_file)
    # webbrowser.open(output_file)
    
    return chart #fig

def make_bar_chart(spe, dfbarchart):
    # Calculando os valores
#    spe='Serra do Seridó XIV'
#    spe='Pirapora V'  #'São Januário III'
    spe_short = reversed_mapping.get(spe, spe)
    
#    breakpoint()
    mes_atual = df_obs.index[-1].month - 1
#    for spe in [k for (k,v) in spe2complexo.items() if v=='SDS1']:
#    breakpoint()
    if 'Pirapora' in spe:
#        breakpoint()
        recurso = dfbarchart.loc[ (dfbarchart.SPE==spe) & (dfbarchart.Tipo=='Recurso') , : ].iloc[:,mes_atual+3].values[0]
        requisito = dfbarchart.loc[ (dfbarchart.SPE==spe) & (dfbarchart.Tipo=='Requisito') , : ].iloc[:,mes_atual+3].values[0]
    else:
        recurso = dfbarchart.loc[ (dfbarchart.SPE==spe) & (dfbarchart.Tipo=='Recurso') , : ].iloc[:,mes_atual+3].values[0] / 1000
        requisito = dfbarchart.loc[ (dfbarchart.SPE==spe) & (dfbarchart.Tipo=='Requisito') , : ].iloc[:,mes_atual+3].values[0] / 1000
    
#    breakpoint()
    
    if spe_short in ['SDS X','SDS XI','SDS XII','SDS XIV','SDS XVI','SDS XVII']:
        #energ_proj = (df_exp_prod_remain_month.filter(like=spe+'_', axis=1).loc[limit_on_month:].iloc[1:] / (1-3.5/100)).sum()[0] *0.96 / 1000
        #recurso = recurso - energ_proj
        fig = go.Figure(
            data=[
                go.Bar(name='Geração', x=['Recurso'], y=[recurso], text=f"{recurso:.1f}", textfont=dict(size=24), marker=dict(color='blue'),showlegend=False),
                #go.Bar(name='Projeção', x=['Recurso'], y=[energ_proj], text=f"{energ_proj:.1f}", textfont=dict(size=24,color='white'), marker=dict(color='gray'), marker_pattern_shape="."),
                go.Bar(name='Requisito', x=['Requisito'], y=[requisito], text=f"{requisito:.1f}", textfont=dict(size=24), marker=dict(color='rgba(255, 134, 29, 1)'),showlegend=False),
            ],
            layout=dict(
                barcornerradius=10,
            ),
        )
    else:
        #energ_proj = 0
        # Criando o gráfico de barras
        fig = go.Figure(
            data=[
                go.Bar(name='Recurso', x=['Recurso'], y=[recurso], text=f"{recurso:.1f}", textfont=dict(size=24), marker=dict(color='blue'),showlegend=False),
                go.Bar(name='Requisito', x=['Requisito'], y=[requisito], text=f"{requisito:.1f}", textfont=dict(size=24), marker=dict(color='rgba(255, 134, 29, 1)'),showlegend=False),
            ],
            layout=dict(
                barcornerradius=10,
            ),
        )
    
    # marker=dict(color='rgba(0, 26, 112, 1)')
    # Atualizando o layout do gráfico
    fig.update_layout(barmode='stack',title={'text': spe, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}})
    fig.update_xaxes(title_text=None)
    fig.update_yaxes(range=[0, max(recurso, requisito) * 1.3]) # fig.update_yaxes(range=[0, max(recurso, energ_proj, requisito) * 1.3])
#    fig.show()
    
    return fig

def lastro():
    resultados = []
    resultados_MCP = []
    for fase in ['FLN1', 'FLN2', 'SDS1', 'SDS2', 'PIR1', 'PIR2', 'PIR3']:
        # Filtrar as SPEs da fase atual
        spes_na_fase = [k for k, v in spe2complexo.items() if v == fase]
        
        if fase == 'SDS2':
            prioritarios = ['Serra do Seridó XI', 'Serra do Seridó XIV']
            spes_na_fase = [item for item in spes_na_fase if item in prioritarios] + \
                               [item for item in spes_na_fase if item not in prioritarios]
        # elif 'PIR' in fase:
        #     spes_na_fase = [reversed_mapping.get(nome, nome) for nome in spes_na_fase]
        
        # % de rateio SDS XI e SDS XIV:
        global_percent_SDS_XI = 1
        global_percent_SDS_XIV = 1
        
        # Filtrar o DataFrame uma vez para as SPEs na fase
        df_fase = dfGA[dfGA.SPE.isin(spes_na_fase)]
        
        # if 'PIR' in fase:
        #     df_fase["SPE"] = df_fase["SPE"].replace(mapping_dict)
            
#        if 'PIR' in fase: breakpoint()
        # Calcular recurso e requisito para cada SPE
        for spe in spes_na_fase:
            
            df_spe = df_fase[df_fase.SPE == spe]
            
            if fase in ['FLN1','FLN2']:
                
                mes_atual = df_obs.index[-1].month - 1
                
                energia_observada = (df_energy_mtd.loc[:limit_on_month, reversed_mapping.get(spe, spe) ] ).sum()           
                energia_projetada = (df_exp_prod_remain_month[
                                         df_exp_prod_remain_month.columns[df_exp_prod_remain_month.columns.isin([reversed_mapping.get(spe, spe) + '_power'])]
                                       ].loc[limit_on_month:].iloc[1:]  ).sum().sum()
                
                if df_spe[df_spe.Item == 'CCEAR-D (MWh)'].iloc[:, 3:].size == 0:
                    cceard = np.zeros(12)
                else:
                    cceard = df_spe[df_spe.Item == 'CCEAR-D (MWh)'].iloc[:, 3:].values
                recurso = (
                    df_spe[df_spe.Item == 'GF Líquida (MWh)'].iloc[:, 3:].values +
                    df_spe[df_spe.Item == 'PPAs Compra (MWh)'].iloc[:, 3:].values
                )
                requisito = (
                    df_spe[df_spe.Item == 'PPAs (MWh)'].iloc[:, 3:].values +
                    cceard -
                    df_spe[df_spe.Item == 'PERDAS CCEAR (MWh)'].iloc[:, 3:].values
                )
                
                recurso_MCP = (
                    (energia_observada + energia_projetada) + df_spe[df_spe.Item == 'PPAs Compra (MWh)'].iloc[:, 3:].values[0] #[0][mes_atual]
                )
                if fase == 'FLN1':
                    requisito_MCP = (
                        (energia_observada + energia_projetada) * df_spe[df_spe.Item == 'Atendimento ACR (%)'].iloc[:, 3:].values + df_spe[df_spe.Item == 'PPAs (MWh)'].iloc[:, 3:].values
                    )
                elif fase == 'FLN2':
                    requisito_MCP = (
                        df_spe[df_spe.Item == 'GF Líquida (MWh)'].iloc[:, 3:].values
                    )

            elif fase == 'SDS1':          
                recurso = (
                    df_spe[df_spe.Item == 'GF Líquida (MWh)'].iloc[:, 3:].values +
                    df_spe[df_spe.Item == 'PPAs Compra (MWh)'].iloc[:, 3:].values
                )
                
                # requisito = PPA Cemig flex * percent_spe + demais PPAs ("PPAs (MWh)") - perdas CCEAR
                mes_atual = df_obs.index[-1].month - 1
                
                sds1_percent = {"Serra do Seridó II": 0.06, "Serra do Seridó III": 0.169, "Serra do Seridó IV": 0.176, "Serra do Seridó VI": 0.201, "Serra do Seridó VII": 0.189, "Serra do Seridó IX": 0.205}
                spe_list_F1 = [k for (k, v) in spe2complexo.items() if v == 'SDS1']
                energia_observada_SDSF1 = (df_energy_mtd.loc[:limit_on_month, 'TRF01_SDS'] ).sum()           
                energia_projetada_F1 = (df_exp_prod_remain_month[
                                         df_exp_prod_remain_month.columns[df_exp_prod_remain_month.columns.isin([spe + '_power' for spe in spe_list_F1])]
                                       ].loc[limit_on_month:].iloc[1:] ).sum().sum()
                
#                breakpoint()
                energia_observada = (df_energy_mtd.loc[:limit_on_month, spe ] ).sum()           
                energia_projetada = (df_exp_prod_remain_month[
                                         df_exp_prod_remain_month.columns[df_exp_prod_remain_month.columns.isin([spe + '_power'])]
                                       ].loc[limit_on_month:].iloc[1:]  ).sum().sum()
#                breakpoint()
                recurso_MCP = (
                    (energia_observada + energia_projetada) + df_spe[df_spe.Item == 'PPAs Compra (MWh)'].iloc[:, 3:].values[0] #[0][mes_atual]
                )
                requisito_MCP = (
                    df_spe[df_spe.Item == 'GF Líquida (MWh)'].iloc[:, 3:].values[0] #[0][mes_atual]
                )
                
                PPA_CEMIG_flex_F1 = 0
#                breakpoint()
                if (energia_observada_SDSF1 + energia_projetada_F1)*0.443259 >= df_spe[df_spe.Item == 'Sazonalização Cemig (MWh)'].iloc[:, 3:].values[0][mes_atual]*1.1 :
                    PPA_CEMIG_flex_F1 = df_spe[df_spe.Item == 'Sazonalização Cemig (MWh)'].iloc[:, 3:].values[0][mes_atual]*1.1
                elif (energia_observada_SDSF1 + energia_projetada_F1)*0.443259 <= df_spe[df_spe.Item == 'Sazonalização Cemig (MWh)'].iloc[:, 3:].values[0][mes_atual]*0.9 :
                    PPA_CEMIG_flex_F1 = df_spe[df_spe.Item == 'Sazonalização Cemig (MWh)'].iloc[:, 3:].values[0][mes_atual]*0.9
                else:
                    PPA_CEMIG_flex_F1 = (energia_observada_SDSF1 + energia_projetada_F1)*0.443259
                
                requisito = (
                    PPA_CEMIG_flex_F1 * sds1_percent[spe] + df_spe[df_spe.Item == 'PPAs (MWh)'].iloc[:, 3:].values[0] - df_spe[df_spe.Item == 'PERDAS CCEAR (MWh)'].iloc[:, 3:].values[0]
                )
                
                # requisito = (
                #     df_spe[df_spe.Item == 'PPA Cemig flex (MWh)'].iloc[:, 3:].values +
                #     df_spe[df_spe.Item == 'PPAs (MWh)'].iloc[:, 3:].values -
                #     df_spe[df_spe.Item == 'PERDAS CCEAR (MWh)'].iloc[:, 3:].values
                # )
            elif fase == 'SDS2':
                mes_atual = df_obs.index[-1].month - 1
                spe_list_F2 = [k for (k, v) in spe2complexo.items() if v == 'SDS2']
                
                    # projeções da energia remanescente:
                energia_projetada = (df_exp_prod_remain_month.filter(like=spe+'_', axis=1).loc[limit_on_month:].iloc[1:] ).sum()[0]
                energia_projetada_F2 = (df_exp_prod_remain_month[
                                         df_exp_prod_remain_month.columns[df_exp_prod_remain_month.columns.isin([spe + '_power' for spe in spe_list_F2])]
                                       ].loc[limit_on_month:].iloc[1:] ).sum().sum()
                sum_proj_spes_11_14 = (df_exp_prod_remain_month[
                                         df_exp_prod_remain_month.columns[df_exp_prod_remain_month.columns.isin(['Serra do Seridó XI_power','Serra do Seridó XIV_power'])]
                                       ].loc[limit_on_month:].iloc[1:] ).sum().sum()
                

                    # energia observada até o momento:
                energia_observada = (df_energy_mtd.loc[:limit_on_month, spe]).sum()
                energia_observada_SDSF2 = (df_energy_mtd.loc[:limit_on_month, 'TRF02_SDS'] ).sum()                
                sum_net_spes_11_14_mtd = (df_energy_mtd.loc[:limit_on_month, ['Serra do Seridó XI','Serra do Seridó XIV']]).sum().sum()
                
                
                PPA_ENGIE_flex_F2 = 0
                sazo_PPA_ENGIE_XI_XIV = df_fase[df_fase.Item=='Sazonalização Engie (MWh)'].iloc[1,mes_atual+3]
                if (sum_net_spes_11_14_mtd+sum_proj_spes_11_14)*0.68 >= sazo_PPA_ENGIE_XI_XIV * 1.1 :
                    PPA_ENGIE_flex_F2 = df_spe[df_spe.Item == 'Sazonalização Engie (MWh)'].iloc[:, 3:].values[0][mes_atual]*1.1
                elif (sum_net_spes_11_14_mtd+sum_proj_spes_11_14)*0.68 <= sazo_PPA_ENGIE_XI_XIV * 0.9 :
                    PPA_ENGIE_flex_F2 = df_spe[df_spe.Item == 'Sazonalização Engie (MWh)'].iloc[:, 3:].values[0][mes_atual]*0.9
                else:
                    PPA_ENGIE_flex_F2 = (sum_net_spes_11_14_mtd+sum_proj_spes_11_14)*0.68
                
                percent_rateio_engie_spe = 0
                if spe in ['Serra do Seridó XI','Serra do Seridó XIV']:
                    percent_rateio_engie_spe = (energia_observada + energia_projetada) / (sum_net_spes_11_14_mtd + sum_proj_spes_11_14)
                else:
                    percent_rateio_engie_spe  = 0
                
                percent_rateio = (energia_observada + energia_projetada - PPA_ENGIE_flex_F2*percent_rateio_engie_spe) / \
                                 (energia_observada_SDSF2 + energia_projetada_F2 - PPA_ENGIE_flex_F2)
                
                if spe == 'Serra do Seridó XI' and percent_rateio < 0:
                    percent_rateio = 0
                    global_percent_SDS_XI = percent_rateio
                elif spe == 'Serra do Seridó XIV' and percent_rateio < 0:
                    percent_rateio = 0
                    global_percent_SDS_XIV = percent_rateio
                
                if ((global_percent_SDS_XI==0) or (global_percent_SDS_XIV==0)) and spe not in ['Serra do Seridó XI','Serra do Seridó XIV']:
                    percent_rateio = (energia_observada + energia_projetada) / (energia_observada_SDSF2 - sum_net_spes_11_14_mtd + energia_projetada_F2 - sum_proj_spes_11_14)
                
#                breakpoint()
                if spe in ['Serra do Seridó XI','Serra do Seridó XIV']:
                    # requisito = %rateio * sazo_PPA + PPA_ENGIE_flex * %rateio_engie
                    requisito = (percent_rateio * df_spe[df_spe.Item == 'Sazonalização PPAs (MWh)'].iloc[:, 3:].values[0] + \
                                PPA_ENGIE_flex_F2*percent_rateio_engie_spe)
                    
                    requisito_MCP = requisito + (percent_rateio * df_spe[df_spe.Item == 'Sazonalização PPAs Venda Conv (MWh)'].iloc[:, 3:].values[0])
                else:
#                    breakpoint()
                    # requisito = %rateio * sazo_PPA
                    requisito = (percent_rateio * df_spe[df_spe.Item == 'Sazonalização PPAs (MWh)'].iloc[:, 3:].values[0])
                    
                    requisito_MCP = requisito + (percent_rateio * df_spe[df_spe.Item == 'Sazonalização PPAs Venda Conv (MWh)'].iloc[:, 3:].values[0])
                
#                breakpoint()
                    
                # recurso = (geração realizada + projeção até o final do mês) x 0,96 + PPAs Compra
#                breakpoint()
                recurso = (
                    #(energia_observada + energia_projetada)*0.96 + df_spe[df_spe.Item == 'Sazonalização PPAs Compra (MWh)'].iloc[mes_atual, 3:].values[0] * percent_rateio
                    (energia_observada + energia_projetada) + df_spe[df_spe.Item == 'Sazonalização PPAs Compra (MWh)'].iloc[:, 3:].values[0] * percent_rateio
                )
                
                recurso_MCP = (
                    recurso + (percent_rateio * df_spe[df_spe.Item == 'Sazonalização PPAs Compra Conv (MWh)'].iloc[:, 3:].values[0])
                )

            #if spe=='Serra do Seridó II': breakpoint()
            
            if 'PIR' in fase:
                consumo_observado = -df_eneatw2.loc[:limit_on_month,spe][df_eneatw2.loc[:limit_on_month,spe]<0].sum().sum() / 1000
                _,last_day = calendar.monthrange(datetime.now().year, datetime.now().month)
                
                last_day = calendar.monthrange(datetime.today().year, datetime.today().month)[1]
                remaining_days_in_month = max(0, last_day - datetime.today().day+1)
                
                consumo_projetado = -df_eneatw2.loc[:limit_on_month,spe][df_eneatw2.loc[:limit_on_month,spe]<0].resample('1d').sum().mean()/1000 * remaining_days_in_month
                
                requisito_MCP = (
                    consumo_observado + consumo_projetado
                )
                
                # recurso_MCP = (
                #     requisito_spe/sum(requisito_spe;1:11) * sum(PPA - Compra (MWh) ; 1:11) # df_spe[df_spe.Item == 'PPA - Compra (MWh)'].iloc[:, 3:].values[0]
                # )
                
            
            if 'FLN' in fase:
                resultados.append([fase, spe, "Recurso"] + recurso[0].tolist())
                resultados.append([fase, spe, "Requisito"] + requisito[0].tolist())
                resultados_MCP.append([fase, spe, "Recurso"] + recurso_MCP.tolist())
                resultados_MCP.append([fase, spe, "Requisito"] + requisito_MCP[0].tolist())
            elif 'SDS1' in fase:
                resultados.append([fase, spe, "Recurso"] + recurso[0].tolist())
                resultados.append([fase, spe, "Requisito"] + requisito.tolist())
                resultados_MCP.append([fase, spe, "Recurso"] + recurso_MCP.tolist())
                resultados_MCP.append([fase, spe, "Requisito"] + requisito_MCP.tolist())
            elif 'PIR' in fase:
                # resultados_MCP.append([fase, spe, "Recurso"] + recurso_MCP.tolist())
                array_meses = np.zeros(12)
                array_meses[mes_atual] = requisito_MCP
                resultados_MCP.append([fase, spe, "Requisito"] + list(array_meses))
            else:
                resultados.append([fase, spe, "Recurso"] + recurso.tolist())
                resultados.append([fase, spe, "Requisito"] + requisito.tolist())
                resultados_MCP.append([fase, spe, "Recurso"] + recurso_MCP.tolist())
                resultados_MCP.append([fase, spe, "Requisito"] + requisito_MCP.tolist())

#    breakpoint()
    # Criar o DataFrame final
    dflastro = pd.DataFrame(resultados, columns=["Fase", "SPE", "Tipo"] + dfGA.columns[3:].tolist())
    dfMCP = pd.DataFrame(resultados_MCP, columns=["Fase", "SPE", "Tipo"] + dfGA.columns[3:].tolist())
    
    spes_PIR = [pir for pir in dfMCP.SPE.unique() if 'Pirapora' in pir]
    requisito_PIR_total = dfMCP[dfMCP.SPE.isin(spes_PIR) & (dfMCP.Tipo=='Requisito')].iloc[:,mes_atual+3].sum()
    ppaConsumo_PIR_total = dfGA[dfGA.SPE.isin(spes_PIR) & (dfGA.Item=='PPA - Compra (MWh)')].iloc[:,mes_atual+3].sum()
    for spe_pir in spes_PIR:
#        breakpoint()
        recurso_MCP = (
            dfMCP[(dfMCP.SPE==spe_pir) & (dfMCP.Tipo=='Requisito')].iloc[:,mes_atual+3] / requisito_PIR_total * ppaConsumo_PIR_total
        )
        array_meses = np.zeros(12)
        array_meses[mes_atual] = recurso_MCP
        nova_linha = pd.DataFrame([[fase, spe_pir, 'Recurso'] + list(array_meses)], columns=dfMCP.columns)
        dfMCP = pd.concat([dfMCP, nova_linha], ignore_index=True)
    
    return dflastro, dfMCP

# valores_lastro, valores_MCP = lastro()
# valores_lastro.applymap(lambda x: str(x).replace('.',',')).to_clipboard()
# valores_MCP.applymap(lambda x: str(x).replace('.',',')).to_clipboard()

def acum_prod_X_BU_MTD_chart(df, ativo):
    fasesnet = []
    fasesbu = []
    if ativo_st=='SDS': fase1_net='TRF01_SDS';fase1_bu='SDS1_BU';fase2_net='TRF02_SDS';fase2_bu='SDS2_BU';\
                     fasesnet.append(fase1_net);fasesnet.append(fase2_net);fasesbu.append(fase1_bu);fasesbu.append(fase2_bu);
    elif ativo_st=='FLN': fase1_net='TRF01_FLN';fase1_bu='FLN1_BU';fase2_net='TRF02_FLN';fase2_bu='FLN2_BU';\
                     fasesnet.append(fase1_net);fasesnet.append(fase2_net);fasesbu.append(fase1_bu);fasesbu.append(fase2_bu);
    elif ativo_st=='PIR': fase1_net='SE Pirapora TR01';fase1_bu='PIR1_BU';fase2_net='SE Pirapora TR03 (F2)';fase2_bu='PIR2_BU';fase3_net='SE Pirapora TR02 (F3)';fase3_bu='PIR3_BU';\
                     fasesnet.append(fase1_net);fasesnet.append(fase2_net);fasesnet.append(fase3_net);fasesbu.append(fase1_bu);fasesbu.append(fase2_bu);fasesbu.append(fase3_bu);
    
    df['complexo_BU'] = df[fasesbu].sum(axis=1)
    df['complexo_NET'] = df[fasesnet].sum(axis=1)
    
    fasesnet.append('complexo_NET')
    fasesbu.append('complexo_BU')
    
    fig = go.Figure()
    for idx,fase in enumerate(fasesnet):
        if idx==0: flagvisible=True;
        else: flagvisible=False;
        bar_colors = ['blue' if date <= df_obs.index[-1] else 'gray' for date in df.index]
        bar_patterns = ['' if date <= df_obs.index[-1] else '/' for date in df.index]
        fig.add_trace(go.Bar(
            x=df.index,
            y=df[fase].cumsum()/1000,
            name="Geração",
            marker=dict(
                color=bar_colors,
                pattern=dict(shape=bar_patterns)  # Aplicação de padrões
            ),#'blue',
            visible=flagvisible
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[fasesbu[idx]].cumsum()/1000,
            mode='lines+markers',
            name="BU",
            line=dict(color='orange', width=2),
            visible=flagvisible
        ))

    # Determinar número de fases dinamicamente
    num_fases = len(fasesnet)
    
    # Criar botões dinamicamente
    buttons = []
    for i in range(num_fases):
        visible_list = [False] * (2 * num_fases)  # 2 traces por fase (bar + scatter)
        visible_list[2*i] = True                  # Ativa bar da fase
        visible_list[2*i + 1] = True              # Ativa linha da fase
        
        buttons.append(
            dict(
                label=f"Complexo" if i == num_fases - 1 else f"Fase {i+1}",
                method="update",
                args=[{"visible": visible_list}]
            )
        )

    fig.update_layout(
        # ... (configurações existentes)
        updatemenus=[
            dict(
                type="buttons",
                buttons=buttons,
                direction="left",
                showactive=True,
                x=0.9,
                y=1.2,
                bgcolor="gray",
                bordercolor="gray",
                font=dict(color="black"),
            )
        ]
    )
    return fig
# acum_prod_X_BU_MTD_chart(merged_df,ativo_st).show()

def energia_acum():
    energia_observada = df_energy_mtd.loc[:limit_on_month, :]#.cumsum()
    energia_projetada_spes = df_exp_prod_remain_month.loc[limit_on_month:].iloc[1:] 
    energia_projetada_spes.columns = energia_projetada_spes.columns.str.replace('_power', '', regex=False)
    energia_projetada_spes.rename(columns={f'P{i}': f'Pirapora {i}' for i in range(1, 12)},inplace=True)
       
    column_to_fase = {e['name']: e['fase'] for e in eolicas}

    # Filtrar apenas as colunas que estão no DataFrame e no mapeamento
    valid_columns = [col for col in energia_projetada_spes.columns if col in column_to_fase]
    
    # Reagrupar as colunas por fase
    fase_groups = {}
    for col in valid_columns:
        fase = column_to_fase[col]
        if fase not in fase_groups:
            fase_groups[fase] = []
        fase_groups[fase].append(col)
    
    # Criar um DataFrame com as somas agrupadas por fase
    aggregated_df = pd.DataFrame({
        fase: energia_projetada_spes[cols].sum(axis=1) for fase, cols in fase_groups.items()
    })
    aggregated_df.rename(columns={'FLN2': 'TRF02_FLN','FLN1': 'TRF01_FLN','SDS1': 'TRF01_SDS','SDS2': 'TRF02_SDS',
                                  'PIR1': 'SE Pirapora TR01','PIR2':'SE Pirapora TR03 (F2)', 'PIR3': 'SE Pirapora TR02 (F3)'}, inplace=True)

    common_columns = energia_observada.columns.intersection(aggregated_df.columns)
    result = pd.concat([energia_observada[common_columns], aggregated_df[common_columns]], axis=0)
    
    selected_columns = [col for col in dfbu_BU.columns if col.endswith('_BU')] # [ col for col in dfbu_BU.columns if col.endswith('_BU') and 'PIR' not in col ]
    
    merged_df = result.merge(dfbu_BU[selected_columns], left_index=True, right_index=True, how='left')

    return merged_df

# -----------------------------------------------------------------------------



#st.set_page_config(layout="wide")

opcao = st.sidebar.selectbox(
    "Selecione o ativo",
    ['Folha Larga Norte', 'Serra do Seridó', 'Pirapora'],
    index=0
)

ativo_mapping = {
    'Folha Larga Norte': 'FLN',
    'Serra do Seridó': 'SDS',
    'Pirapora': 'PIR'
}

ativo_st = ativo_mapping[opcao]

df_fcst, df_obs, df_eneatw2, limit_on_month, df_exp_prod_remain_month, df_energy_mtd, df_fcst_hourly, df_obs_hourly = get_info_ativo()
dflastro, dfmcp = lastro() #Problema na linha do lastro

# df_exp_prod_remain_month.applymap(lambda x: str(x).replace('.',',')).to_clipboard()

# if df_obs.index[-1] == datetime.now().day

# Título do aplicativo
st.title(f'{ativo_st} - Acompanhamento Mensal')
st.markdown(
    f"<h4 style='font-size: 18px;'>{df_obs.index[0].strftime('%d/%b')} - {df_obs.index[-1].strftime('%d/%b')}</h4>",
    unsafe_allow_html=True
)
st.text("")

fases_do_ativo = sorted([chave for chave in spes_em_fases if ativo_st in chave])

#spes_do_ativo = sorted([chave for chave in eolicas if ativo_st in 'fase'])
nomes_fase = sorted([eolica['name'] for eolica in eolicas if fases_do_ativo[0] in eolica['fase']])
spe_extenso = [mapping_dict.get(nome, nome) for nome in nomes_fase]

# Criação de colunas para os retângulos superiores
#cols = st.columns((4, 2, 2), gap='large')

#st.subheader('Previsão do recurso',divider='gray', anchor=False)

cols = st.columns((4, 3), gap='large',vertical_alignment='center',border=True)

with cols[0]:
    # st.subheader('Previsão do recurso')
    st.markdown('<h5 style="text-align: center; color: white;">Previsão do recurso</h5>', unsafe_allow_html=True)
    
    show_hourly = st.toggle('Mostrar dados horários', value=False)
    
    fig_weather = make_lines_weather(ativo_st, show_hourly)
    st.plotly_chart(fig_weather, use_container_width=True)

with cols[1]:
#    st.markdown("<h3 style='text-align: center;'>Energia MTD x BU (GWh)</h3>", unsafe_allow_html=True)
    st.markdown('<h5 style="text-align: center; color: white;">Energia x BU - MTD (GWh)</h5>', unsafe_allow_html=True)
    if len(fases_do_ativo) < 3:
        cols2 = st.columns(len(fases_do_ativo), gap='small',vertical_alignment='center')
        for idx,col in enumerate(cols2):
            with col:
                fig_altair = make_gauge_energy(fases_do_ativo[idx])
                st.altair_chart(fig_altair, use_container_width=True)
    else:
        cols2 = st.columns(2, gap='small',vertical_alignment='center')
        with cols2[0]: 
            fig_altair = make_gauge_energy(fases_do_ativo[0])
            st.altair_chart(fig_altair, use_container_width=True)
        with cols2[1]: 
            fig_altair = make_gauge_energy(fases_do_ativo[1])
            st.altair_chart(fig_altair, use_container_width=True)
        cols2_1 = st.columns(1, gap='small',vertical_alignment='center')
        with cols2_1[0]:
            fig_altair = make_gauge_energy(fases_do_ativo[2])
            st.altair_chart(fig_altair, use_container_width=True)


st.subheader('Geração x BU - realizado e projetado',divider='gray', anchor=False)

cols_acum = st.columns((4, 3), gap='large',border=True,vertical_alignment='center',)

merged_df = energia_acum()

with cols_acum[0]:
#    st.header('Previsão do recurso')
    fig_acum = acum_prod_X_BU_MTD_chart(merged_df,ativo_st)
    st.plotly_chart(fig_acum, use_container_width=True)

with cols_acum[1]:
#    columns = merged_df.columns # ['TRF02_SDS', 'TRF01_SDS', 'TRF01_FLN', 'TRF02_FLN', 'FLN1_BU', 'SDS2_BU', 'FLN2_BU', 'SDS1_BU']
    st.markdown('<h5 style="text-align: center; color: white;">Expectativa de fechamento do mês</h5>', unsafe_allow_html=True)
    columns_to_rename = ['TRF02_SDS', 'TRF01_SDS', 'TRF01_FLN', 'TRF02_FLN', 'SE Pirapora TR01', 'SE Pirapora TR03 (F2)', 'SE Pirapora TR02 (F3)']
    new_column_names = ['SDS2', 'SDS1', 'FLN1', 'FLN2', 'PIR1', 'PIR2', 'PIR3']
    merged_df_aux = merged_df.rename(columns=dict(zip(columns_to_rename, new_column_names)))
    
    cols_metric_acum = st.columns(len(fases_do_ativo))
    for i,fase in enumerate(fases_do_ativo):
        
        value = str(round(merged_df_aux[fase].sum()/1000,1))+" GWh"
        delta = str( round(( merged_df_aux[fase].sum() / merged_df_aux[fase+"_BU"].sum() - 1) * 100 , 1) ) + "%"
        cols_metric_acum[i].metric(label=fase, value=value, delta=delta, border=True)

if ativo_st != 'PIR':
    with st.expander('Lastro',icon=":material/monitoring:"):
        cols_f1 = st.columns(spes_em_fases[fases_do_ativo[0]])
        for i in range(spes_em_fases[fases_do_ativo[0]]):
            with cols_f1[i]:
                #st.write(f"Conteúdo da coluna {i+1}")
                st.plotly_chart(make_bar_chart(spe_extenso[i],dflastro), use_container_width=True)
        
        nomes_fase = sorted([eolica['name'] for eolica in eolicas if fases_do_ativo[1] in eolica['fase']])
        cols_f2 = st.columns(spes_em_fases[fases_do_ativo[1]])
        spe_extenso = [mapping_dict.get(nome, nome) for nome in nomes_fase]
        for i in range(spes_em_fases[fases_do_ativo[1]]):
            with cols_f2[i]:
                st.plotly_chart(make_bar_chart(spe_extenso[i],dflastro), use_container_width=True)



with st.expander('Exposição MCP',icon=":material/monitoring:"):
    for fase in fases_do_ativo:
        # Obtém os nomes das SPEs na fase atual
        nomes_fase = sorted([eolica['name'] for eolica in eolicas if fase in eolica['fase']])
        
        # Mapeia os nomes usando o dicionário de mapeamento
        spe_extenso = [mapping_dict.get(nome, nome) for nome in nomes_fase]
        if 'PIR' in fase:
            spe_extenso = [mapping_dict.get(nome,nome) for nome in spe_extenso]
    
        # Cria colunas para os gráficos
        cols = st.columns(spes_em_fases[fase])
    
        # Plota os gráficos
        for i, spe in enumerate(spe_extenso):
            with cols[i]:
#                if fase=='PIR1': breakpoint()
                st.plotly_chart(make_bar_chart(spe, dfmcp), use_container_width=True, key=f"mcp_chart_{fase}_{i}")
                
    
    # cols_f1 = st.columns(spes_em_fases[fases_do_ativo[0]])
    # nomes_fase = sorted([eolica['name'] for eolica in eolicas if fases_do_ativo[0] in eolica['fase']])
    # spe_extenso = [mapping_dict.get(nome, nome) for nome in nomes_fase]
    # for i in range(spes_em_fases[fases_do_ativo[0]]):
    #     with cols_f1[i]:
    #         st.plotly_chart(make_bar_chart(spe_extenso[i],dfmcp), use_container_width=True, key=f"mcp_chart_f1_{i}")
    # nomes_fase = sorted([eolica['name'] for eolica in eolicas if fases_do_ativo[1] in eolica['fase']])
    # cols_f2 = st.columns(spes_em_fases[fases_do_ativo[1]])
    # spe_extenso = [mapping_dict.get(nome, nome) for nome in nomes_fase]
    # for i in range(spes_em_fases[fases_do_ativo[1]]):
    #     with cols_f2[i]:
    #         st.plotly_chart(make_bar_chart(spe_extenso[i],dfmcp), use_container_width=True, key=f"mcp_chart_f2_{i}")



# df_energy_mtd.applymap(lambda x: str(x).replace('.',',')).to_clipboard()

#Marcos 
# df_energy_mtd[df_energy_mtd.columns[-14:]].applymap(lambda x: str(x).replace('.',',')).to_clipboard()
# df_exp_prod_remain_month.loc[sorted(set(df_exp_prod_remain_month.index).difference(set(df_energy_mtd.index)))].applymap(lambda x: str(x).replace('.',',')).to_clipboard()
#----------


# df_exp_prod_remain_month.applymap(lambda x: str(x).replace('.',',')).to_clipboard()
# dfmcp.applymap(lambda x: str(x).replace('.',',')).to_clipboard()







