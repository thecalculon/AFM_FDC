import numpy as np
import pandas as pd
import numpy.linalg as la
import glob
import lib as lib
from scipy.optimize import curve_fit
import sys as sys
import os
import matplotlib.pyplot as plt

#################################################################
frcecomp=False
onebynano=1e9
onebypico=1e12
theta=0.26
radius_ev=84.38029625e-9
#################################################################


def cost(xx,ka,sigma):
    sigma=round(sigma,11)
    ka=round(ka,9)
    kasigma=np.array([ka,sigma])
    print(f"Performing Optimization for Ka = {ka} and sigma = {sigma}")
    t_delta,t_FF,a,b,c=lib.forcedistcurve(kasigma,np.max(xx)/(radius_ev*onebynano),
			verbose=False)
    t_delta=(t_delta-t_delta[0])*radius_ev*onebynano
    t_FF=t_FF*radius_ev*onebypico
    FF_model=np.interp(xx,t_delta,t_FF)
    return np.log10(FF_model)
#################################################################
# Let's see this later

# This is the main code that needs to work. 
# for j in range(1):
# I need to read the vesicle parameters: 

folder = sys.argv[1]
radius, height, xmax, Shift = lib.read_vesicle_data(folder)
print(radius, height, xmax, Shift)
dd = np.loadtxt(folder+"/AverageFDC.txt")
dexpt,fexpt=dd[:,0]*onebynano+Shift, dd[:,1]*onebypico
dexpt,fexpt=lib.chop2(dexpt,fexpt,min_=0,max_=xmax)
d1,fpush=dexpt,np.log10(fexpt)
popt, pcov = curve_fit(cost, d1, fpush, p0=[0.5,0.005],
    method='lm', xtol=1e-2)
print("fitted [Ka, sigma] = ",popt)
print("Error =", np.sqrt(np.dot(10**fpush-10**cost(d1,*popt),
    10**fpush-10**cost(d1,*popt))/np.dot(10**fpush,10**fpush))*100)

delta,FF,a,b,c=lib.forcedistcurve(popt,xmax/(radius_ev*onebynano), verbose=False)
np.savetxt(folder+"/SimultedMembrane.txt", np.vstack([delta,FF,a,b,c]).T, comments=f"[Ka, Sigma] = f{popt}")

'''
Plot the results.
'''
fig, ax = plt.subplots()
ax.plot(radius*(delta - delta[0]), radius*(FF), 'o', markerfacecolor='none',
        markersize=5, label='Simulated')
ax.plot(dd[:, 0]*onebynano, dd[:, 1]*onebynano, '--k', label='Experimental')
ax.set(xlabel="Indentation (nm)", ylabel="Force (nN)")
ax.legend()

'''
Plot the membrane at different indentation
The a, b, c values can also be read from folder + /SimulatedMembrane.txt
'''
fig, ax = plt.subplots()
Np = 4096
rr,zz,rrtip,zztip=lib.membrane(a[10],b[10],c[10],Np=Np)
ax.plot(rr[0:],zz[0:],'k-',linewidth=1.0)
ax.plot(-rr[4*Np-1::-1],zz[4*Np-1::-1],'k-',linewidth=1.0)
ax.plot(rrtip,zztip,'r-',linewidth=1.0)
ax.plot(-rrtip[-1::-1],zztip[-1::-1],'r-',linewidth=1.0)
ax.set_aspect('equal')
ax.spines[['right','top','left','bottom']].set_visible(False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.show()
