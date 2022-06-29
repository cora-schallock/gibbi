import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def write_fits(path,data):
    #write fits file to path
    hdul = fits.PrimaryHDU(data)
    hdul.writeto(path)

def read_fits(path):
    #read fits files
    hdul = fits.open(path)
    data = hdul[0].data
    return data

def preprocess_fits(the_fits,offset=10):
    preprocessed_fits = the_fits
    bad_pixel_mask = np.zeros(the_fits.shape)
    
    bad_pixel_mask[np.isnan(the_fits)] = 1.0
    bad_pixel_mask[np.isinf(the_fits)] = 1.0
    
    preprocessed_fits[bad_pixel_mask==1.0] = 0.0
    
    the_min = np.min(preprocessed_fits)
    total_offset = max([0,-the_min]) + offset
    preprocessed_fits += total_offset
    
    return preprocessed_fits,bad_pixel_mask

def view_fits(fits_to_view,title="", save_path = ""):
    plt.figure(figsize=(20,10))
    plt.imshow(fits_to_view, origin= 'lower') #, cmap='gray' #,cmap='inferno'
    plt.title(title)
    plt.colorbar()
    
    plt.show()
    
def save_fits(fits_to_view,title="", save_path = ""):
    plt.figure(figsize=(20,10))
    plt.imshow(fits_to_view, origin= 'lower') #, cmap='gray' #,cmap='inferno'
    plt.title(title)
    plt.colorbar()
    
    plt.savefig(save_path)
    
    plt.clf()
    plt.close()