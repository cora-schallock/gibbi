"""
#Path to CSV and FITS:
CSV_DIR_PATH = "C:\\Users\\cora\\Desktop\\research\\data\\sparcfire_run\\table2"
FITS_DIR_PATH = "C:\\Users\\cora\\Desktop\\research\\data\\galaxy\\table2"
DATA_FOLDER = "C:\\Users\\cora\\Desktop\\current_research\\data\\table2"
"""
#BANDS:
PAN_STARRS1_BANDS = ["g","r","i","y","z"]

#CSV KEYS:
NAME_KEY = "name"
BAND_KEY = "band"

DISK_MAJ_ANGLE_KEY = 'diskMajAxsAngleRadians'
DISK_MIN_AXS_LEN_KEY = 'diskMinAxsLen'
DISK_MAJ_AXS_LEN_KEY = 'diskMajAxsLen'
INPUT_CENTER_C_KEY = 'inputCenterC'
INPUT_CENTER_R_KEY ='inputCenterR'

BULGE_MIN_AXS_LEN_KEY = "bulgeMinAxsLen"
BULGE_MAJ_AXS_LEN_KEY = "bulgeMajAxsLen"
BULGE_AXS_RATIO_KEY = "bulgeAxisRatio"
BULGE_MAJ_AXS_ANGLE_KEY = "bulgeMajAxsAngle"

#Keys required in BAND DICT
BAND_DICT_KEYS = [DISK_MAJ_ANGLE_KEY,
                 DISK_MIN_AXS_LEN_KEY,
                 DISK_MAJ_AXS_LEN_KEY,
                 INPUT_CENTER_C_KEY,
                 INPUT_CENTER_R_KEY,
                 BULGE_AXS_RATIO_KEY,
                 BULGE_MAJ_AXS_LEN_KEY,
                 BULGE_MAJ_AXS_ANGLE_KEY]


"""
CARTESSIAN_ANGLE_KEY = "cartessian_angle"
POS_FLUX_KEY = "pos_flux"
NEG_FLUX_KEY = "neg_flux"
FLUX_PERCENT_DIFF_KEY = "flux_percent_diff"
SCALE_FACTOR_KEY = "scale_factor"
CORRECT_LABEL_KEY = "correct_label"
OBSERVED_LABEL_KEY = "observed_label"



KEY_LIST = [NAME_KEY, BAND_KEY, DISK_MAJ_ANGLE_KEY, DISK_MIN_AXS_LEN, DISK_MAJ_AXS_LEN, INPUT_CENTER_C, INPUT_CENTER_R,
            BULGE_MAJ_AXS_LEN_KEY, BULGE_MIN_AXS_LEN_KEY, BULGE_AXS_RATIO_KEY,BULGE_MAJ_AXS_ANGLE_KEY,
            CARTESSIAN_ANGLE_KEY, POS_FLUX_KEY, NEG_FLUX_KEY, FLUX_PERCENT_DIFF_KEY, SCALE_FACTOR_KEY,
            CORRECT_LABEL_KEY, OBSERVED_LABEL_KEY]
            
"""