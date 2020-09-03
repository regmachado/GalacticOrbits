from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
import os

#
# 3. Make face-on and edge-on plots
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
    fig = plt.subplots(nrows=2, ncols=1, figsize=(7.5, 3.0))

    L     = 10.0
    lw    = 0.5
    alpha = 0.7
    color = 'tab:blue'

    #Face-on frame
    ax1 = plt.subplot(121)
    ax1.set_aspect('equal')

    ax1.plot(x, y, lw=lw, c=color, alpha=alpha)

    ax1.set_xlim(-L, L)
    ax1.set_ylim(-L, L)

    ticks = np.arange(-10,15,5)
    ax1.set_xticks(ticks)
    ax1.set_yticks(ticks)

    ax1.set_xlabel('$x$ (kpc)')
    ax1.set_ylabel('$y$ (kpc)')
    
    #Edge-on frame
    ax2 = plt.subplot(122)
    ax2.set_aspect('equal')

    ax2.plot(x, z, lw=lw, c=color, alpha=alpha)

    ax2.set_xlim(-L, L)
    ax2.set_ylim(-L, L)

    ticks = np.arange(-10,15,5)
    ax2.set_xticks(ticks)
    ax2.set_yticks(ticks)
    
    ax2.set_xlabel('$x$ (kpc)')
    ax2.set_ylabel('$z$ (kpc)')

    #Directory to save figures
    if not os.path.exists('plots'):
        os.makedirs('plots')

    #Save figures
    plt.savefig('plots/plot_%s.png' % k4, bbox_inches='tight', dpi=250)
    plt.close()

    print( 'Saved plots/plot_%s.png' % k4 )
    
