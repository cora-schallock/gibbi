import numpy as np
from photutils.aperture import ellipse

from matrix import create_disk_angle_matrix
    
#Ellipse Mask:
##########################################################################################################################
# NOTE:                                                                                                                  #       
#   Elliptical apperature uses the following coordinate convention:                                                      #
#      In Photutils, pixel coordinates are zero-indexed, meaning that (x, y) = (0, 0) corresponds to the center of the   #
#      lowest, leftmost array element. This means that the value of data[0, 0] is taken as the value over the range      # 
#      -0.5 < x <= 0.5, -0.5 < y <= 0.5.                                                                                 #
#    Source: https://buildmedia.readthedocs.org/media/pdf/photutils/v0.3/photutils.pdf                                   #
#    Documentation:https://photutils.readthedocs.io/en/stable/api/photutils.aperture.EllipticalAperture.html             #
#                                                                                                                        #
#   This differs from the SourceExtractor, IRAF, FITS, and ds9 conventions, in                                           #
#      which the center of the lowest, leftmost array element is (1, 1).                                                 #
#     Source: See pg.59 in http://star-www.dur.ac.uk/~pdraper/extractor/Guide2source_extractor.pdf                       #
##########################################################################################################################

def create_elliptical_mask(h, k, a, b, theta, shape=(240,240)):
    the_ellipse = ellipse.EllipticalAperture((h,k), a, b, theta=theta)
    mask = the_ellipse.to_mask(method='exact')
    return mask.to_image(shape) #don't convert to int with .astype(int), there's a really weird bug

#Bisection Mask:
def create_bisection_masks(h, k, a, b, theta, shape=(240,240)):
    disk_angle_matrix = create_disk_angle_matrix(h,k,theta,shape)
    
    pos_mask = (disk_angle_matrix<np.pi)
    neg_mask = (disk_angle_matrix>=np.pi)
    
    return (pos_mask, neg_mask)