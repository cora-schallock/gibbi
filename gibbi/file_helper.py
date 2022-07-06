import os
import pandas as pd
import numpy as np


from constants import BAND_DICT_KEYS
from convert import can_float

def row_to_band_dict(the_row):
    gal_name = ''
    gal_band = ''
    gal_dict = {}
    
    #if row is missing, will be nan
    
    if 'name' in the_row:
        [gal_name,gal_band] = the_row['name'].strip().rsplit("_",1)
    
    for key in BAND_DICT_KEYS:
        if key in the_row and not np.isnan(the_row[key]):
            gal_dict[key] = the_row[key]

    return gal_name, gal_band, gal_dict


#functions to read files:
def read_galaxy_csv(csv_path):
    '''read galaxy data from csv'''
    csv_dict = dict()
    df = pd.read_csv(csv_path,encoding = 'ISO-8859-1')
    
    for index, row in df.iterrows():
        gal_name, gal_band, gal_dict = row_to_band_dict(row)
        
        if gal_name != "" and gal_band != "" and len(gal_dict) == len(BAND_DICT_KEYS):
            if gal_name not in csv_dict:
                csv_dict[gal_name] = dict()
                
            csv_dict[gal_name][gal_band] = gal_dict
    return csv_dict

#folder helper
def check_if_folder_exists_and_create(path):
    '''check if folder exists and if not, create it'''
    if not os.path.exists(path):
        os.makedirs(path)