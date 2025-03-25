import sys
import numpy as np
import glob as glob
import matplotlib.pyplot as plt
import matplotlib
import lib as lib
import matplotlib.cm as clr_b

nano = 1e9
folder = sys.argv[1]
files = lib.ReadFromFolder(folder)

def TimePlot(ax1, ax2, files):
   numkey = len(files)
   norm = matplotlib.colors.Normalize(vmin = 0,
        vmax = numkey)
   for i, f in enumerate(files):
      rgba = clr_b.viridis(norm(i), bytes=False)
      rgba_hex = matplotlib.colors.rgb2hex(rgba)
      d1, d2, fpush, fretrace = lib.ReadSingleFile(f);
      # plot the push curve;
      d = np.asarray(d1)*nano
      force = np.asarray(fpush)*nano
      ax1.plot(-d, force, '-', color=rgba_hex)
      d = np.asarray(d2)*nano
      force = np.asarray(fretrace)*nano
      ax2.plot(-d, force, '-', color=rgba_hex)

fig, ax1 = plt.subplots()
fig, ax2 = plt.subplots()
TimePlot(ax1, ax2, files)
for xx in [ax1, ax2]:
    xx.set(xlabel="Indentation (nm)", ylabel="Force (nN)")
plt.show()



# def determine_KA(fol):
#     K_ = []; 
#     df_push = pd.read_pickle(fol+"/force_push.pkl")
#     for i, a in enumerate(df_push.keys()):
#        d = -1*np.asarray(df_push[a][0])
#        force = np.asarray(df_push[a][1])
#        am = d > 0 
#        au = d < 2e-8
#        mask = am & au
#        m1, c1 = np.polyfit(d[mask], force[mask], 1)
#        K_.append(m1)

#     return np.asarray(K_)




# def make_data_frame(fol):
#      df_push, tmp_df = pd.DataFrame({}), pd.DataFrame({})
#      df_pull, tmp_df = pd.DataFrame({}), pd.DataFrame({})
#      d1, d2, fpush, fretrace = lib.read_file(files[0]);
#      char = "%04d" %(0)
#      df_push[char] = np.vstack([d1, fpush]).tolist()
#      df_pull[char] = np.vstack([d2, fretrace]).tolist()
#      for i, f in enumerate(files[1:]):
#          char = "%04d" %(i+1)
#          dt1, dt2, ftpush, ftretrace = lib.read_file(f);
#          tmp_df = pd.DataFrame()
#          tmp_df[char] = np.vstack([dt1, ftpush]).tolist()
#          df_push = pd.concat([df_push, tmp_df], axis=1)
#          tmp_df = pd.DataFrame()
#          tmp_df[char] = np.vstack([dt2, ftretrace]).tolist()
#          df_pull = pd.concat([df_pull, tmp_df], axis=1)

#      df_push.to_pickle(fol+'/force_push.pkl')
#      df_pull.to_pickle(fol+'/force_pull.pkl')


# make_data_frame(folder)
# plotStore(folder)

#KA = determine_KA(folder)

# fig, ax = plt.subplots()
# ax.plot(KA, 'o')
# ax.axhline(np.mean(KA), ls='--', color="k")
# ax.axhline(np.mean(KA) + np.std(KA)/2, ls='--', color='k')
# ax.axhline(np.mean(KA) - np.std(KA)/2, ls='--', color='k')
# ax.set(ylim=[0.002, 0.010], xlim=[20,80])
# print(np.std(KA)/2)
# plt.show()
# ax.hist(KA, bins=32)
# plt.show()
