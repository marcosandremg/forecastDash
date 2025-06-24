# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:14:15 2024

@author: pepereira
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime,timedelta

proxies = {
        "http": "http://10.55.0.65:8080",
        "https": "http://10.55.0.65:8080",
}
# .condarc file!!!

token = "e7695942-0f7b-4f75-aaf3-fdda09e3a087"
headers = {'accept': 'application/json','pim-auth': token}

# Anemometria Way2:
#anemom = pd.read_excel(r'C:\Users\pepereira\OneDrive - EDF Renouvelables\Área de Trabalho\Avaliações\Way2 - ID TMAs EDF.xlsx')

anemom_way2 =  [
    {'name': 'FLN1',
     'id': 5718},
    {'name': 'FLN2',
     'id': 5719},
    {'name': 'FLN',
     'id': 5722},
    {'name': 'SDS1',
     'id': 5698},
    {'name': 'SDS2',
     'id': 6166},
    {'name': 'SDS',
     'id': 6167},
]


eneat_RB_way2 = [
    {'name': 'Pirapora V',
     'id': 3879,
     'fase': 'PIR1'},
    {'name': 'Pirapora VI',
     'id': 3880,
     'fase': 'PIR1'},
    {'name': 'Pirapora VII',
     'id': 3881,
     'fase': 'PIR1'},
    {'name': 'Pirapora IX',
     'id': 3878,
     'fase': 'PIR1'},
    {'name': 'Pirapora X',
     'id': 3882,
     'fase': 'PIR1'},
    {'name': 'Pirapora II',
     'id': 3886,
     'fase': 'PIR2'},
    {'name': 'Pirapora III',
     'id': 3887,
     'fase': 'PIR2'},
    {'name': 'Pirapora IV',
     'id': 3888,
     'fase': 'PIR2'},
    {'name': 'Vazante I',
     'id': 3883,
     'fase': 'PIR3'},
    {'name': 'Vazante II',
     'id': 3884,
     'fase': 'PIR3'},
    {'name': 'Vazante III',
     'id': 3885,
     'fase': 'PIR3'},
    
    {'name': 'Serra do Serido X',
     'id': 6283,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XI',
     'id': 6284,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XII',
     'id': 6285,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XIV',
     'id': 6286,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XVI',
     'id': 6287,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XVII',
     'id': 6288,
     'fase': 'SDS2'},
    
    {'name': 'Serra do Serido II',
     'id': 6277,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido III',
     'id': 6278,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido IV',
     'id': 6280,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido IX',
     'id': 6279,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido VI',
     'id': 6281,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido VII',
     'id': 6282,
     'fase': 'SDS1'},
    
    {'name': 'SP01',
     'id': 6276,
     'fase': 'FLN1'},
    {'name': 'SP04',
     'id': 6289,
     'fase': 'FLN1'},
    {'name': 'SP13',
     'id': 6290,
     'fase': 'FLN1'},
    {'name': 'SP14',
     'id': 6291,
     'fase': 'FLN1'},
    
    {'name': 'SP03',
     'id': 6292,
     'fase': 'FLN2'},
    {'name': 'SP05',
     'id': 6293,
     'fase': 'FLN2'},
    {'name': 'SP06',
     'id': 6294,
     'fase': 'FLN2'},
    {'name': 'SP10',
     'id': 6295,
     'fase': 'FLN2'},
    {'name': 'SP11',
     'id': 6296,
     'fase': 'FLN2'},
]


eneat_way2 = [
    {'name': 'Pirapora V',
     'id': 3790,
     'fase': 'PIR1'},
    {'name': 'Pirapora VI',
     'id': 3791,
     'fase': 'PIR1'},
    {'name': 'Pirapora VII',
     'id': 3792,
     'fase': 'PIR1'},
    {'name': 'Pirapora IX',
     'id': 3793,
     'fase': 'PIR1'},
    {'name': 'Pirapora X',
     'id': 3794,
     'fase': 'PIR1'},
    {'name': 'SE Pirapora TR01',
     'id': 3796,
     'fase': 'PIR1'},
    {'name': 'Pirapora II',
     'id': 3801,
     'fase': 'PIR2'},
    {'name': 'Pirapora III',
     'id': 3802,
     'fase': 'PIR2'},
    {'name': 'Pirapora IV',
     'id': 3803,
     'fase': 'PIR2'},
    {'name': 'SE Pirapora TR03 (F2)',
     'id': 3804,
     'fase': 'PIR2'},
    {'name': 'Vazante I',
     'id': 3797,
     'fase': 'PIR3'},
    {'name': 'Vazante II',
     'id': 3798,
     'fase': 'PIR3'},
    {'name': 'Vazante III',
     'id': 3799,
     'fase': 'PIR3'},
    {'name': 'SE Pirapora TR02 (F3)',
     'id': 3800,
     'fase': 'PIR3'},
    
    {'name': 'Serra do Serido X',
     'id': 5984,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XI',
     'id': 5491,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XII',
     'id': 5492,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XIV',
     'id': 5493,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XVI',
     'id': 5985,
     'fase': 'SDS2'},
    {'name': 'Serra do Serido XVII',
     'id': 5986,
     'fase': 'SDS2'},
    {'name': 'TRF02_SDS',
     'id': 5483,
     'fase': 'SDS2'},
    
    {'name': 'Serra do Serido II',
     'id': 4865,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido III',
     'id': 4909,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido IV',
     'id': 4910,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido IX',
     'id': 4913,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido VI',
     'id': 4911,
     'fase': 'SDS1'},
    {'name': 'Serra do Serido VII',
     'id': 4912,
     'fase': 'SDS1'},
    {'name': 'TRF01_SDS',
     'id': 5513,
     'fase': 'SDS1'},
    
    {'name': 'SP01',
     'id': 3860,
     'fase': 'FLN1'},
    {'name': 'SP04',
     'id': 3862,
     'fase': 'FLN1'},
    {'name': 'SP13',
     'id': 3867,
     'fase': 'FLN1'},
    {'name': 'SP14',
     'id': 3868,
     'fase': 'FLN1'},
    {'name': 'TRF01_FLN',
     'id': 3775,
     'fase': 'FLN1'},
    
    {'name': 'SP03',
     'id': 3861,
     'fase': 'FLN2'},
    {'name': 'SP05',
     'id': 3863,
     'fase': 'FLN2'},
    {'name': 'SP06',
     'id': 3864,
     'fase': 'FLN2'},
    {'name': 'SP10',
     'id': 3865,
     'fase': 'FLN2'},
    {'name': 'SP11',
     'id': 3866,
     'fase': 'FLN2'},
    {'name': 'TRF02_FLN',
     'id': 3776,
     'fase': 'FLN2'},
]

id_to_name_mapping = {d['id']: d['name'] for d in eneat_way2}
id_to_name_mapping_RB = {d['id']: d['name'] for d in eneat_RB_way2}
id_to_name_mapping_AMA = {d['id']: d['name'] for d in anemom_way2}

ids_to_get = [s['id'] for s in eneat_RB_way2 if 'fase' in s and 'PIR' in s['fase'] and not pd.isna(s['id'])]


fase_to_names = {}
for item in eneat_RB_way2:
    fase = item['fase']
    name = item['name']
    if fase not in fase_to_names:
        fase_to_names[fase] = []
    fase_to_names[fase].append(name)


ids_to_get = [s['id'] for s in eneat_RB_way2 if 'fase' in s and 'SDS' in s['fase']]
ids_to_get = ','.join(str(id) for id in ids_to_get)


def get_Energy_custom(start_time:datetime, end_time:datetime, complex_name:str=None):
    if complex_name != None:
        ids_to_get = [s['id'] for s in eneat_RB_way2 if 'fase' in s and complex_name in s['fase']]
        ids_to_get = ','.join(str(id) for id in ids_to_get)
    else:
        ids_to_get = [s['id'] for s in eneat_RB_way2]
        ids_to_get = ','.join(str(id) for id in ids_to_get)
    
    start_time = start_time.strftime('%Y-%m-%dT03:05:00')#+'00%0A00%0A00'
    end_time = end_time.strftime('%Y-%m-%dT03:05:00')#+'00%0A00%0A00'
    
    response = requests.get(
         f"https://pim.way2.com.br:183/api/v3/dados-de-medicao/pontos?ids={ids_to_get}&grandezas=Eneat&intervalo=CincoMinutos&medicao-datainicio={start_time}&medicao-datafim={end_time}",
         headers=headers,
         # grandezas=Eneat (medidor SMF físico) - EneatLiquida (Perdas CCEE (apenas rateio de perdas) - energia líquida)
     )
     
    if response.status_code == 200:
         
         data = response.json()
         # data['dados'][0]['valores'][:10]
         
         # Initialize an empty DataFrame
         medicoes = pd.DataFrame()
         
         for medidor in range(len(data['dados'])):
             id_medidor = data['dados'][medidor]['pontoId']
             
             # Create the DataFrame for the current medidor
             df = pd.DataFrame(data['dados'][medidor]['valores'])[['data','valor']]
             
             # Convert 'data' to datetime
             df['data'] = pd.to_datetime(df['data'])
             df.set_index('data', inplace=True)
             
             # Rename the 'valor' column to the 'pontoId'
             df.rename(columns={'valor': id_medidor}, inplace=True)
             
             # Remove nan rows
             df.dropna(axis=0, inplace=True)
             
             # Concatenate the current DataFrame with the main DataFrame
             medicoes = pd.concat([medicoes, df], axis=1)
         
         medicoes.rename(columns=id_to_name_mapping_RB, inplace=True)
         medicoes.index = medicoes.index - timedelta(minutes=5)
         
         for fase, names in fase_to_names.items():
             # Verifica se todas as colunas (nomes) da fase existem no DataFrame
             colunas_existentes = [name for name in names if name in medicoes.columns]
             if colunas_existentes:
                 medicoes[fase] = medicoes[colunas_existentes].sum(axis=1)

         mapeamento_nomes = {
            'PIR1': 'SE Pirapora TR01',
            'PIR2': 'SE Pirapora TR03 (F2)',
            'PIR3': 'SE Pirapora TR02 (F3)',
            'SDS2': 'TRF02_SDS',
            'SDS1': 'TRF01_SDS',
            'FLN1': 'TRF01_FLN',
            'FLN2': 'TRF02_FLN'}
         medicoes.rename(columns=mapeamento_nomes, inplace=True)
         
    else:
        print("Falha na conexão com API\n")
        print(f"Error: {response.status_code}")
        print(response.text)
     
    return medicoes
# ini=datetime(2025, 2, 1)
# fim=datetime(2025, 2, 1)
# dfEneat=get_Energy_custom(ini,fim,)
# dfEneat.map(lambda x: str(x).replace('.',',')).to_clipboard()

def get_Energy_MTD(complex_name:str=None):
    if complex_name != None:
        ids_to_get = [s['id'] for s in eneat_RB_way2 if 'fase' in s and complex_name in s['fase']]
        ids_to_get = ','.join(str(id) for id in ids_to_get)
    else:
        ids_to_get = [s['id'] for s in eneat_RB_way2]
        ids_to_get = ','.join(str(id) for id in ids_to_get)
        
    response = requests.get(
        f"https://pim.way2.com.br:183/api/v3/dados-de-medicao/pontos?ids={ids_to_get}&grandezas=Eneat&contextodasdatas=ConsiderarMesCheio&intervalo=UmaHora&medicao-temporelativo=Ontem",
        headers=headers,
    )
    
    if response.status_code == 200:
        
        data = response.json()
        # data['dados'][0]['valores'][:10]
        
        # Initialize an empty DataFrame
        medicoes = pd.DataFrame()
        
        for medidor in range(len(data['dados'])):
            id_medidor = data['dados'][medidor]['pontoId']
            
            # Create the DataFrame for the current medidor
            df = pd.DataFrame(data['dados'][medidor]['valores'])[['data','valor']]
            
            # Convert 'data' to datetime
            df['data'] = pd.to_datetime(df['data'])
            df.set_index('data', inplace=True)
            
            # Rename the 'valor' column to the 'pontoId'
            df.rename(columns={'valor': id_medidor}, inplace=True)
            
            # Remove nan rows
            df.dropna(axis=0, inplace=True)
            
            # Remove last row
            df = df.iloc[:-1, :]
            
            # Concatenate the current DataFrame with the main DataFrame
            medicoes = pd.concat([medicoes, df], axis=1)
        
        medicoes.rename(columns=id_to_name_mapping, inplace=True)
        medicoes.index = medicoes.index - timedelta(hours=1)
        
    else:
        print("Falha na conexão com API\n")
        print(f"Error: {response.status_code}")
        print(response.text)
    
    return medicoes

# teste = get_Energy_MTD('SDS')
# teste.applymap(lambda x: str(x).replace('.',',')).to_clipboard()

# VelVenMedSup : Velocidade do Vento (Média Anemômetro Superior) AMA
# PrecMedPluv: Precipitação (Média - Pluviômetro)

def get_obs_wind_MTD(complex_name:str):
    ids_to_get = [s['id'] for s in anemom_way2 if complex_name in s['name']]
    ids_to_get = ','.join(str(id) for id in ids_to_get)
    #ids_to_get=4985
    response = requests.get(
        f"https://pim.way2.com.br:183/api/v3/dados-de-medicao/pontos?ids={ids_to_get}&grandezas=VelVenMedSup&contextodasdatas=ConsiderarMesCheio&intervalo=UmaHora&medicao-temporelativo=Ontem",
        headers=headers,
    )
    if response.status_code == 200:
        
        data = response.json()
        # data['dados'][0]['valores'][:10]
        
        # Initialize an empty DataFrame
        medicoes = pd.DataFrame()
        
        for medidor in range(len(data['dados'])):
            id_medidor = data['dados'][medidor]['pontoId']
            
            # Create the DataFrame for the current medidor
            df = pd.DataFrame(data['dados'][medidor]['valores'])[['data','valor']]
            
            # Convert 'data' to datetime
            df['data'] = pd.to_datetime(df['data'])
            df.set_index('data', inplace=True)
            
            # Rename the 'valor' column to the 'pontoId'
            df.rename(columns={'valor': id_medidor}, inplace=True)
            
            # Remove nan rows
            df.dropna(axis=0, inplace=True)
            
            # Remove last row
            df = df.iloc[:-1, :]
            
            # Concatenate the current DataFrame with the main DataFrame
            medicoes = pd.concat([medicoes, df], axis=1)
        
        medicoes.rename(columns=id_to_name_mapping_AMA, inplace=True)
        
    else:
        print("Falha na conexão com API\n")
        print(f"Error: {response.status_code}")
        print(response.text)
    
    return medicoes

# get_obs_wind_MTD('FLN')











