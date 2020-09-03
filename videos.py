from __future__ import print_function
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
import os

#
# 4. Create videos with a dark background
#

#From initial conditions
xlist,   = np.loadtxt('ic.txt', unpack=True, usecols=(0,), ndmin=2)
Nsamples = len(xlist)

#Loop over particles
for k in range(0, Nsamples):
    
    k4 = '{:04d}'.format(k)

    #Read coordinates
    time, x, y, z, vx, vy, vz = np.loadtxt('output/orbit_%s.txt' % k4, unpack=True)
    
    #Downsample
    step = 5
    x  = x[::step]
    y  = y[::step]
    z  = z[::step]
    vx = vx[::step]
    vy = vy[::step]
    vz = vz[::step]

    #Create figure
    fig = plt.figure()
    
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    
    color = colors[ k % len(colors) ] 

    fig.set_size_inches(3.0*0.9, 4.0*0.9)

    plt.style.use('dark_background')
    
    #Face-on frame
    ax1 = fig.add_subplot(211)
    ax1.set_aspect('equal')

    lw = 0.6

    line, = ax1.plot([],[], lw=lw, c=color)

    ax1.set_xlim(-10, 10)
    ax1.set_ylim(-10, 10)

    ax1.tick_params( axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False, labelleft=False)
    
    ax1.spines['bottom'].set_color('gray')
    ax1.spines['top'].set_color('gray') 
    ax1.spines['right'].set_color('gray')
    ax1.spines['left'].set_color('gray')

    #Edge-on frame
    ax2 = fig.add_subplot(212)
    ax2.set_aspect('equal')

    line2, = ax2.plot([], [], lw=lw, c=color)

    ax2.set_xlim(-10, 10)
    ax2.set_ylim(-4, 4)

    ax2.tick_params( axis='both', which='both', bottom=False, top=False, left=False, labelbottom=False, labelleft=False)
    
    ax2.spines['bottom'].set_color('gray')
    ax2.spines['top'].set_color('gray') 
    ax2.spines['right'].set_color('gray')
    ax2.spines['left'].set_color('gray')
    
    def animate(i):
        line.set_xdata(x[:i])
        line.set_ydata(y[:i])
        line2.set_xdata(x[:i])
        line2.set_ydata(z[:i])
        return line, line2

    ani = animation.FuncAnimation(fig, animate, frames=len(x), fargs=None, interval=1, blit=True)

    plt.subplots_adjust(left=0.05, bottom=-0.28, right=0.95, top=1.08, wspace=0.0, hspace=-0.48)

    if not os.path.exists('videos'):
        os.makedirs('videos')
        
    print( 'Creating videos/orbit_%s.mp4 ... ' % k4 )

    ani.save('videos/orbit_%s.mp4' % k4, writer='ffmpeg', fps=24, dpi=250)
