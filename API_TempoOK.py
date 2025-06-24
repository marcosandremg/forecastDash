# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:12:40 2023

@author: pepereira
"""

import requests
from requests.exceptions import HTTPError, JSONDecodeError
import json
import pandas as pd
from datetime import datetime,timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# proxies = {
#         "http": "http://10.55.0.65:8080",
#         "https": "http://10.55.0.65:8080",
# }

token = "92030947c559186b123117e59387a97a"
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# Variáveis para EÓLICA (v2):
# - FORECAST:
        # {'power': 'Geração [kWh]',
        #  'air_temperature': 'Temperatura [°C]',
        #  'power_ratio': 'Fator de capacidade [%]',
        #  'precipitation': 'Precipitação [mm]',
        #  'wind_speed': 'Velocidade do Vento [m/s]', 
        #  'wind_direction': 'Direção do vento [°]'}
# - OBSERVÁVEIS:
        # {'power': 'Geração [kWh]',
        #  'power_ratio': 'Fator de capacidade [%]',
        #  'wind_speed': 'Velocidade do Vento [m/s]',
        #  'wind_direction': 'Direção do vento [°]',
        #  'air_temperature': 'Temperatura [°C]',
        #  'precipitation': 'Precipitação [mm]'}

# Variáveis para SOLAR (v2):
# - FORECAST:
        # {'ghi': 'GHI [Wh/m²]',
        #  'dhi': 'DHI [Wh/m²]',
        #  'gpoa': 'GPOA [Wh/m²]',
        #  'power_nom': 'Geração DC [kWh]',
        #  'power': 'Geração [kWh]',
        #  'air_temperature': 'Temperatura [°C]',
        #  'dni': 'DNI [Wh/m²]', 
        #  'power_ratio': 'Fator de capacidade [%]',
        #  'precipitation': 'Precipitação [mm]',
        #  'relative_humidity': 'Umidade relativa [%]',
        #  'cloud_fraction': 'Cobertura de nuvens [%]',
        #  'temp_cell': 'Temperatura do Painel [°C]',
        #  'wind_speed': 'Velocidade do Vento [m/s]'}
# - OBSERVÁVEIS:
        # {'power': 'Geração [kWh]',
        #  'ghi': 'GHI [Wh/m²]',
        #  'power_ratio':'Fator de capacidade [%]',
        # 'wind_speed': 'Velocidade do Vento [m/s]',
        # 'air_temperature': 'Temperatura [°C]',
        # 'precipitation': 'Precipitação [mm]',
        # 'cloud_fraction': 'Cobertura de nuvens [%]',
        # 'relative_humidity': 'Umidade relativa [%]',
        # 'dhi': 'DHI [Wh/m²]'}


solar = [
  {'name': 'Pirapora 5','id': 7,'lat': -17.41391571533239,'lon': -44.8927668060647,'fase': 'PIR1'},
  {'name': 'Pirapora 6','id': 8,'lat': -17.415052744369707,'lon': -44.89861017136228,'fase': 'PIR1'},
  {'name': 'Pirapora 7','id': 9,'lat': -17.415257591338026,'lon': -44.90346246228107,'fase': 'PIR1'},
  {'name': 'Pirapora 9','id': 11,'lat': -17.412901280322725,'lon': -44.91571878578695,'fase': 'PIR1'},
  {'name': 'Pirapora 10','id': 2,'lat': -17.41390097568513,'lon': -44.9218728299955,'fase': 'PIR1'},
  {'name': 'Pirapora 2','id': 4,'lat': -17.41336351927182,'lon': -44.87748351150745,'fase': 'PIR2'},
  {'name': 'Pirapora 3','id': 5,'lat': -17.41552962565598,'lon': -44.88298176121369,'fase': 'PIR2'},
  {'name': 'Pirapora 4','id': 6,'lat': -17.415739693564923,'lon': -44.88756260272471,'fase': 'PIR2'},
  {'name': 'Pirapora 1','id': 1,'lat': -17.406276542457285,'lon': -44.88622578500049,'fase': 'PIR3'},
  {'name': 'Pirapora 8','id': 10,'lat': -17.412482009504227,'lon': -44.90884257943179,'fase': 'PIR3'},
  {'name': 'Pirapora 11','id': 3,'lat': -17.403474104448275,'lon': -44.91373579403826,'fase': 'PIR3'}
  ]
eolicas =  [
  {'name': 'SP06','id': 12,'lat': -10.424213064142668,'lon': -40.46361655175965,'fase': 'FLN2'},
  {'name': 'SP03','id': 13,'lat': -10.359941859252485,'lon': -40.45256195253639,'fase': 'FLN2'},
  {'name': 'SP05','id': 14,'lat': -10.299101712848284,'lon': -40.437232528419536,'fase': 'FLN2'},
  {'name': 'SP10','id': 15,'lat': -10.27526002323199,'lon': -40.43426983040704,'fase': 'FLN2'},
  {'name': 'SP11','id': 16,'lat': -10.25274784368419,'lon': -40.42790784243588,'fase': 'FLN2'},
  {'name': 'SP01','id': 17,'lat': -10.332480509734934,'lon': -40.43694472381592,'fase': 'FLN1'},
  {'name': 'SP13','id': 18,'lat': -10.35568050926975,'lon': -40.438791726953376,'fase': 'FLN1'},
  {'name': 'SP14','id': 19,'lat': -10.375928375087696,'lon': -40.449662319793234,'fase': 'FLN1'},
  {'name': 'SP04','id': 20,'lat': -10.393554423439161,'lon': -40.46099546218671,'fase': 'FLN1'},
  {'name': 'SDA I', 'id': 22, 'lat': -14.778523333333332, 'lon': -42.570750000000004, 'fase': 'SDA1'},
  {'name': 'SDA II', 'id': 23, 'lat': -14.799179, 'lon': -42.571557999999996, 'fase': 'SDA1'},
  {'name': 'SDA III', 'id': 24, 'lat': -14.83373, 'lon': -42.556934444444444, 'fase': 'SDA1'},
  {'name': 'SDA IV', 'id': 25, 'lat': -14.817663, 'lon': -42.583366999999996, 'fase': 'SDA1'},
  {'name': 'SDA V', 'id': 26, 'lat': -14.833058, 'lon': -42.588356, 'fase': 'SDA1'},
  {'name': 'SDA VI', 'id': 27, 'lat': -14.802158, 'lon': -42.598371, 'fase': 'SDA1'},
  {'name': 'Serra do Seridó II', 'id': 28, 'lat': -6.98025, 'lon': -36.76081, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó III', 'id': 29, 'lat': -6.97782, 'lon': -36.79, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó IV', 'id': 30, 'lat': -6.95413, 'lon': -36.77816, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó IX', 'id': 31, 'lat': -7.01218, 'lon': -36.81053, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó VI', 'id': 32, 'lat': -6.9891, 'lon': -36.79852, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó VII', 'id': 33, 'lat': -7.00256, 'lon': -36.77758, 'fase': 'SDS1'},
  {'name': 'Serra do Seridó X', 'id': 34, 'lat': -7.04068, 'lon': -36.74961, 'fase': 'SDS2'},
  {'name': 'Serra do Seridó XI', 'id': 35, 'lat': -7.01507, 'lon': -36.82414, 'fase': 'SDS2'},
  {'name': 'Serra do Seridó XII', 'id': 36, 'lat': -7.04114, 'lon': -36.8059, 'fase': 'SDS2'},
  {'name': 'Serra do Seridó XIV', 'id': 37, 'lat': -6.94012, 'lon': -36.79549, 'fase': 'SDS2'},
  {'name': 'Serra do Seridó XVI', 'id': 38, 'lat': -7.04213, 'lon': -36.77123, 'fase': 'SDS2'},
  {'name': 'Serra do Seridó XVII', 'id': 39, 'lat': -7.02068, 'lon': -36.75019, 'fase': 'SDS2'}
]

solar_complexes = [{'name': 'Pirapora','id': 1, 'lat': -17.41272, 'lon': -44.89888}]
eolicas_complexes = [{'name': 'Folha Larga Norte','id': 2,  'lat': -10.3378, 'lon': -40.44383},
                     {'name': 'Serra das Almas', 'id': 3, 'lat': -14.81088, 'lon': -42.57872},
                     {'name': 'Serra do Seridó - Fase 1', 'id': 4, 'lat': -6.98726, 'lon': -36.78935},
                     {'name': 'Serra do Seridó - Fase 2', 'id': 5, 'lat': -7.0184, 'lon': -36.78478}]

# [s['id'] for s in solar if 'PIR1/PIR2/PIR3' in s['fase']]
# [s['id'] for s in eolicas if 'VDB1/VDB2/VDB3/FLN1/FLN2/SDS1/SDS2' in s['fase']]



def get_plants_list(power_source: str):
    payload = {
        "api_token": token,
        "power_source": power_source, # "wind" # "solar"
        "division": "subparks" # "subparks" / "complexes"
    }

    try:
        response = requests.post(
            "https://api.tempook.com/geracao/v2/list/plants",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Verifica se a resposta foi bem-sucedida
        response.raise_for_status()
        
        # Tentativa de decodificar o JSON
        observations = response.json()
        print(observations)
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
        
    except Exception as err:
        print(f'Other error occurred: {err}')
#get_plants_list('solar')
def get_obs_variables_list(power_source: str):
    payload = {
        "api_token": token,
        "power_source": power_source # "wind" # "solar"
    }

    try:
        response = requests.post(
            "https://api.tempook.com/geracao/v2/list/obs_variables",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Verifica se a resposta foi bem-sucedida
        response.raise_for_status()
        
        # Tentativa de decodificar o JSON
        observations = response.json()
        print(observations)
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
        
    except Exception as err:
        print(f'Other error occurred: {err}')
#get_obs_variables_list('wind')
def get_forecast_variables_list(power_source: str):
    payload = {
        "api_token": token,
        "power_source": power_source # "wind" / "solar"
    }

    try:
        response = requests.post(
            "https://api.tempook.com/geracao/v2/list/variables",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Verifica se a resposta foi bem-sucedida
        response.raise_for_status()
        
        # Tentativa de decodificar o JSON
        observations = response.json()
        print(observations)
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
        
    except Exception as err:
        print(f'Other error occurred: {err}')
#get_forecast_variables_list('wind')
def get_v2_models_list(power_source: str):
    payload = {
        "api_token": token,
        "power_source": power_source # "wind" # "solar"
    }
    try:
        response = requests.post(
            "https://api.tempook.com/geracao/v2/list/models",
            headers=headers,
            data=json.dumps(payload)
        )
        
        # Verifica se a resposta foi bem-sucedida
        response.raise_for_status()
        
        # Tentativa de decodificar o JSON
        observations = response.json()
        print(observations)
        
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        
    except JSONDecodeError as json_err:
        print(f'JSON decoding error occurred: {json_err}')
        
    except Exception as err:
        print(f'Other error occurred: {err}')
    return
#get_v2_models_list('wind')

# =============================================================================
#                                 PREVISÃO
# =============================================================================

def get_forecast_values_range(power_source: str, prev_vars: list, integration: str, start_date: str, end_date: str, division: str, complex_name:str=None):
    idlist = []
    idlistname = []
    dfprev = pd.DataFrame()
    if power_source=='wind':
        if division=='complexes':
            idlist, idlistname =  map( list, zip(*[(s['id'], s['name']) for s in eolicas_complexes if 'name' in s and 'SDA' not in s['name']]) )
                                # map(list , zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s]))
        elif division=='subparks':
            idlist, idlistname =  map( list, zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s and 'SDA' not in s['name']]) )
                                # map(list , zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s]))
    elif power_source=='solar':
        prev_vars=['ghi','precipitation']
        if division=='complexes':
            idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar_complexes if 'name' in s]))
        elif division=='subparks':
            idlist = idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar if 'name' in s]))
    
    payload = {
        "api_token": token,
        "power_source": power_source, #"wind",
        "id": idlist, #[s['id'] for s in eolicas if 'fase' in s and complex_name in s['fase']], # [s['id'] for s in eolicas if 'fase' in s and 'SDS' in s['fase']]
        "variables": prev_vars,
        "start_date": start_date,
        "end_date": end_date,
        "integration": integration,                                            # 'daily' / 'hourly'
        "model_id": 20,
        "division": division,                                                     # [{'id': 20, 'name': 'TOK-IA', 'type': 'FORECAST'}
        #"analysis_date": pd.to_datetime('today').normalize().replace(day=1).strftime('%Y%m%d')
    }
    
    response = requests.post(
        "https://api.tempook.com/geracao/v2/forecast/multiforecast/range",
        headers=headers,
        data=json.dumps(payload),
    )
#    breakpoint()
    if response.status_code == 200:
        resp_json = response.json()
        
        dfprev = pd.DataFrame(index = pd.to_datetime(resp_json['data'][0]['times']),
                              columns = idlistname ) #[ next(item for item in eolicas if item["id"] == x['id'])['name'] for x in resp_json['data'] ]  )
        
        for idx,col in enumerate(dfprev.columns):
            for var in prev_vars:
                dfprev[col+'_'+var] = resp_json['data'][idx][var]
        
        dfprev = dfprev.dropna(axis=1, how='all')
        if integration=='hourly':
            dfprev.index = dfprev.index - timedelta(hours=3)
#        print(dfprev)
    else:
        print("\nFalha na conexão com API\n")
        print(response.text)
    
    return dfprev
# prev_vars = ["wind_speed", "precipitation"]
# first_day = datetime.now().replace(day=1).strftime('%Y%m%d') #.replace(day=1,hour=3,minute=0,second=0,microsecond=0) # hour=3 -> UTC
# upper_date = (datetime.now() + timedelta(days=10)).strftime('%Y%m%d')
# dfprev = get_forecast_values_range('wind', prev_vars, 'daily', first_day, upper_date, 'complexes',)
# # dfprev = get_forecast_values_range('wind', prev_vars, 'daily', first_day, upper_date, 'subparks')
# dfprev.applymap(lambda x: str(x).replace('.',',')).to_clipboard()

# perguntar sobre ultima rodagem do modelo para as previsões passadas: https://api.tempook.com/geracao/v2/forecast/multiforecast/range

# =============================================================================
#                                 OBSERVADO
# =============================================================================

def get_observed_values_range(power_source: str, obs_vars: list, integration:str, start_date: str, end_date: str, division: str, complex_name:str=None):
    #start_date = (pd.to_datetime('today').normalize() - timedelta(days=window)) + timedelta(hours=3)
    #end_date = pd.to_datetime('today').normalize()+timedelta(hours=3) #- timedelta(days=1) # ontem

    idlist = []
    idlistname = []
    dfobs = pd.DataFrame()
    if power_source=='wind':
        if division=='complexes':
            idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in eolicas_complexes if 'name' in s]))
        elif division=='subparks':
            idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s]))
    elif power_source=='solar':
        obs_vars=['ghi']
        if division=='complexes':
            idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar_complexes if 'name' in s]))
        elif division=='subparks':
            idlist = idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar if 'name' in s]))
    
    payload = {
        "api_token": token,
        "power_source": power_source,
        "id": idlist,
        "variables": obs_vars,
        "model_id": 101, # {'id': 100, 'name': 'TOKOBS', 'type': 'OBSERVED'} // {'id': 101, 'name': 'CUSTOMER', 'type': 'OBSERVED'} // {'id': 104, 'name': 'ONS', 'type': 'OBSERVED'}
        "start_date": start_date,
        "end_date": end_date
    }
    # CHUVA E TEMPERATURA -> model_id = 100
    # VELOCIDADE DO VENTO -> model_id = 101
    
    response = requests.post(
        "https://api.tempook.com/geracao/v2/observed/multiobserved/range",
        headers=headers,
        data=json.dumps(payload),
        #proxies=proxies
    )
    
    if response.status_code == 200:
        resp_json = response.json()
        
        index = pd.date_range(start=start_date, end=end_date, freq='1H')
        columns = idlistname
        
        dfobs = pd.DataFrame(index = index, columns=columns )
        
#        breakpoint()
        for idx, col in enumerate(dfobs.columns):
            for var in obs_vars:
                temp_df = pd.DataFrame([{'datetime': pd.to_datetime(datetime), col: value} for datetime, value in zip(resp_json['data'][idx]['times'], resp_json['data'][idx][var])])
                temp_df.set_index('datetime', inplace=True)
                dfobs = pd.merge(dfobs, temp_df, how='outer', left_index=True, right_index=True, suffixes=('', f'_{var}'))
        
        dfobs = dfobs.dropna(axis=1, how='all')

        if integration=='hourly':
            dfobs.index = dfobs.index - timedelta(hours=3)
        elif integration=='daily':
            if power_source=='wind':
                dfobs = dfobs.resample('1d').mean()
            elif power_source=='solar':
                dfobs = dfobs.resample('1d').sum()
            dfobs = dfobs.dropna(axis=0, how='all')
    else:
        print("Falha na conexão com API\n")
        print(response.text)
    
    return dfobs

# obs_vars = ["wind_speed"]
# first_day = datetime.now().replace(day=1).strftime('%Y%m%d')
# upper_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
# dfobs = get_observed_values_range('wind', obs_vars, 'daily', first_day, upper_date, 'complexes',)
# dfobs.applymap(lambda x: str(x).replace('.',',')).to_clipboard()



# =============================================================================
#                                MODELO NARMAX
# =============================================================================




# from sysidentpy.model_structure_selection import FROLS, MetaMSS
# from sysidentpy.basis_function._basis_function import Polynomial

# from sysidentpy.utils.plotting import plot_residues_correlation, plot_results
# from sysidentpy.residues.residues_correlation import compute_residues_autocorrelation, compute_cross_correlation


# from sklearn.preprocessing import StandardScaler
# scaler_in = StandardScaler()
# scaler_out = StandardScaler()
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, LSTM, Dropout
# from keras.regularizers import l2

# basis_function = Polynomial(degree=2)
# models_df = pd.DataFrame(columns=['Regressors', 'Parameters', 'ERR','SPE'])
# results_df = pd.DataFrame(index=columns,columns=['MAE','RMSE','MSE'])
# modelos = {}
# for spe in columns:
#     df_aux = pd.DataFrame()
#     df_aux = dfobs.loc[:, dfobs.columns[dfobs.columns.str.contains(spe+"_")]].copy()
#     df_aux = df_aux.dropna()
#     x_train, x_valid, y_train, y_valid = train_test_split(df_aux.loc[:,df_aux.columns.str.contains('_wind')],
#                                                           df_aux.loc[:,df_aux.columns.str.contains('_power')],
#                                                           test_size = 0.3,
#                                                           shuffle=False)
# #    pdb.set_trace()
#     model = MetaMSS(
#         norm=-2,
#         xlag=1,
#         ylag=1,
#         estimator="least_squares",
#         k_agents_percent=10,
#         estimate_parameter=True,
#         maxiter=30,
#         n_agents=10,
#         loss_func="metamss_loss",
#         basis_function=basis_function,
# #        random_state=42,
#         model_type="NARMAX"
#     )
    
#     # model.fit(X=x_train.to_numpy(), y=y_train.to_numpy())
#     model.fit(X=x_train.to_numpy(), y=y_train.to_numpy(), X_test=x_valid.to_numpy(), y_test=y_valid.to_numpy())
#     # model.fit(X=[x[0] for x in x_train.values],
#     #           y=[x[0] for x in y_train.values],
#     #           X_test=[x[0] for x in x_valid.values],
#     #           y_test=[x[0] for x in y_valid.values])
    
    
#     yhat = model.predict(X=x_valid.to_numpy(), y=y_valid.to_numpy())
#     plot_results(y=y_valid.to_numpy(), yhat=yhat, n=200, title=spe + ' - NARMAX(P) [MetaMSS(ylag=' + str(model.ylag[0]) + ',xlag=' + str(model.xlag[0]) + ')]')
    
#     # plt.figure(figsize=(10, 6))
#     # plt.plot(y_valid.index,y_valid.to_numpy(), label='Data', marker='.', markersize=10, linewidth=1.5)
#     # plt.plot(y_valid.index,yhat, label='Model', marker='*', markersize=8, linewidth=1.5)
#     # plt.legend()
#     # plt.title(spe + ' - Polinomial [MetaMSS(ylag=' + str(model.ylag[0]) + ',xlag=' + str(model.xlag[0]) + ')]',fontsize=18)
#     # plt.ylabel("y, $\hat{y}$", fontsize=14)
#     # plt.xticks(fontsize=12)
#     # plt.yticks(fontsize=12)
#     # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%b'))
#     # plt.show()
    
#     # Métricas:
#     mse = metrics.mean_squared_error(y_valid.to_numpy(), yhat)
#     print('MSE: ',mse)
#     rmse = metrics.mean_squared_error(y_valid.to_numpy(), yhat, squared=False)
#     print('RMSE: ',rmse)
#     mae = metrics.mean_absolute_error(y_valid.to_numpy(), yhat)
#     print('MAE: ',mae)
    
#     results_df.loc[spe,'MAE']=mae
#     results_df.loc[spe,'RMSE']=rmse
#     results_df.loc[spe,'MSE']=mse
    
    
#     r = pd.DataFrame(
#         results(
#             model.final_model, model.theta, model.err,
#             model.n_terms, err_precision=8, dtype='sci'
#             ),
#         columns=['Regressors', 'Parameters', 'ERR'])
#     r['SPE']=spe
#     print(r)
#     models_df = pd.concat([models_df,r])
#     modelos[spe] = model
#     #break
#     #pdb.set_trace()
#     #ee = compute_residues_autocorrelation(y_valid.to_numpy(), yhat)
#     #plot_residues_correlation(data=ee, title="Residues", ylabel="$e^2$")
#     #x1e = compute_cross_correlation(y_valid.to_numpy(), yhat, x_valid.to_numpy())
#     #plot_residues_correlation(data=x1e, title="Residues", ylabel="$x_1e$")
    


# print(models_df)
# print(results_df)







# =============================================================================
#                                MODELO LSTM
# =============================================================================

# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import LSTM, Dense, Dropout
# from keras.callbacks import EarlyStopping

# results_df = pd.DataFrame(index=columns,columns=['MAE','RMSE','MSE'])
# modelos = {}
# for spe in columns:
#     df_aux = pd.DataFrame()
#     df_aux = dfobs.loc[:, dfobs.columns[dfobs.columns.str.contains(spe+"_")]].copy()
#     df_aux = df_aux.dropna()
    
#     scaler = MinMaxScaler(feature_range=(0, 1))
#     data = scaler.fit_transform(df_aux.loc[:, df_aux.columns[df_aux.columns.str.contains(spe+"_wind")]].values.reshape(-1, 1))

#     # Split data into input (X) and output (y) variables
#     def create_dataset(data, time_steps):
#         X, y = [], []
#         for i in range(len(data) - time_steps):
#             X.append(data[i:(i + time_steps), 0])
#             y.append(data[i + time_steps, 0])
#         return np.array(X), np.array(y)
    
#     time_steps = 24  # Assuming hourly data, using 24 hours as input
#     X, y = create_dataset(data, time_steps)
    
#     # Reshape input data to be 3D [samples, time steps, features]
#     X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
#     # Split data into train and test sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
#     # Define the LSTM model
#     units=100
#     model = Sequential()
#     model.add(LSTM(units=units, return_sequences=True, input_shape=(X.shape[1], 1)))
#     model.add(Dropout(0.2))
#     model.add(LSTM(units=units, return_sequences=True))
#     model.add(Dropout(0.2))
#     model.add(LSTM(units=units))
#     model.add(Dense(units=1))
    
#     # Compile the model
#     model.compile(optimizer='adam', loss='mean_squared_error')
    
#     # Define early stopping callback
#     early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    
#     # Fit the model
#     model.fit(X_train, y_train, epochs=1000, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    
#     # Predict on the test data
#     test_predictions = model.predict(X_test)
    
#     # Inverse transform both test_predictions and y_test to get original scale
#     test_predictions = [x[0] for x in scaler.inverse_transform(test_predictions.reshape(-1,1))]
#     y_test_original = [x[0] for x in scaler.inverse_transform(y_test.reshape(-1,1))]
    
#     # Plot test data vs. predicted test data
#     plt.figure(figsize=(10, 6))
#     plt.plot(y_test_original, label='Test Data')
#     plt.plot(test_predictions, label='Predicted Test Data')
#     plt.xlabel('Time')
#     plt.ylabel('Wind Speed')
#     #plt.title('Wind Speed Forecasting: Test Data vs. Predicted Test Data')
#     plt.title(spe + ' - LSTM',fontsize=18)
#     plt.legend()
#     plt.show()
    
#     # Calculate metrics
#     mae = metrics.mean_absolute_error(y_test_original, test_predictions)
#     mse = metrics.mean_squared_error(y_test_original, test_predictions)
#     rmse = np.sqrt(mse)
    
#     print("Mean Absolute Error (MAE):", mae)
#     print("Mean Squared Error (MSE):", mse)
#     print("Root Mean Squared Error (RMSE):", rmse)
    
#     modelos[spe] = model
    
#     results_df.loc[spe,'MAE']=mae
#     results_df.loc[spe,'RMSE']=rmse
#     results_df.loc[spe,'MSE']=mse
    
# #    pdb.set_trace()
# print(results_df)




# =============================================================================
#                                 PREVISÃO
# =============================================================================

# from datetime import datetime
# for spe in columns:
#     df_aux = pd.DataFrame()
#     df_aux = dfprev.loc[:, dfprev.columns[dfprev.columns.str.contains(spe+"_")]].copy()
#     df_aux = df_aux.dropna()
    
#     #today = datetime(datetime.now().year, datetime.now().month, 25).date() if pd.Timestamp.now().day > 25 else pd.Timestamp.now().date().strftime('%Y-%m-%d')
#     today = pd.Timestamp.now().date().strftime('%Y-%m-%d')
    
#     df_aux[df_aux.index.month == pd.Timestamp.now().month].loc[today:,:]
    
#     prediction = modelos[spe].predict(X = df_aux[df_aux.index.month == pd.Timestamp.now().month].loc[today:,df_aux.columns.str.contains('_wind')].to_numpy(),
#                                       y = None)
    
    
    






















