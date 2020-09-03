from __future__ import print_function
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import os

#
# 4. Create 3D videos
#

#From initial conditions
xlist,   = np.loadtxt('ic.txt', unpack=True, usecols=(0,), ndmin=2)
Nsamples = len(xlist)

#Loop over particles
for k in range(0, Nsamples):
    
    k4 = '{:04d}'.format(k)

    #Read coordinates
    time, x, y, z, vx, vy, vz = np.loadtxt('output/orbit_%s.txt' % k4, unpack=True)
    
    Ntimes = len(time)-1
    
    step = 50

    for i in range(0, Ntimes, step):

        print('Creating videos3D/video3_%s.mp4 : %d/%d' % (k4, i, Ntimes))        

        #Create figure            
        fig = plt.subplots(nrows=1, ncols=1, figsize=(6.0, 6.0))

        L     = 10.0
        lw    = 0.8
        alpha = 0.8
        color = 'tab:blue'

        #Face-on frame
        ax = plt.subplot(111, projection='3d')
        ax.set_aspect('equal')
        
        ax.plot(x[0:i], y[0:i], z[0:i], lw=lw, c=color, alpha=alpha)
            
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
        if not os.path.exists('videos3D/tmp/'):
            os.makedirs('videos3D/tmp/')

        #Save figures
        i5 = '{:05d}'.format(i/step)
        plt.savefig('videos3D/tmp/plot_%s.png' % i5, bbox_inches='tight', dpi=180)
        plt.close()

    #Create video        
    command = 'ffmpeg -y -framerate 12 -i videos3D/tmp/plot_' + '%05d' + '.png -c:v libx264 -vf format=yuv420p videos3D/video3_%s.mp4 >/dev/null 2>&1' % (k4)
    os.system(command)
    
    #Clean figures
    command = 'rm videos3D/tmp/plot_*.png'
    os.system(command)
