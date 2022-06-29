import numpy as np

from mask import create_elliptical_mask

def read_sextractor_file(file_path):
    keys = []
    objects = []
    
    with open(file_path,"r") as f:
        for line in f:
            if line.startswith('#'):
                current_key = line.split()[2] #split() (no args) splits on all whitespace: https://stackoverflow.com/a/4309689
                keys.append(current_key)
            else:
                values = map(lambda x: float(x), line.split())
                objects.append(dict(zip(keys,values)))
    return objects

def filter_objects(objects,fits_shape, min_star_class=0.1):
    #Step 1: Initalize list of objects to return and array of sizes:
    objects_to_keep = objects
    the_sizes = np.zeros(len(objects))
    
    #Step 2: Calculate sizes (A + B):
    for i in range(len(objects)):
        the_sizes[i] = objects[i]["A_IMAGE"]+objects[i]["B_IMAGE"]
        
    #Step 3: Remove largest size and return remaining objects:
    del objects_to_keep[np.argmax(the_sizes)]
    
    #Step 4: Filter out objects that are classified as galaxies (i.e. "CLASS_STAR">=min_star_class):
    objects_to_keep = list(filter(lambda o: o["CLASS_STAR"]>=min_star_class,objects_to_keep))
    
    #Step 5: Filter out objects whose center is outside bounds of image:
    # For example: NGC3312 has an object with dict = {'XWIN_IMAGE': 765.473, 'YWIN_IMAGE': -7.86, ...}
    # Needs to be filtered out
    objects_to_keep = list(filter(lambda o: o['XWIN_IMAGE']-1>=0 and o['XWIN_IMAGE']-1<fits_shape[1],objects_to_keep))
    objects_to_keep = list(filter(lambda o: o['YWIN_IMAGE']-1>=0 and o['YWIN_IMAGE']-1<fits_shape[0],objects_to_keep))
    
    return objects_to_keep

def make_star_mask_from_sextractor_file(sex_path,fits_shape,min_star_class=0.1):
    #Step 1: Initalize star mask (nothing masked out)
    the_final_mask = np.zeros(fits_shape)
    
    #Step 2: Read in sextractor file, and then filter out objects (i.e. ignore galaxies, and main galaxy object)
    objects = read_sextractor_file(sex_path)
    objects_to_mask = filter_objects(objects,fits_shape,min_star_class=min_star_class)
    
    #Step 3: Add stars to mask
    for gal_dict in objects_to_mask:
        the_mask = create_elliptical_mask(gal_dict['XWIN_IMAGE']-1,
                                          gal_dict['YWIN_IMAGE']-1,
                                          gal_dict['A_IMAGE'],
                                          gal_dict['B_IMAGE'],
                                          np.radians(gal_dict['THETA_IMAGE']),
                                          shape=fits_shape)
        the_final_mask += the_mask
    the_final_mask[the_final_mask>0] = 1.0 #in the case of overlapping stars, normalize to 1.0
    
    return the_final_mask

    
    