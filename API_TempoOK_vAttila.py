
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
        "power_source": power_source 
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
        "power_source": power_source 
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
#integration: str, start_date: str, end_date: str, division: str, complex_name:str=None,power_source: str=None,prev_vars: list=None

# =============================================================================
#                                 PREVISÃO
# =============================================================================

def get_forecast_values_range(integration: str, start_date: str, end_date: str, division: str, complex_name:str=None, power_source: str=None, prev_vars: list=None):
    """
    Retrieves forecast values for a specific power source within a given date range and granularity.

    Args:
        integration (str): The temporal resolution of the observations. Options are 'hourly' or 'daily'.
        start_date (str): The start date for the observation in 'YYYY-MM-DD' format.
        end_date (str): The end date for the observation in 'YYYY-MM-DD' format.
        division (str): Specifies the division level, either 'complexes' or 'subparks'.
        complex_name (str, optional): The name of the complex (for filtering), applicable only to 'wind'.
        power_source (str, optional): The power source to retrieve observed data for. Options are 'wind' or 'solar'.
        obs_vars (list, optional): List of variables to observe, e.g., 'wind_speed', 'precipitation', etc.

    Returns:
        pd.DataFrame: A DataFrame containing forecast values indexed by time. Columns include variable names
        and corresponding IDs, e.g., 'SP06_wind_speed', 'SP06_precipitation'.

    Raises:
        ValueError: If the API response status is not 200.
        KeyError: If the response JSON is not in the expected format.

    Examples:
        >>> df = get_forecast_values_range(
                power_source='wind',
                prev_vars=['wind_speed', 'precipitation'],
                integration='daily',
                start_date='2025-01-01',
                end_date='2025-01-15',
                division='complexes',
                complex_name='FLN1'
            )
        >>> print(df.head())

    Notes:
        - The function uses the `TempoOk` API to retrieve forecasts.
        - Solar (ghi) unit in kWh/m²  - windspeed m/s - precipitation mm
        - Make sure the `headers` and `token` variables are defined globally for authentication.
        - The `eolicas`, `solar`, `eolicas_complexes`, and `solar_complexes` dictionaries must
          be pre-defined to map IDs to names and phases.
        - For hourly forecasts, the function adjusts the time index by subtracting 3 hours.
        -if power_source and prev_vars are not defined the function will automatically return a df of all plants expected ressource (windspeed-precipitation/ghi-precipitation)
    """

    if power_source==None:

        df_wind = get_forecast_values_range(  integration, start_date, end_date, division, complex_name,'wind',["wind_speed", "precipitation"])
        df_solar =get_forecast_values_range(  integration, start_date, end_date, division, complex_name,'solar',['ghi','gpoa','air_temperature','wind_speed','precipitation'])
        dfprev = pd.concat([df_wind, df_solar], axis=1)
    else:
        if prev_vars is None:
            raise ValueError("prev_vars must be defined when power_source is specified.")
        idlist = []
        idlistname = []
        dfprev = pd.DataFrame()   
        if power_source=='wind':
            if division=='complexes':
                idlist, idlistname =  map( list, zip(*[(s['id'], s['name']) for s in eolicas_complexes if 'name' in s and 'SDA' not in s['name']]) )
            elif division=='subparks':
                idlist, idlistname =  map( list, zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s and 'SDA' not in s['name']]) )
        elif power_source=='solar':
            if division=='complexes':
                idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar_complexes if 'name' in s]))
            elif division=='subparks':
                idlist = idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar if 'name' in s]))
        
        payload = {
            "api_token": token,
            "power_source": power_source,
            "id": idlist,
            "variables": prev_vars,
            "start_date": start_date,
            "end_date": end_date,
            "integration": integration,                                            
            "model_id": 20,
            "division": division,                                                  # [{'id': 20, 'name': 'TOK-IA', 'type': 'FORECAST'}
            #"analysis_date": pd.to_datetime('today').normalize().replace(day=1).strftime('%Y%m%d')
        }
        
        response = requests.post(
            "https://api.tempook.com/geracao/v2/forecast/multiforecast/range",
            headers=headers,
            data=json.dumps(payload),verify=False
        )

        if response.status_code == 200:
            resp_json = response.json()
            
            dfprev = pd.DataFrame(index = pd.to_datetime(resp_json['data'][0]['times']),
                                  columns = idlistname )
            
            for idx,col in enumerate(dfprev.columns):
                for var in prev_vars:
                    dfprev[col+'_'+var] = resp_json['data'][idx][var]
                    if var in ['ghi', 'gpoa', 'dhi']:                               
                        dfprev[col+'_'+var] = dfprev[col+'_'+var] / 1000
            
            dfprev = dfprev.dropna(axis=1, how='all')
            if integration=='hourly':
                dfprev.index = dfprev.index - timedelta(hours=3)
                dfprev = dfprev.iloc[3:,:]
        else:
            print("\nFalha na conexão com API\n")
            print(response.text)
        
    return dfprev

# prev_vars = ["wind_speed", "precipitation"]          
# first_day = datetime.now().replace(day=1, hour=3).strftime('%Y%m%d') #.replace(day=1,hour=3,minute=0,second=0,microsecond=0) # hour=3 -> UTC
# upper_date = ((datetime.now().replace(hour=3)) + timedelta(days=30)).strftime('%Y%m%d')
# dfprev = get_forecast_values_range('daily', first_day, upper_date, 'complexes')
# dfprev = get_forecast_values_range('hourly', first_day, upper_date, 'complexes') # for GE dashboard
# dfprev.applymap(lambda x: str(x).replace('.',',')).to_clipboard()



# =============================================================================
#                                 OBSERVADO
# =============================================================================

def get_observed_values_range(integration: str, start_date: str, end_date: str, division: str, complex_name:str=None,power_source: str=None,obs_vars: list=None):
    """
    Retrieves observed values for a specific power source within a given date range and granularity.

    Args:
        integration (str): The temporal resolution of the observations. Options are 'hourly' or 'daily'.
        start_date (str): The start date for the observation in 'YYYY-MM-DD' format.
        end_date (str): The end date for the observation in 'YYYY-MM-DD' format.
        division (str): Specifies the division level, either 'complexes' or 'subparks'.
        complex_name (str, optional): The name of the complex (for filtering), applicable only to 'wind'.
        power_source (str, optional): The power source to retrieve observed data for. Options are 'wind' or 'solar'.
        obs_vars (list, optional): List of variables to observe, e.g., 'wind_speed', 'precipitation', etc.

    Returns:
        pd.DataFrame: A DataFrame containing observed values indexed by time. Columns include variable names
        and corresponding IDs, e.g., 'SP06_wind_speed', 'SP06_temperature'.

    Raises:
        ValueError: If the API response status is not 200.
        KeyError: If the response JSON is not in the expected format.

    Examples:
        >>> df = get_observed_values_range(
                integration='hourly',
                start_date='2025-01-01',
                end_date='2025-01-15',
                division='complexes',
                power_source='wind',
                obs_vars=['wind_speed', 'temperature']
            )
        >>> print(df.head())

    Notes:
        - The function uses the `tempook` API to retrieve observed values.
        - Solar (ghi) unit in kWh/m²  - windspeed m/s - precipitation mm
        - The `model_id` determines the type of observation:
            - `100`: Precipitation and temperature
            - `101`: Wind speed
        - For hourly data, the timestamps are adjusted by subtracting 3 hours from the index.
        - For daily data:
            - Mean values are used for wind observations.
            - Summed values are used for solar observations.
        - The `eolicas`, `solar`, `eolicas_complexes`, and `solar_complexes` dictionaries must
          be pre-defined to map IDs to names and phases.
        - If power_source is not defined the function will automatically return a df of all plants observed ressource (windspeed-precipitation/ghi-precipitation)
    """
    if power_source==None:
        df_solar =get_observed_values_range(  integration, start_date, end_date, division,complex_name=None,power_source='solar',obs_vars=['ghi'])
        #dfsolar['Pirapora_ghi']=dfsolar['Pirapora_ghi']/1000
        #integration with energy 
        #hourly consideration with UTC time and arg format
        df_wind = get_observed_values_range(  integration, start_date, end_date, division,complex_name=None,power_source='wind',obs_vars=["wind_speed"])
        
        dfobs = pd.concat([df_wind, df_solar], axis=1)
        
    else:
        if obs_vars is None:
            raise ValueError("obs_vars must be defined when power_source is specified.")
        else:
            idlist = []
            idlistname = []
            dfobs = pd.DataFrame()
            if power_source=='wind':
                model_id=101
                if division=='complexes':
                    idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in eolicas_complexes if 'name' in s]))
                elif division=='subparks':
                    idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in eolicas if 'name' in s]))
            elif power_source=='solar':
                model_id=100
                if division=='complexes':
                    idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar_complexes if 'name' in s]))
                elif division=='subparks':
                    idlist = idlist, idlistname = map(list , zip(*[(s['id'], s['name']) for s in solar if 'name' in s]))
            
            payload = {
                "api_token": token,
                "power_source": power_source,
                "id": idlist,
                "variables": obs_vars,
                "model_id": model_id, # {'id': 100, 'name': 'TOKOBS', 'type': 'OBSERVED'} // {'id': 101, 'name': 'CUSTOMER', 'type': 'OBSERVED'} // {'id': 104, 'name': 'ONS', 'type': 'OBSERVED'}
                "start_date": start_date,
                "end_date": end_date
            }
            # CHUVA E TEMPERATURA -> model_id = 100
            # VELOCIDADE DO VENTO -> model_id = 101
            
            response = requests.post(
                "https://api.tempook.com/geracao/v2/observed/multiobserved/range",
                headers=headers,
                data=json.dumps(payload),verify=False
                #proxies=proxies
            )
            
            if response.status_code == 200:
                resp_json = response.json()
                index = pd.date_range(start=start_date, end=end_date, freq='1H')
                columns = idlistname
                
                dfobs = pd.DataFrame(index = pd.to_datetime(resp_json['data'][0]['times']),
                                      columns = idlistname )
                    
        #        breakpoint()
                for idx, col in enumerate(dfobs.columns):
                    for var in obs_vars:
                        if var in resp_json['data'][idx]:
                            temp_df = pd.DataFrame([{'datetime': pd.to_datetime(datetime), col: value} for datetime, value in zip(resp_json['data'][idx]['times'], resp_json['data'][idx][var])])
                            temp_df.set_index('datetime', inplace=True)
                            if var in ['ghi', 'gpoa', 'dhi']:                               
                                temp_df = temp_df / 1000
                            dfobs = pd.merge(dfobs, temp_df, how='outer', left_index=True, right_index=True, suffixes=('', f'_{var}'))
                        else:
                            print(f"Warning: Variable '{var}' not found in the response for column '{col}'")


                dfobs = dfobs.dropna(axis=1, how='all')

                if integration=='hourly':
                    dfobs.index = dfobs.index - timedelta(hours=3)
                    dfobs = dfobs.iloc[3:,:]
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
# dfobs = get_observed_values_range( 'daily', first_day, upper_date, division='complexes')
# dfobs = get_observed_values_range( 'hourly', first_day, upper_date, division='complexes')
# dfobs.applymap(lambda x: str(x).replace('.',',')).to_clipboard()
