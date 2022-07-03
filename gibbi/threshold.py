import numpy as np

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