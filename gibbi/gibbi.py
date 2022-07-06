import numpy as np

from threshold import iteratively_threshold_band_with_percentile

def extract_diffs(the_data_dict):
    
    for i in range(len(the_data_dict)):
        diffs[i] = the_data_dict[i][-1]
    return diffs

def extract_data_dict(the_data_dict,the_band_size):
    the_size = (len(the_data_dict),the_band_size[0],the_band_size[1])
    
    diffs = np.zeros(len(the_data_dict))
    #el_data_thresholds = np.zeros(the_size)
    el_data_thresholds = []
    
    for i in range(len(the_data_dict)):
        #el_data_thresholds[i] = the_data_dict[i][0]
        el_data_thresholds.append(the_data_dict[i][0])
        diffs[i] = the_data_dict[i][-1]
        
    return (el_data_thresholds,diffs)
        

def run_gibbi_on_galaxy(the_gal,threshold_steps=96,min_percentile=0,max_percentile=95):
    #20 good
    #make sure you have computed the mask already
    
    xs = dict()
    diff_dict = dict()
    el_data_threshold_dict = dict()
    valid_pixel_mask_dict = dict()
    
    for each_band in the_gal.valid_bands:
        the_band_size = the_gal.bands[each_band].shape
        
        (el_data,valid_pixel_mask,the_thresholds,the_data_dict,the_percentiles) = iteratively_threshold_band_with_percentile(the_gal,
                                                                                                                             each_band,
                                                                                                                             threshold_steps,
                                                                                                                             min_percentile,
                                                                                                                             max_percentile)
        
        (el_data_thresholds,diffs) = extract_data_dict(the_data_dict,the_band_size)
        
        xs[each_band] = the_percentiles
        diff_dict[each_band] = diffs
        el_data_threshold_dict[each_band] = el_data_thresholds
        valid_pixel_mask_dict[each_band] = valid_pixel_mask
    
    return (xs,diff_dict,el_data_threshold_dict,valid_pixel_mask_dict)