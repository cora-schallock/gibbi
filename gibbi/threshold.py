import numpy as np
from fits import view_fits

"""
#v1
def get_threshold_range_from_percentile(the_galaxy,the_band,min_percentile=0,max_percentile=95):
    el_data = the_galaxy.ellipse_masks[the_band]*the_galaxy[the_band].fits
    
    min_threshold=np.percentile(el_data[the_galaxy.ellipse_masks[the_band]==1.0], min_percentile)
    max_threshold=np.percentile(el_data[the_galaxy.ellipse_masks[the_band]==1.0], max_percentile)
    
    return (min_threshold,max_threshold)

def threshold_band(the_galaxy,the_band,threshold):
    el_data = the_galaxy.ellipse_masks[the_band]*the_galaxy[the_band].fits
    el_data_threshold = el_data>=threshold
    
    el_pos_theshold = el_data_threshold*the_galaxy.pos_masks[the_band]
    el_neg_theshold = el_data_threshold*the_galaxy.neg_masks[the_band]
    
    pos_sum = np.sum(el_pos_theshold)
    neg_sum = np.sum(el_neg_theshold)
    diff = (pos_sum-neg_sum)/(pos_sum+neg_sum)
    
    return (el_data_threshold, el_pos_theshold, el_neg_theshold, pos_sum, neg_sum, diff)

def iteratively_threshold_band(the_galaxy,the_band,threshold_steps=200,min_percentile=0,max_percentile=95):
    (min_threshold,max_threshold) = get_threshold_range_from_percentile(the_galaxy,the_band,min_percentile,max_percentile)
    the_thresholds = np.linspace(min_threshold,max_threshold,threshold_steps)
    
    the_data_dict = dict()
    for i in range(threshold_steps):
        the_data_dict[i] = threshold_band(the_galaxy,the_band,the_thresholds[i])
    
    return (the_thresholds,the_data_dict,min_threshold,max_threshold,threshold_steps)
"""
"""
#v2
def get_threshold_range_from_percentile(the_galaxy,the_band,min_percentile=0,max_percentile=95):
    el_data = the_galaxy.ellipse_masks[the_band]*the_galaxy[the_band].fits
    valid_pixels = the_galaxy.bands[the_band].good_pixel_mask * the_galaxy.bands[the_band].no_star_mask * the_galaxy.ellipse_masks[the_band]
    
    
    min_valid_pixels = 0.5
    valid_pixels[valid_pixels>min_valid_pixels] = 1.0
    valid_pixels[valid_pixels<=min_valid_pixels] = 0.0

    min_threshold=np.percentile(el_data[valid_pixels==1.0], min_percentile)
    max_threshold=np.percentile(el_data[valid_pixels==1.0], max_percentile)
    
    return (min_threshold,max_threshold,el_data,valid_pixels)

def threshold_band(the_galaxy,the_band,threshold,el_data,valid_pixels):
    el_data_threshold = (el_data*valid_pixels)>=threshold
    
    el_pos_theshold = el_data_threshold*the_galaxy.pos_masks[the_band]
    el_neg_theshold = el_data_threshold*the_galaxy.neg_masks[the_band]
    
    el_pos_valid_pixels = valid_pixels*the_galaxy.pos_masks[the_band]
    el_neg_valid_pixels = valid_pixels*the_galaxy.neg_masks[the_band]
    
    pos_sum = np.sum(el_pos_theshold)/np.sum(el_pos_valid_pixels)
    neg_sum = np.sum(el_neg_theshold)/np.sum(el_neg_valid_pixels)
    diff = (pos_sum-neg_sum)/(pos_sum+neg_sum)
    
    return (el_data_threshold, el_pos_theshold, el_neg_theshold, el_pos_valid_pixels, el_neg_valid_pixels, pos_sum, neg_sum, diff)

def iteratively_threshold_band(the_galaxy,the_band,threshold_steps=200,min_percentile=0,max_percentile=95):
    (min_threshold,max_threshold,el_data,valid_pixels) = get_threshold_range_from_percentile(the_galaxy,the_band,min_percentile,max_percentile)
    the_thresholds = np.linspace(min_threshold,max_threshold,threshold_steps)
    
    the_data_dict = dict()
    for i in range(threshold_steps):
        the_data_dict[i] = threshold_band(the_galaxy,the_band,the_thresholds[i],el_data,valid_pixels)
    
    return (the_thresholds,the_data_dict,min_threshold,max_threshold,threshold_steps,el_data,valid_pixels)
"""

def precompute_threshold_arrays(the_galaxy,the_band,min_valid_pixel_threshold=0.5):
    #Step 1) Calculate valid_pixel_mask  (1's for pixels considered, 0's for pixels ignored)
    valid_pixel_mask = the_galaxy.bands[the_band].good_pixel_mask * the_galaxy.bands[the_band].no_star_mask * the_galaxy.ellipse_masks[the_band]
    valid_pixel_mask[valid_pixel_mask>min_valid_pixel_threshold] = 1.0
    valid_pixel_mask[valid_pixel_mask<=min_valid_pixel_threshold] = 0.0
    
    #Step 2) Calculate el_data (valid_pixel_mask applied to fits)
    el_data = the_galaxy.ellipse_masks[the_band]*valid_pixel_mask*the_galaxy[the_band].fits
    
    return (el_data,valid_pixel_mask)

def get_threshold_range_from_percentile(el_data,valid_pixel_mask,min_percentile=0,max_percentile=95):
    min_threshold=np.percentile(el_data[valid_pixel_mask==1.0], min_percentile)
    max_threshold=np.percentile(el_data[valid_pixel_mask==1.0], max_percentile)
    
    return (min_threshold,max_threshold)

def threshold_band(the_galaxy,the_band,threshold,el_data,valid_pixels,pos_area,neg_area):
    el_data_threshold = el_data>=threshold
    
    el_pos_theshold = el_data_threshold*the_galaxy.pos_masks[the_band]
    el_neg_theshold = el_data_threshold*the_galaxy.neg_masks[the_band]
    
    pos = np.sum(el_pos_theshold)/pos_area
    neg = np.sum(el_neg_theshold)/neg_area
    diff = (pos-neg)/(pos+neg)
    
    return (el_data_threshold, el_pos_theshold, el_neg_theshold, pos, neg, diff)
    

def iteratively_threshold_band_with_percentile(the_galaxy,the_band,threshold_steps=200,min_percentile=0,max_percentile=95):
    #Step 1) Compute el_data and valid_pixel_mask
    (el_data,valid_pixel_mask) = precompute_threshold_arrays(the_galaxy,the_band)
    
    #Step 2) Calculate thresholds (via percentile)
    (min_threshold,max_threshold) = get_threshold_range_from_percentile(el_data,valid_pixel_mask,min_percentile,max_percentile)
    the_thresholds = np.linspace(min_threshold,max_threshold,threshold_steps)
    the_percentiles = np.linspace(min_percentile,max_percentile,threshold_steps)
    
    #Step 3) Calculate pos and neg area (how many pixels on each side are valid and in elipse)
    pos_area = np.sum(valid_pixel_mask*the_galaxy.pos_masks[the_band]*the_galaxy.ellipse_masks[the_band])
    neg_area = np.sum(valid_pixel_mask*the_galaxy.pos_masks[the_band]*the_galaxy.ellipse_masks[the_band])
    
    the_data_dict = dict()
    for i in range(threshold_steps):
        the_data_dict[i] = threshold_band(the_galaxy,the_band,the_thresholds[i],el_data,valid_pixel_mask,pos_area,neg_area)
    
    return (el_data,valid_pixel_mask,the_thresholds,the_data_dict,the_percentiles)