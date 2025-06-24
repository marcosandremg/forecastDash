'''
Funções gerais para todos os Gets
'''
import epmwebapi as epm
import datetime
import requests
import pandas as pd
from WorkingPath import WorkingPath
import os

proxies = {
            "http": "http://10.55.0.65:8080",
            "https": "http://10.55.0.65:8080"}

def getpathSuporte():
    '''
    Path da pasta da rede de arquivos suporte
    '''
    a=WorkingPath()
    return a.path_diario_pirapora_Suporte()

def getpathSave():
    '''
    # Path pasta na rede onde salvar os dowloads
    '''
    return "C:\\Users\\pepereira\\OneDrive - EDF Renouvelables\\Área de Trabalho\\Avaliações\\PIR - getData_EPM_v2\\Data\\" 

def getPiraporas():
    ''' Piraporas com o 0 ["P01", "P02",...'''

    #return ["P01"]
    return ["P01","P02", "P03","P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11"]

def login():
        login = '{\n"username" : "Supervision Center",\n"password" : "eDF@UFVP17",\n"lang" : "en"\n}'
        responseEDFid = requests.post('https://portal.solarpark-online.com/ifms/login',
                                  data=login,
                                  verify=False,
                                  proxies=proxies)

        cookies = responseEDFid.cookies
        id = responseEDFid.json()['id']
        
        return cookies, id 

def makeRequest(body, cookies, startDate, endDate):
        
        url = "https://portal.solarpark-online.com/ifms/sources/values?start_date=" + startDate + "&end_date=" + endDate
        data = requests.post(url, json=body, cookies=cookies, proxies=proxies)
        return data

def findElem (array, elem, key, value):
    for dictionary in array:
        if (dictionary[key] == elem):
            return dictionary[value]

def setDia(date):
    '''Função pra auxílio de nome da data'''
    mes = date.month
    if mes < 10:
        mes = "0" +str(mes)
    else:
        mes = str(mes)
    
    dia = date.day
    if dia < 10:
        dia = "0" +str(dia)
    else:
        dia = str(dia)
    
    return dia+mes 

def setNameDia(endTime):
    '''Função pra auxílio de nome da data'''
    diaFinal = int(endTime[6:8])
    if diaFinal < 10:
        diaFinal = "0" +str(diaFinal)
    else:
        diaFinal = str(diaFinal)
    
    return diaFinal

def clearFolder(folderName):
    '''Esvazia a pasta de destino'''
    dir = getpathSave() + folderName
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
def login_EPM():

    user = 'marcos.galdino'
    password = 'Pira@2024'

    try:
        connection = epm.EpmConnection('http://10.95.128.5:44333', 'http://10.95.128.5:44332', user, password)
        print(f'Conexão com 10.95.128.6 criada com sucesso para o usuário {user}')
    except:
        print(f'Falha no estabelecimento da conexão com 10.95.128.6 para o usuário {user}')
    
    return connection

def editdf(json):
    df = pd.DataFrame(json)
    dfMeasures = pd.DataFrame(d['measures'] for d in json)  # As linhas são os equips de MESMO ÍNDICE em df !!!
    dfMeasures = dfMeasures.transpose() # As linhas são dateStamps e colunas são equipamentos
    if not(df.empty):   
        dfMeasures.columns = df['name'] + "-" + df['type'].values
        dfMeasures.index = pd.to_datetime(dfMeasures.index.str.replace('T',""),dayfirst=True)
        dfMeasures.index = pd.to_datetime(dfMeasures.index) - datetime.timedelta(hours=3)

    
    return dfMeasures

def verifyPYRP(df):
    piranomsComProblema = []
    #Verifica se piranômetro > 1000 e, caso negativo, cria a média:
    for piranometro in [col for col in df.columns if 'PYRP' in col]:
        try:
            if len(df[df[piranometro] == '1000'])/df.shape[0] >= 0.35:  # se tiver mais de 35% de medições em 1000
                del df[piranometro]
                print(piranometro + ' - MEDIÇÃO CONGELADA EM 1000 W/m²')
                piranomsComProblema.append(piranometro + ' - MEDIÇÃO CONGELADA EM 1000 W/m²')  # variável que armazena piranômetros com problemas
            #else:
            #    print(piranometro + ' - OK')
            #    piranomsComProblema.append(piranometro + ' - OK')
        except:
            print(f'{piranometro} - Piranometro Sem nenhuma medição')
    return 0

def getFase():
    return {'P01':'3','P02':'2','P03':'2','P04':'2','P05':'1','P06':'1',
            'P07':'1','P08':'3','P09':'1','P10':'1','P11':'3'}

def convert_to_preferred_format(sec):
    hour = sec // 3600
    sec = sec%3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec) 

def getFalha():
    return ['24V terminal supply short circuit','AC-Circuit breaker tripped','Amplifier board contactor','Auto Reset','Auxiliary supply fault','Battery synchronisation fault',
            'Cooling water over-temperature ','Cooling water pressure fault / Fluid cooling system fault / Cooling water pump fault','Current clipping timeout',
            'D current direction fault(reverse ldc)','DC-link overvoltage','DC-link short circuit','DC-Link under-voltage','ECAT operation fault / PIB watchdog fault',
            'Environmental conditions','External fan','External faults','External oscillations','Feedback AC circuit breaker','Feedback DC circuit breaker',
            'Feedback discharging contactor','Feedback PV short circuit breaker ','Fieldbus connection faut','Fieldbus warning','Float controller fault','FPGA version wrong',
            'Fuse discharge resistor','Heat sink over-temperature','Heat sink temperature measuremente','Heat sink under-temperature','IGBT feedback fault',
            'IGBT Vce desaturation fault / PIB amplifier connection','Insulation fault','Insulation warning','Inverter producing reactive power',
            'Inverter without communication with scada','Line filter','Line inductor cubicle over-temperature','Line inductor fan','Line under voltage warning','Line voltage fault',
            'Line voltage measurement','MV transformer fault','NCU','No fail','Over voltage protection warning','PIB internal power supply','PIB measurement connector',
            'PIB terminal supply','Pole grounding','Power electronics cubicle fan','Power electronics cubicle over-temperature','Precharging failed','Short circuit/Short-Circuit-To-Earth',
            'Switching cycle AC-Breaker (daily)','Transformer Fault','Unidentified fault','UPS fault','Water heating/cooling fault']

def mes():
    return {'01':'Janeiro','02':'Fevereiro','03':'Março','04':'Abril','05':'Maio',
            '06':'Junho','07':'Julho','08':'Agosto','09':'Setembro','10':'Outubro',
            '11':'Novembro','12':'Dezembro'}