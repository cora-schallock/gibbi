import os
import numpy as np
import matplotlib
#matplotlib.use('Agg') #use this to not display
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg


from constants import PAN_STARRS1_BANDS
from fits import view_fits

from file_helper import check_if_folder_exists_and_create
"""
THE Pan-STARRS1 PHOTOMETRIC SYSTEM:
[Filter] [Mean Wavelength(A)]
g 4866 
r 6215
i 7545 
z 8679 
y 9633 
source: https://outerspace.stsci.edu/display/PANSTARRS/PS1+Filter+properties
"""

PANSTARRS_COLOR_DICT = {'g':'green',
                        'r':'red',
                        'i':'indigo',
                        'z':'blue',
                        'y':'orange'}
#color names: https://matplotlib.org/3.1.0/_images/sphx_glr_named_colors_003.png

DEFAULT_POSITIVE_RGB_VECTOR = [60/255,179/255,113/255] #mediumseagreen
DEFAULT_NEGATIVE_RGB_VECTOR = [240/255,128/255,125/255] #lightcoral
DEFAULT_BAD_PIXEL_RGB_VECTOR = [169/255,169/255,169/255] #lightgrey

def create_color_map_class(pos,neg,valid_pixels):
    cmap_class = np.zeros((pos.shape[0],pos.shape[1],3))
    
    cmap_class[pos>=1.0] = DEFAULT_POSITIVE_RGB_VECTOR
    cmap_class[neg>=1.0] = DEFAULT_NEGATIVE_RGB_VECTOR
    cmap_class[valid_pixels<1.0] = DEFAULT_BAD_PIXEL_RGB_VECTOR
    
    return cmap_class

def make_cmap_class_for_bands(the_gal,valid_pixel_mask_dict):
    cmaps_class_for_bands = dict()
    
    for the_band in the_gal.valid_bands: #used to be the_gal.bands
        cmap_class = create_color_map_class(the_gal.pos_masks[the_band],the_gal.neg_masks[the_band],valid_pixel_mask_dict[the_band])
        cmaps_class_for_bands[the_band] = cmap_class
    return cmaps_class_for_bands

def construct_color_image_plot(the_gal,ax_color,img,dark_side=""):
    #Step 4) Add color image:
    
    ax_color.imshow(img)
    the_title = the_gal.name
    if dark_side != "":
        the_title += ": dark side = {}".format(dark_side)
    
    ax_color.title.set_text(the_title)
    ax_color.axis('off')


def construct_threshold_mask_plot(band_subplot,threshold_mask,band_title="",band_title_color="k",cmap=None):
    band_subplot.imshow(threshold_mask, origin='lower')
    if not isinstance(cmap,type(None)):
        band_subplot.imshow(cmap, origin= 'lower',alpha=0.45)
    band_subplot.set_title(band_title, color=band_title_color)
    band_subplot.axis('off')
    
def construct_diff_plot(xs,diff_dict,ax_combined,diff_line=-1):
    #Step 1) Plot difference vs. percentil graph for each band
    for band in xs:
        ax_combined.plot(xs[band],diff_dict[band],color=PANSTARRS_COLOR_DICT[band], label=band) 
   
    #Step 2) If applicable, plot verticle line (indicating current percentile threshold)
    if diff_line != -1:
        ax_combined.axvline(diff_line)
    
    #Step 3) Add labels and legend
    ax_combined.set_xlabel('percentile')
    ax_combined.set_ylabel('threshold diff.')
    ax_combined.legend(loc="lower left")
    
def make_panstarr_threshold_figure(xs,diff_dict,el_data_threshold_dict,valid_pixel_mask_dict,threshold_index_to_use,the_gal,color_image,dark_side="",file_output=""):
    #Step 1) Initalize plt subplots (use mosaic to customize laylout)
    gs_kw = dict(width_ratios=[1,1,1,2.25], height_ratios=[1, 1])
    fig, axd = plt.subplot_mosaic([['color','g','r', 'combined'],
                                   ['i','z','y', 'combined']],
                                  gridspec_kw=gs_kw, figsize = (22,8),
                                  constrained_layout=True)
    fig.patch.set_facecolor('white')
    
    #Step 2) Add threshold_mask plots for each band
    cmaps = make_cmap_class_for_bands(the_gal,valid_pixel_mask_dict)
    for each_band in the_gal.valid_bands:
        band_subplot = axd[each_band]
        threshold_mask = el_data_threshold_dict[each_band][threshold_index_to_use]
        
        band_title = "{} band: {:.1f}% (of max per band)".format(each_band,xs[each_band][threshold_index_to_use])
        construct_threshold_mask_plot(band_subplot,threshold_mask,band_title,PANSTARRS_COLOR_DICT[each_band],cmaps[each_band])
        
    #Step 3) Add Diff plot
    ax_combined = axd['combined']
    construct_diff_plot(xs,diff_dict,ax_combined,xs[the_gal.valid_bands[0]][threshold_index_to_use])
    
    #Step 4) Add color image plot
    ax_color = axd['color']
    construct_color_image_plot(the_gal,ax_color,color_image,dark_side=dark_side)
        
    #Step 5) Save figure (if file_output != '') otherwise display it
    if file_output != "":
        fig.savefig(file_output, dpi = 300, bbox_inches='tight')
    else:
        plt.show()
    plt.close(fig)
            
        
def run_visualize(xs,diff_dict,el_data_threshold_dict,valid_pixel_mask_dict,the_gal,visualize_path,dark_side=""):
    threshold_range = xs[the_gal.valid_bands[0]]
    
    gal_output_path = os.path.join(visualize_path,the_gal.name)
    check_if_folder_exists_and_create(gal_output_path)
    
    color_image = mpimg.imread(the_gal.color_image_path)
    
    for i in range(len(threshold_range)):
        if i%5 == 0:
            threshold = threshold_range[i]
            file_output = os.path.join(gal_output_path,'{}.png'.format(i))
        
            make_panstarr_threshold_figure(xs,diff_dict,el_data_threshold_dict,valid_pixel_mask_dict,i,the_gal,color_image,dark_side=dark_side,file_output=file_output)
    