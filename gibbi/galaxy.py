from constants import *
from fits import read_fits
from mask import create_elliptical_mask, create_bisection_masks
from convert import can_float, convert_matlab_to_cartessian, convert_disk_angle_to_bisection_angle, normalize_angle

class galaxy:
    #def __init__(self,name,bands_to_load=[]):
    def __init__(self,name,bands_dict={}):
        self.name = name
        self.bands = {}
        self.valid_bands = []
        self.ref_band = None
        #self.color_image_path = get_color_image_path(name)
        
        self.ellipse_masks = {}
        self.pos_masks = {}
        self.neg_masks = {}
        
        #initalize bands (from band dict)
        if len(bands_dict) != 0:
            for each_band in bands_dict:
                self.load_band(each_band,bands_dict[each_band])
        
    def has_band(self,band):
        return band in self.bands.keys()
    
    def load_band(self,band,dict_for_band):
        the_band = galaxy_band(self.name, band, dict_for_band)
        the_band.load()
        
        self.bands[band] = the_band
        
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
                elif each_key == DISK_MIN_AXS_LEN:
                    self.diskMinAxsLen = float(band_dict[each_key])
                elif each_key == DISK_MAJ_AXS_LEN:
                    self.diskMajAxsLen = float(band_dict[each_key])
                elif each_key == INPUT_CENTER_C:
                    self.inputCenterC = float(band_dict[each_key])
                elif each_key == INPUT_CENTER_R:
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
        
    
