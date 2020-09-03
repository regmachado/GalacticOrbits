from __future__ import print_function
import numpy as np
import os

#
# 2. Given a sample of initial conditions, integrate the orbits
#

#Read list of initial conditions
if not os.path.isfile('ic.txt'):
    print( 'File not found: ic.txt' )
    exit(0)
else:
    x_list, y_list, z_list, vx_list, vy_list, vz_list = np.loadtxt('ic.txt', unpack=True, ndmin=2)

Nsample = len(x_list)

#System of units 
#[L] = kpc
#[M] = 1e10Msun
#[V] = km/s
#[T] = 0.98 Gyr
G    = 43007.1

#Halo parameters
Mh = 25.0 #1e10Msun
ah = 50.0 #kpc

#Disk parameters
Md =  5.0 #1e10Msun
A  =  1.0 #kpc
B  =  0.5 #kpc

#Accelerations due to the halo potential (Hernquist)
def AccelHalo_x(x,y,z):
    r = np.sqrt(x**2+y**2+z**2)
    return -G*Mh / (r+ah)**2 * x/r

def AccelHalo_y(x,y,z):
    r = np.sqrt(x**2+y**2+z**2)
    return -G*Mh / (r+ah)**2 * y/r

def AccelHalo_z(x,y,z):
    r = np.sqrt(x**2+y**2+z**2)
    return -G*Mh / (r+ah)**2 * z/r

#Accelerations due to the disk potential (Miyamoto-Nagai)
def AccelDisk_x(x,y,z):
    Z  = A + np.sqrt(z**2+B**2)
    RR = np.sqrt(x**2+y**2+Z**2)
    return -G*Md * x / RR**3

def AccelDisk_y(x,y,z):
    Z  = A + np.sqrt(z**2+B**2)
    RR = np.sqrt(x**2+y**2+Z**2)
    return -G*Md * y / RR**3

def AccelDisk_z(x,y,z):
    Z  = A + np.sqrt(z**2+B**2)
    RR = np.sqrt(x**2+y**2+Z**2)
    return -G*Md * Z / np.sqrt(z**2+B**2) * z / RR**3

#Total accelerations
def Accelerations(x,y,z):
    ax = AccelHalo_x(x,y,z) + AccelDisk_x(x,y,z)
    ay = AccelHalo_y(x,y,z) + AccelDisk_y(x,y,z)
    az = AccelHalo_z(x,y,z) + AccelDisk_z(x,y,z)
    return ax, ay, az

#Loop over particles
for k in range(0, Nsample):
    
    k4 = '{:04d}'.format(k)
   
    #Prepare output directory
    if not os.path.exists('output'):
        os.makedirs('output')
        
    #Prepare output file
    outputfile = open('output/orbit_%s.txt' % k4, 'w+')
    outputfile.write('#t    x    y    z    vx    vy    vz\n')
    outputfile.write('#(Gyr)   (kpc)           (km/s)    \n')
    
    #Initial conditions of particle k
    x  =  x_list[k]
    y  =  y_list[k]
    z  =  z_list[k]
    vx = vx_list[k]
    vy = vy_list[k]
    vz = vz_list[k]

    #Time steps
    tstart =  0.0   #Gyr
    tstop  = 10.0   #Gyr
    dt     =  0.001 #Gyr
    Nsteps = int((tstop-tstart)/dt)

    #Output frequency
    SaveEvery = 1

    #Initial accelerations
    ax, ay, az = Accelerations(x, y, z)

    #Time integration (Leapfrog)
    for i in range (0, Nsteps+1):
        
        #Current time        
        time = tstart + i * dt
        
        #Advance positions
        x_new = x + vx * dt + 0.5 * ax * dt**2
        y_new = y + vy * dt + 0.5 * ay * dt**2
        z_new = z + vz * dt + 0.5 * az * dt**2
        
        #Store previous accelerations
        ax_old = ax
        ay_old = ay
        az_old = az
        
        #Compute current accelerations
        ax_new, ay_new, az_new = Accelerations(x_new, y_new, z_new)
        
        #Advance velocities
        vx_new = vx + 0.5 * (ax_old + ax_new) * dt
        vy_new = vy + 0.5 * (ay_old + ay_new) * dt
        vz_new = vz + 0.5 * (az_old + az_new) * dt
        
        #Update coordinates
        x  =  x_new
        y  =  y_new
        z  =  z_new
        vx = vx_new
        vy = vy_new
        vz = vz_new
        ax = ax_new
        ay = ay_new
        az = az_new
        
        #Write output
        if( i % SaveEvery == 0 ):
            outputfile.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t\n" % (time, x, y, z, vx, vy, vz) )
            print( "Particle %s : saved coordinates at t=%f Gyr" % (k, time) )

    outputfile.close()
