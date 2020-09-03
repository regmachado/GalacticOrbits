from __future__ import print_function
import random

#
# 1. Create a sample of initial conditions within arbitrary ranges
#

ic = open('ic.txt', 'w+')
ic.write("# x    y    z    vx    vy    vz\n")
ic.write("# (kpc)          (km/s)        \n")

Nsample = 4

for i in range(0, Nsample):
    
    x  =   5.0 * random.random() + 5.0
    y  =   0.0
    z  =   5.0 * random.random()
    vx =  20.0 * random.random() 
    vy = 200.0 * random.random()
    vz =  20.0 * random.random()

    ic.write("%f\t%f\t%f\t%f\t%f\t%f\t\n" % (x, y, z, vx, vy, vz) )

ic.close()

print("Created %d initial conditions." % Nsample)
