import requests
import pandas as pd
import numpy as np
import pickle
import json
from tqdm import tqdm

'''
Scaping functions to pull data from football index's main website.
'''

# get player data function
def get_player_data(i):
    # make request through FI API
    url = 'https://api-prod.footballindex.co.uk/v2/timeseries?id='+i+'&period=30d&interval=1d'
    response = requests.get(url)
    response_data = json.loads(response.text)
    # extract time series
    tmp = pd.DataFrame(list(response_data['items']))
    # name and order cols
    tmp.rename(columns={'key':'DateTime', 'sumQty':'Volume','minPrice':'minPrice','maxPrice':'maxPrice','avgPrice':'avgPrice'},inplace=True)
    tmp = tmp[['DateTime', 'Volume', 'maxPrice', 'minPrice', 'avgPrice']]
    tmp.fillna(0,inplace=True)
    # reformat date col
    tmp['DateTime'] = tmp['DateTime'].astype(str).str[:10].str.replace('T',' ')
    tmp['DateTime'] = pd.to_datetime(tmp['DateTime'])
    
    return i, tmp 

# use the 24 hour data request to pull todays data
def get_todays_data(i):
    # make request through FI API
    url = 'https://api-prod.footballindex.co.uk/v2/timeseries?id='+i+'&period=1d&interval=2h'
    response = requests.get(url)
    response_data = json.loads(response.text)
    # extract time series
    tmp = pd.DataFrame(list(response_data['items']))
    # name and order cols
    tmp.rename(columns={'key':'DateTime', 'sumQty':'Volume','minPrice':'minPrice','maxPrice':'maxPrice','avgPrice':'avgPrice'},inplace=True)
    tmp = tmp[['DateTime', 'Volume', 'maxPrice', 'minPrice', 'avgPrice']]
    tmp.fillna(0,inplace=True)
    # reformat date col
    tmp['DateTime'] = tmp['DateTime'].astype(str).str[:19].str.replace('T',' ')
    tmp['DateTime'] = pd.to_datetime(tmp['DateTime'])
    # use only todays data
    tmp = tmp[tmp['DateTime'] > pd.Timestamp('today').normalize()].iloc[:-1,:]
    tmp = tmp.mean().to_frame().T
    tmp = tmp.round(2)
    tmp['DateTime'] = pd.to_datetime('today').date()
    tmp['DateTime'] = pd.to_datetime(tmp['DateTime'])
    tmp = tmp[['DateTime', 'Volume', 'maxPrice', 'minPrice', 'avgPrice']]

    return i, tmp 


# Pickle saving functions
def save_obj(file, file_name):
    with open('00_global_player_database/'+ file_name + '.pkl', 'wb') as f:
        pickle.dump(file, f, pickle.HIGHEST_PROTOCOL)

def load_obj(file_name):
    with open('00_global_player_database/' + file_name + '.pkl', 'rb') as f:
        return pickle.load(f)