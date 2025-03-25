import numpy as np
import pandas as pd
import numpy.linalg as la
import glob
import lib as lib
from scipy.optimize import curve_fit
import sys as sys
import os

'''
Code to perform the optimization Here is a brief explanation of how you could
implement this in Python:
'''

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
    fname=folder+"/sigma"+str(sigma).replace(".","o")+\
    "_k"+str(ka).replace(".","o")+"_th"+\
    str(theta).replace(".","o")+".txt"
    if os.path.isfile(fname) and frcecomp==False:
        print("Taking data from "+ fname)
        dd=np.loadtxt(fname)
        t_delta,t_FF=dd[:,0],dd[:,1]
    else:
        print("generating data for Ka =", str(ka), ", sigma =", str(sigma))
        t_delta,t_FF,a,b,c=lib.forcedistcurve(kasigma,np.max(xx)/(radius_ev*onebynano),
			verbose=False)
        np.savetxt(fname,np.vstack([t_delta,t_FF,a,b,c]).T)
    t_delta=(t_delta-t_delta[0])*radius_ev*onebynano
    t_FF=t_FF*radius_ev*onebypico
    FF_model=np.interp(xx,t_delta,t_FF)
    return np.log10(FF_model)
#################################################################
# Let's see this later

# This is the main code that needs to work. 
#for j in range(1):
# I need to read the vesicle parameters: 

folder = sys.argv[1]
radius, height, shift, xmax = lib.read_vesicle_data(folder)
print(radius, height)
dd = np.loadtxt(folder+"/AverageFDC.txt")
dexpt,fexpt=dd[:,0]*onebynano+2.0, dd[:,1]*onebypico
xmax = 10.0 
dexpt,fexpt=lib.chop2(dexpt,fexpt,min_=0,max_=xmax)
d1,fpush=dexpt,np.log10(fexpt)
popt, pcov = curve_fit(cost, d1, fpush, p0=[0.5,0.005],
    method='lm', xtol=1e-2)
print("popt=",popt)
print("Error =", np.sqrt(np.dot(10**fpush-10**cost(d1,*popt),
    10**fpush-10**cost(d1,*popt))/np.dot(10**fpush,10**fpush))*100)


