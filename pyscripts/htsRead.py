import pandas as pd
import requests as rq
import ssl
import re

def htsRead(df):
    
    try:
        tariffs = df['Tariff #']
    except:
        return 'Not a valid HTS file'
    index = 1
    error = False
    counter = 0
    columns = df.columns.tolist()

    read_result = {
        'Printout': [],
        'Tariffs-affected': [],
        'Final-df': pd.DataFrame(columns=columns),
        'Details': []
    }

    for tariff in tariffs:
        index+=1
        regx = re.compile('(?:(?:[\d]{4}\.[\d]{2}\.(?:[\d]{2}|[\d]{4}))(?:$|,))|(?:(?:[\d]{8}|[\d]{10})(?:$|,))')
        no_space_tariff = re.sub(' ', '', str(tariff))
        checkTariff = re.sub(regx, '', str(no_space_tariff))
        if not checkTariff == '':
            error = True
            read_result['Details'].append(errorDetails(tariff=tariff))
            read_result['Final-df'].loc[counter] = df.loc[index-2]
            counter += 1
            read_result['Tariffs-affected'].append(index)
            read_result['Printout'].append(tariff)
        else:
            from pyscripts import tariffRead



    if not error:
        read_result['Printout'].append('No tariffs presented errors')


    return read_result

def errorDetails(tariff):
    regx_characters = re.compile('[^0-9.,]+')
    character_errors = regx_characters.findall(str(tariff))

    error_details = {}

    if(len(character_errors) > 0):
        error_details['characters'] = character_errors
    else:
        error_details['characters'] = ['No incompatible characters found in analysis']

    error_details['length'] = len(str(tariff))

    return error_details