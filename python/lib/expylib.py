import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib.cm as clr_b
import matplotlib as matplotlib
import glob as glob
import re

"""
Library for the analysis of AFM data from exosome. 
"""

def TimeSort(fnames):
    """
    fnames: Array of files with force-distance information 
    returns: Array of files sorted based on time index.
    """
    tidx = [f[-16:-4].replace('.', '') for f in fnames]
    tidx = np.asarray(tidx, dtype=int)
    idx = np.argsort(tidx)
    fn = [fnames[i] for i in idx]
    # fn = files[idx]
    return fn


def ReadFromFolder(folder):
    """
    folder : The folder containing the AFM force-distance in ascii
    return : Array of the files inside sorted based on indentation [1st, 2nd, .. nth, .. last] indentation 
    """
    try:
       files_ = glob.glob(folder+"/processed_curves-*/force-save*.txt")
    except:
       print(f"The folder {folder} does contain the folder processed_curves-* where files force-save- are stored")
       print("See documentation on how to arrange the data", folder)
       raise
    return TimeSort(files_)


def ReadSingleFile(f):
    """
    f: filename
    returns: data read from the ascii file
    """
    d1, d2, fpush, fretrace = np.asarray([]), np.asarray([]), np.asarray([]), np.asarray([])
    try:
       f = open(f, "r")
    except:
       print(f"file {f} doesn't exist check the code.") 
       raise
    lines = f.readlines()
    is_push = True
    for line in lines: #.split("\n"):
        if line == '\n':
            is_push = False
        if is_push and not line.startswith('#'):
            d = line.strip().split()
            d1 = np.hstack([d1,float(d[0])])
            fpush = np.hstack([fpush,float(d[1])])
        if line != '\n' and not is_push and not line.startswith('#'):
            d = line.strip().split()
            d2 = np.hstack([d2,float(d[0])])
            fretrace = np.hstack([fretrace,float(d[1])])
    return d1, d2, fpush, fretrace


def CleanPath(path):
    return re.sub(r".*/(force-save.*)", r"\1", path)
radius, height = None, None

# Read file line by line
def read_vesicle_data(folder):
    '''
    Read vesicle parameters, where radius and height are expected in the text file with a '.txt' extension located at the specified folder location.
    ''' 
    radius, height, xmax, Shift = None, None, None, None # initialise variables to None as no value is loaded yet
    print(folder+"/vesicle_para.txt")
    try: 
        with open(folder+"/vesicle_para.txt", "r") as file: # opening txt file in read mode
            for line in file: # iterating over each line in the file
                key, value = line.strip().split(": ") # stripping any leading/trailing whitespaces and splitting string into key and value at ':'
                if key == "radius": # if key is 'Radius'
                    radius = float(value) # convert string value to integer and assign it to radius variable
                elif key == "height": # if key is 'Height'
                    height = float(value) # convert string value to integer and assign it to height variable
                elif key == "xmax": # if key is ''
                    xmax = float(value) # convert string value to integer and assign it to height variable
                elif key == "shift": # if key is ''
                    Shift = float(value) # convert string value to integer and assign it to height variable
            if radius is None or height is None or height is None or Shift is None: 
                raise ValueError('Both radius and height must be provided in vesicle_para.txt file') # raise error if either of them are still not defined
    except FileNotFoundError: # catch the exception if specified txt file does not exist
        print("File with vesicle parameters is not found!") 
        raise 
    except ValueError as e: # catch any other type of error related to reading or parsing the file
        print(e) 
        raise
    else: # if no exception is raised
        return radius, height, xmax, Shift # return tuple of both valuesdef read_wrong_keys(filename):

def identify_tether_filter(disps, displ, fpush, fpull):

   fil_fpl = gaussian_filter(fpull, sigma=3, order=0 )
   fil_fps = gaussian_filter(fpush, sigma=3, order=0 )

   ext_push = -1*min(np.diff(fil_fps))
   ext_pull = max(np.diff(fil_fpl))

   is_tether1 = ext_pull > 1.5*ext_push
   idx = np.where(np.diff(fil_fpl)==ext_pull)[0][0]

   return is_tether1, idx, displ[idx]

def identify_tether(disps, displ, fpush, fpull):
      fpl_l0 = fpull[displ<0]
      fpl_g0 = fpull[displ>0]

      fps_l0 = fpush[disps<0]
      fps_g0 = fpush[disps>0]

      dpsl0 = disps[disps<0]
      dpsg0 = disps[disps>0]

      dpll0 = displ[displ<0]
      dplg0 = displ[displ>0]

      ext_push = -1*min(np.diff(fps_g0[::2]))
      ext_pull = max(np.diff(fpl_g0[::2]))

      is_tether1 = ext_pull > 1.5*ext_push

      ext_push = -1*min(np.diff(fps_l0))
      ext_pull = max(np.diff(fpl_l0))

      is_tether2 = ext_pull > 1.8*ext_push

      return is_tether1, is_tether2

def trunc_fd(push, pull):
    """
    push pull: are the pd data for certain keys
    pull curve hovers over the starting point a lot. It truncates the pull curve
    returns: force-push, force-pull, push_d, pull_d
    """
    fpush, fpull = np.asarray(push[1]), np.asarray(pull[1])
    disps, displ = np.asarray(push[0]), np.asarray(pull[0])
    fpull = fpull[0:len(fpush)]
    displ = displ[0:len(fpush)]
    return fpush, fpull, -disps, -displ

def teth_keys(df_push, df_pull):
    key_l0, key_g0, ind_jl0, ind_jg0 = [], [], [], []
    for a in df_push.keys():
        fpush, fpull, disps, displ = trunc_fd(df_push[a], df_pull[a])
        # tl0, tg0 = identify_tether(-disps, -displ, fpush, fpull)
        tl0, idx, xx_t  = identify_tether_filter(disps, displ, fpush, fpull)
        if(tl0):
          if(xx_t < 0.0):
              key_l0.append(a)
              ind_jl0.append(idx)
          if(xx_t > 0.0):
              key_g0.append(a)
              ind_jg0.append(idx)

    return key_l0, key_g0, ind_jl0, ind_jl0

def get_ftether(key, idx,  push, pull, fig_tit, fig_key, toplot):
    fth, dth = [], []
    nano = 1e9
    i = 0;
    if(toplot):
      fig, ax = plt.subplots()
      norm = matplotlib.colors.Normalize(vmin = 0,
             vmax = len(key))
    for idx, a in zip(idx, key):
      fpush, fpull, dpush, dpull = trunc_fd(push[a], pull[a])
      dn, fpln = dpull[:idx+2], fpull[:idx+2]
      pdn, pfpln = dpull[:idx+20], fpull[:idx+20]
      fpln = fpln[dn < 0]
      dn = dn[dn < 0]
      pfpln = pfpln[pdn < 0]
      pdn = pdn[pdn < 0]
      nk = len(dn)-1
      if(len(dn) > 2):
        m, c = np.polyfit(dn[:-2], fpln[:-2], 1)
        if(abs(m) < 0.05):
          fth.append(fpln[nk] - fpln[nk-2])
          dth.append(dn[nk-2])
          i = i + 1;
          if(toplot):
            rgba = clr_b.viridis(norm(i), bytes=False)
            rgba_hex = matplotlib.colors.rgb2hex(rgba)
            fil_fpl = gaussian_filter(fpull, sigma=3, order=0 )
            fil_d = gaussian_filter(dpull, sigma=3, order=0 )
            ax.plot(fil_d*nano, fil_fpl*nano, '-', color=rgba_hex)
    if(toplot):
      ax.set(xlabel='Indentation (nm)', ylabel = 'Force (nN)')
      ax.set(xlim=[-70.0,10.], ylim=[-0.2,0.2], title=fig_tit)
      if(i>0): fig.savefig('teth_'+fig_key+'_'+fig_tit+'.png')
      plt.close()
    return np.asarray(fth), np.asarray(dth)

def stacked_force_dis(push, pull, keys):
    dpush, dpull = np.asarray([]), np.asarray([])
    fpush, fpull = np.asarray([]), np.asarray([])
    for a in keys:
        tfpush, tfpull, tdpush, tdpull = trunc_fd(push[a], pull[a])
        dpush = np.hstack([dpush, tdpush])
        dpull = np.hstack([dpull, tdpull])
        fpush = np.hstack([fpush, tfpush])
        fpull = np.hstack([fpull, tfpull])
    return dpush, dpull, fpush, fpull

def spring(x, K, H, C):
  return K*x*(1.0 + (H*x)**2 + (H*x)**4 ) + C
