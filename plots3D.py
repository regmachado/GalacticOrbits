from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import os

#
# 3. Make 3D plots
#

#From initial conditions
xlist,   = np.loadtxt('ic.txt', unpack=True, usecols=(0,), ndmin=2)
Nsamples = len(xlist)

#Loop over particles
for k in range(0, Nsamples):
    
    k4 = '{:04d}'.format(k)
    
    #Read coordinates
    time, x, y, z, vx, vy, vz = np.loadtxt('output/orbit_%s.txt' % k4, unpack=True)

    #Create figure            
    fig = plt.subplots(nrows=1, ncols=1, figsize=(6.0, 6.0))

    L     = 10.0
    lw    = 0.5
    alpha = 0.7
    color = 'tab:blue'

    #Face-on frame
    ax = plt.subplot(111, projection='3d')
    ax.set_aspect('equal')

    ax.plot(x, y, z, lw=lw, c=color, alpha=alpha)

    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_zlim(-L, L)

    ticks = np.arange(-10,15,5)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)

    ax.set_xlabel('$x$ (kpc)', fontsize=8)
    ax.set_ylabel('$y$ (kpc)', fontsize=8)
    ax.set_zlabel('$z$ (kpc)', fontsize=8)

    #Directory to save figures
    if not os.path.exists('plots3D'):
        os.makedirs('plots3D')

    #Save figures
    plt.savefig('plots3D/plot3_%s.png' % k4, bbox_inches='tight', dpi=180)
    plt.close()

    print( 'Saved plots3D/plot3_%s.png' % k4 )
    
