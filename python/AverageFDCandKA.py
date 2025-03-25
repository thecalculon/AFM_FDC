import sys
import numpy as np
import glob as glob
import matplotlib
import lib as lib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



nano = 1e9
folder = sys.argv[1]
files = lib.ReadFromFolder(folder)

def AverageFdcandKA(files):
   d1, d2, fpush, fretrace = lib.ReadSingleFile(files[0]);
   x_fixed = np.linspace(-20/nano, (max(-d1)-5.0/nano), 100)  # Fixed grid
   Favg = np.zeros(len(x_fixed))
   K_ = []
   for i, f in enumerate(files):
      d1, d2, fpush, fretrace = lib.ReadSingleFile(f);
      interp_func = interp1d(-d1, fpush, kind='linear', fill_value="extrapolate")
      # ax.plot(-d1*nano, fpush*nano, color='yellow')
      f_fixed = interp_func(x_fixed)
      Favg += f_fixed
      am = -d1 > 0 
      au = -d1 < 2e-8
      mask = am & au
      m1, c1 = np.polyfit(-d1[mask], fpush[mask], 1)
      K_.append(m1)
   return x_fixed, Favg/len(files), np.asarray(K_)

# fig, ax = plt.subplots()

x, y, K_ = AverageFdcandKA(files) 
np.savetxt(folder+"/AverageFDC.txt", np.vstack([x,y]).T, fmt="%.5e")
fstripped = np.asarray([lib.CleanPath(f) for f in files])
np.savetxt(folder+"/Forcefile.txt", fstripped, fmt="%s")
np.savetxt(folder+"/KA.txt", K_, fmt="%.5e")
# print(fstripped)
# with open  
# ax.plot(x*nano, y*nano, '-r', linewidth=2)
# plt.show()


