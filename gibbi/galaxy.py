import os

from constants import *
from fits import read_fits
from mask import create_elliptical_mask, create_bisection_masks
from convert import can_float, convert_matlab_to_cartessian, convert_disk_angle_to_bisection_angle, normalize_angle

class galaxy:
    #def __init__(self,name,bands_to_load=[]):
    def __init__(self,name,bands_dict={},gal_color_image_path="",fits_path_function=None,bad_pixel_path_function=None,star_mask_path_function=None):
        self.name = name
        self.bands = {}
        self.valid_bands = []
        self.ref_band = None
        self.color_image_path = gal_color_image_path
        
        self.ellipse_masks = {}
        self.pos_masks = {}
        self.neg_masks = {}
        
        #initalize bands (from band dict)
        self.load_all_bands(bands_dict)
        self.load_all_fits(fits_path_function,bad_pixel_path_function,star_mask_path_function)
        
    def has_band(self,band):
        return band in self.bands.keys()
    
    def load_all_bands(self,bands_dict):
        for each_band in bands_dict:
            the_band = galaxy_band(self.name, each_band, bands_dict[each_band])
            self.bands[each_band] = the_band
        
    def load_all_fits(self,fits_path_function,bad_pixel_path_function,star_mask_path_function):
        for each_band in self.bands:
            if fits_path_function != None:
                try:
                    fits_path_for_band = fits_path_function(self.name,each_band)
                    
                    if os.path.exists(fits_path_for_band):
                        self.bands[each_band].load_fits(fits_path_for_band)
                except Exception as e:
                    print("Error loading fits for {} {} band: {}".format(self.name,each_band,e))
            if bad_pixel_path_function != None:
                try:
                    bad_pixel_path_for_band = bad_pixel_path_function(self.name,each_band)
                    
                    if os.path.exists(bad_pixel_path_for_band):
                        self.bands[each_band].load_bad_pixel_mask(bad_pixel_path_for_band)
                except Exception as e:
                    print("Error loading bad pixel mask for {} {} band: {}".format(self.name,each_band,e))
                    
            if star_mask_path_function != None:
                try:
                    star_mask_path_for_band = star_mask_path_function(self.name,each_band)
                    
                    if os.path.exists(star_mask_path_for_band):
                        self.bands[each_band].load_star_mask(star_mask_path_for_band)
                except Exception as e:
                    print("Error loading star mask for {} {} band: {}".format(self.name,each_band,e))
                
            
        
    def create_masks(self):
        #to do: Check this
        valid_ref = False
        if self.ref_band != None and self.has_band(self.ref_band):
            (a,b) = (self.bands[self.ref_band].a, self.bands[self.ref_band].b) 
            theta = self.bands[self.ref_band].theta
            
        for each_band in self.bands.keys():
            if not valid_ref:
                (a,b) = (self.bands[each_band].a, self.bands[each_band].b) 
                theta = self.bands[each_band].theta
            (h, k) = (self.bands[each_band].h,self.bands[each_band].k)
            shape = self.bands[each_band].shape
            
            try:
                ellipse_masks = create_elliptical_mask(h, k, a, b, theta, shape)
                (pos_mask,neg_mask) = create_bisection_masks(h, k, a, b, theta, shape)
            
                self.ellipse_masks[each_band] = ellipse_masks
                self.pos_masks[each_band] = pos_mask
                self.neg_masks[each_band] = neg_mask
                
                self.valid_bands.append(each_band)
            except Exception as e:
                print("Error in {} {} band: {}".format(self.name,each_band,e))
        
    def __getitem__(self,band):
        if band in self.bands.keys():
            return self.bands[band]
        
    def __str__(self):
        return "{}: {} (ref band={})".format(self.name,str(sorted(self.bands.keys())),self.ref_band)
    
    def __repr__(self):
        return self.__str__()
            
class galaxy_band:
    def __init__(self, name, band, band_dict={}):
        #galaxy info:
        self.name = name
        self.band = band
        self.fits = None
        self.shape = None
        
        self.bad_pixel_mask = None# 1's for bad pixels, 0's for good pixels
        self.good_pixel_mask = None #1's for good pixels, 0's for bad pixels
        
        self.star_mask = None #1's for stars, 0's for no star
        self.no_star_mask = None #0's for stars, 1's for no star
        
        #galaxy params (from SpArcFiRe):
        self.diskMajAxsAngleRadians = 0.0
        self.diskMinAxsLen = 0.0
        self.diskMajAxsLen = 0.0
        self.inputCenterC = 0.0
        self.inputCenterR = 0.0
        
        #bulge params (from SpArcFiRe):
        self.bulgeAxisRatio = 0.0
        self.bulgeMajAxsLen = 0.0
        self.bulgeMajAxsAngle = 0.0
        
        #ellipse params (for gibbi!):
        self.h = 0.0
        self.k = 0.0
        self.a = 0.0
        self.b = 0.0
        self.theta = 0.0
        
        #load band dict:
        if band_dict != {}:
            self.load_band_dict(band_dict)
        
    def calculate_ellipse_params(self):
        (self.h, self.k) = convert_matlab_to_cartessian(self.inputCenterC, self.inputCenterR)
        self.a = self.diskMajAxsLen * 0.5
        self.b = self.diskMinAxsLen * 0.5
        self.theta = convert_disk_angle_to_bisection_angle(self.diskMajAxsAngleRadians)
        
    def load_band_dict(self,band_dict):
        for each_key in band_dict:
            if can_float(band_dict[each_key]):
                if each_key == DISK_MAJ_ANGLE_KEY:
                    self.diskMajAxsAngleRadians = float(band_dict[each_key])
                elif each_key == DISK_MIN_AXS_LEN_KEY:
                    self.diskMinAxsLen = float(band_dict[each_key])
                elif each_key == DISK_MAJ_AXS_LEN_KEY:
                    self.diskMajAxsLen = float(band_dict[each_key])
                elif each_key == INPUT_CENTER_C_KEY:
                    self.inputCenterC = float(band_dict[each_key])
                elif each_key == INPUT_CENTER_R_KEY:
                    self.inputCenterR = float(band_dict[each_key])
                elif each_key == BULGE_AXS_RATIO_KEY:
                    self.bulgeAxisRatio = float(band_dict[each_key])
                elif each_key == BULGE_MAJ_AXS_LEN_KEY:
                    self.bulgeMajAxsLen = float(band_dict[each_key])
                elif each_key == BULGE_MAJ_AXS_ANGLE_KEY:
                    self.bulgeMajAxsAngle = float(band_dict[each_key])
        self.calculate_ellipse_params()
                    
    def load_fits(self,fits_path):
        self.fits = read_fits(fits_path)
        self.shape = self.fits.shape
        
    def load_bad_pixel_mask(self,bad_pixel_path_for_band):
        self.bad_pixel_mask = read_fits(bad_pixel_path_for_band)
        self.good_pixel_mask = 1-self.bad_pixel_mask
        
    def load_star_mask(self,star_mask_path_for_band):
        self.star_mask = read_fits(star_mask_path_for_band)
        self.no_star_mask = 1-self.star_mask
    
