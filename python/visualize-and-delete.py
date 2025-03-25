import sys
import numpy as np
import os as os
import glob as glob
import matplotlib.pyplot as plt
import matplotlib
import lib as lib
import matplotlib.cm as clr_b

nano = 1e9

def TimePlot(ax1, ax2, files):
   for i, f in enumerate(files):
      rgba = clr_b.viridis(norm(i), bytes=False)
      rgba_hex = matplotlib.colors.rgb2hex(rgba)

def plot_file(file_path, rgb_hex):
    """ Function to read and plot a file """
    try:
       d1, d2, fpush, fretrace = lib.ReadSingleFile(file_path);
       # plot the push curve;
       d = np.asarray(d1)*nano
       force = np.asarray(fpush)*nano
       plt.clf()  # Clear previous plot
       plt.plot(-d, force, '-', color=rgba_hex)
       plt.axvline(ls=":", color="k")
       plt.axhline(ls=":", color="k")
       plt.title(f"Viewing: {os.path.basename(file_path)}")
       plt.pause(0.1)  # Pause to allow rendering
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Loop through files
folder = sys.argv[1]
files = lib.ReadFromFolder(folder)

numkey = len(files)
norm = matplotlib.colors.Normalize(vmin = 0,
           vmax = numkey)

i = 0
while i < len(files):
    rgba = clr_b.viridis(norm(i), bytes=False)
    rgba_hex = matplotlib.colors.rgb2hex(rgba)
    plot_file(files[i], rgba_hex)

    print(f"Showing: {files[i]}")
    print("[n] Next | [d] Delete | [q] Quit")

    key = input("Enter choice: ").strip().lower()

    if key == 'd':  # Delete the file
        os.remove(files[i])
        print(f"Deleted {files[i]}")
        files.pop(i)  # Remove from list without incrementing i

    elif key == 'n':  # Skip to the next file
        i += 1

    elif key == 'q':  # Quit
        print("Exiting...")
        break
    else:
        print("Invalid key, try again.")

plt.close()
