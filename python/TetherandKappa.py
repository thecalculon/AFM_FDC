
import sys
import numpy as np
import glob as glob
import matplotlib
import lib as lib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import matplotlib.cm as clr_b



nano = 1e9
folder = sys.argv[1]
files = lib.ReadFromFolder(folder)

def IdentifyJump(curve, X, jump):
   RelSig = curve[X>0.0]
   RelX = X[X>0.0]
   diffs = np.abs(np.diff(RelSig[::3]))
   jump_indices = np.where(diffs > jump)[0]
   has_jump = np.any(diffs > jump)
   if has_jump:
      idx = int(jump_indices[0]*2)
      m, c = np.polyfit(RelX[:idx], RelSig[:idx], 1)
      # fig, ax = plt.subplots()
      # ax.plot(RelX, RelSig, '-b')
      # ax.plot(RelX[:idx], m*RelX[:idx]+c, '-r') 
      # plt.show()
      # print("F/L ", m)
   else:
      m = 0.0
   return has_jump, m

def findFbyL(signal, d):
    """
    Find indices where the difference between consecutive values exceeds d.
    
    Parameters:
        signal (np.ndarray): Input 1D array.
        d (float): Threshold for jump detection.
        
    Returns:
        np.ndarray: Indices where jumps occur.
    """
    diffs = np.abs(np.diff(signal))
    jump_indices = np.where(diffs > d)[0] + 1  # +1 to get the index after the jump
    return jump_indices

def Smooth_1d(signal, window_size=5, sigma_spatial=2.0, sigma_intensity=0.5):
    """
    Edge-preserving smoothing of a 1D curve using a bilateral filter.
    
    Parameters:
        signal (np.ndarray): Input 1D array.
        window_size (int): Size of the smoothing window (should be odd).
        sigma_spatial (float): Standard deviation for spatial (distance) weights.
        sigma_intensity (float): Standard deviation for intensity (value) weights.
        
    Returns:
        np.ndarray: Smoothed 1D array.
    """
    half_window = window_size // 2
    smoothed = np.zeros_like(signal)
    for i in range(len(signal)):
        # Indices of the window
        left = max(i - half_window, 0)
        right = min(i + half_window + 1, len(signal))
        window = signal[left:right]
        # Spatial weights
        spatial_weights = np.exp(-0.5 * ((np.arange(left, right) - i) ** 2) / sigma_spatial ** 2)
        # Intensity weights
        intensity_weights = np.exp(-0.5 * ((window - signal[i]) ** 2) / sigma_intensity ** 2)
        # Combined weights
        weights = spatial_weights * intensity_weights
        weights /= np.sum(weights)
        smoothed[i] = np.sum(window * weights)
    return smoothed

def DetermineTether(ax1, files):
   numkey = len(files)
   norm = matplotlib.colors.Normalize(vmin = 0,
        vmax = numkey)
   FbyL = []
   for i, f in enumerate(files):
      rgba = clr_b.viridis(norm(i), bytes=False)
      rgba_hex = matplotlib.colors.rgb2hex(rgba)
      d1, d2, fpush, fretrace = lib.ReadSingleFile(f);
      # plot the push curve;
      d = np.asarray(d2)*nano
      force = np.asarray(fretrace)*nano
      Fsmooth = Smooth_1d(force, window_size=10, sigma_spatial=2.0, sigma_intensity=0.5)
      has_jump, m = IdentifyJump(Fsmooth, d, 0.02)
      if(has_jump):
         #print(f + " has tether")
         ax.plot(d[d>0], Fsmooth[d>0], '-', color=rgba_hex)
         FbyL.append(-m)
      else:
        print(f + " has no tether") 
   return np.asarray(FbyL)
fig, ax = plt.subplots()
FbyL = DetermineTether(ax, files)
ax.set(xlabel="Indentation (nm)", ylabel="Force (nN)")
plt.show()


# fig, ax = plt.subplots()

np.savetxt(folder+"/FbyL.txt",FbyL, fmt="%.5e")
# print(fstripped)
# with open  
# ax.plot(x*nano, y*nano, '-r', linewidth=2)
# plt.show()


