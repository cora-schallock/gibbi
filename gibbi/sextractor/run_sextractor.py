import os
import subprocess
import sys
import pathlib

CONFIGURATION_FILE_PATH = 'star_rm.sex'
SEX_PATH = './sex'

def is_windows():
    return os.name == "nt"

def is_linux():
    return os.name == "posix"

##Although they are slower, it is recommended to use whenever possible windowed position parameters instead of their isophotal equivalents; the measurements they provide are generally much more accurate (Fig. 7). The centroiding accuracy of XWIN_IMAGE and YWIN_IMAGE is actually very close to that of PSF-fitting on focused and properly sampled star images. Windowed measurements can also be applied to galaxies. It has been verified that for isolated objects with Gaussian-like profiles, their accuracy is close to the theoretical limit set by image noise
#SOURCE: https://sextractor.readthedocs.io/en/latest/PositionWin.html

#https://sextractor.readthedocs.io/en/latest/PositionWin.html
#for positional params

def run_sextractor(fits_path,output_path='output.txt'):

    #path issue with source exctator:
    original_working_dir = os.getcwd()
    #print(original_working_dir)
    new_working_dir = pathlib.Path(__file__).parent.absolute()
    os.chdir(new_working_dir)
    #print(new_working_dir)

    res = 0
    try:
        # Add any other sextractor parameters here
        # Any other output paramers you want you need to put in the star_rm.param
        # A complete list of parameters can be seen by running ./sex -dp
        # default.param

        #1) Create subprocess (if on windows, run on WSL, or if on linux use bash)
        if is_windows():
            proc = subprocess.Popen(
                ['cmd', '/c', 'ubuntu1804', 'run', SEX_PATH, fits_path, '-c', CONFIGURATION_FILE_PATH, '-CATALOG_NAME',
                 output_path], stderr=subprocess.PIPE) #run with wsl on windows
            #^ see post for more info: https://stackoverflow.com/questions/57693460/using-wsl-bash-from-within-python
            
            #This was for a test regarding spaces in name:
            #cmd = ['cmd', '/c', 'ubuntu1804', 'run', SEX_PATH, fits_path.replace(' ', '\ '), '-c', CONFIGURATION_FILE_PATH, '-CATALOG_NAME', output_path.replace(' ', '\ ')]
            #fits_path = '"{}"'.format(fits_path) if ' ' in fits_path else fits_path
            #output_path = '"{}"'.format(output_path) if ' ' in output_path else fits_path
            #cmd = ['cmd', '/c', 'ubuntu1804', 'run', SEX_PATH, fits_path, '-c', CONFIGURATION_FILE_PATH, '-CATALOG_NAME', output_path]
            #print(cmd)
            #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            
            
        elif is_linux():
            proc = subprocess.Popen([SEX_PATH, fits_path, '-c', CONFIGURATION_FILE_PATH, '-CATALOG_NAME', output_path],
                                    stderr=subprocess.PIPE)
        else:
            raise OSError("Not recognized OS, must be Windows or Linux")

        #2) Connect stdout and stderror, and wait for process to end:
        out, err = proc.communicate()
        res = proc.wait()

        #print(err)

        #3) check if error was raised by subprocess:
        if res != 0: raise Exception
            
        os.chdir(original_working_dir) #Keep this or it will break other code
        
    except Exception as e:
        print('Error in running sextractor:{}'.format(e))  
    finally:
        os.chdir(original_working_dir) #Important to keep this, or else other code will break (i.e. code that uses relative paths)

def run_sextractor_on_command_line():
    if len(sys.argv) <= 2:
        print('USAGE: PythonSextractor fitsImagePath')
    else:
        fits_path = sys.argv[1]
        output_path = sys.argv[2]
        if os.path.exists(fits_path):
            run_sextractor(fits_path,output_path)
        else:
            print(fits_path, 'is not a valid path.')

if __name__ == "__main__":
    run_sextractor_on_command_line()
#https://stackoverflow.com/q/57693460/13544635