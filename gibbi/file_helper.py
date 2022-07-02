import pandas as pd
import numpy as np

from constants import BAND_DICT_KEYS
from convert import can_float

def row_to_band_dict(the_row):
    gal_name = ''
    gal_band = ''
    gal_dict = {}
    
    #if row is missing, will be nan
    
    if the_row['name'] == 'NGC1097_i':
    """
    for each_key in BAND_DICT_KEYS:
        if each_key in the_row:
            #print(type(the_row[each_key]))
            gal_dict[each_key] = the_row[each_key]
            
    if the_row['name'] == 'NGC1097_i':
        print(the_row['name'])
        for each_key in gal_dict:
            print(np.isnan(gal_dict[each_key]))
            
    if the_row['name'] == 'NGC1093_g':
        print(the_row['name'])
        for each_key in gal_dict:
            print(np.isnan(gal_dict[each_key]))
    """


#functions to read files:
def read_galaxy_csv(csv_path):
    '''read galaxy data from csv'''
    csv_dict = dict()
    df = pd.read_csv(csv_path,encoding = 'ISO-8859-1')
    
    for index, row in df.iterrows():
        row_to_band_dict(row)