import pandas as pd
import re

def htsRead(df):
    try:
        tariffs = df['Tariff #']
    except:
        return 'Not a valid HTS file'
    index = 1
    error = False
    counter = 0
    columns = ['ImporterAccount', 'FilerCode', 'PartNumber', 'Description', 'Country', 'Tariff #', 'CountryOfOrigin']

    read_result = {
        'Printout': [],
        'Tariffs-affected': [],
        'Final-df': pd.DataFrame(columns=columns)
    }

    for tariff in tariffs:
        index+=1
        regx = re.compile('(?:(?:[\d]{4}\.[\d]{2}\.(?:[\d]{2}|[\d]{4}))(?:$|,))|(?:(?:[\d]{8}|[\d]{10})(?:$|,))')
        no_space_tariff = re.sub(' ', '', str(tariff))
        checkTariff = re.sub(regx, '', str(no_space_tariff))
        if not checkTariff == '':
            error = True
            read_result['Final-df'].loc[counter] = df.loc[index-2]
            counter += 1
            read_result['Tariffs-affected'].append(index)
            read_result['Printout'].append('{})Tariff {} has an issue at row {}'.format(counter, tariff, index))           

    if not error:
        read_result['Printout'].append('No tariffs presented errors')


    return read_result