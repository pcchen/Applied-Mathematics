#!/usr/bin/env python
# -*- coding: UTF-8 -*-

## Poisson -> (laplacian) V = rho/epislion
## ref: http://www.physics.buffalo.edu/phy410-505/topic6/index.html
## numerical only
## charge in [1,1]

import numpy as np

L=10

length = L                   # the number of interior points of x,y
V = np.zeros((L+2,L+2))      # potential to be found. Size =(L+2,L+2)
V_new = np.zeros((L+2,L+2))  # new potential after each stop
rho = np.zeros((L+2,L+2))    # given charge density

X = np.arange(0,L)
Y = np.arange(0,L)
X,Y = np.meshgrid(X,Y)

h = 1/(L+1)             # lattice spacing
q = 10.0                # point charge
#ct = (L+2)/2           # center of lattice
rho[1,1] = q/(h*h)      # charge density

steps = 0               # number of iteration steps
error = 0

def Jacobi():
        for i in range(1,L+1):
            for j in range(1,L+1):
                V_new[i,j]= 0.25 * ( V[i-1,j] + V[i+1,j] + V[i,j-1] + V[i,j+1] + h*h*rho[i,j])

def error_es():
        global error,V_new,V
        n = 0 # number of non-zero differences
        for i in range(L):
            for j in range(L):
                if (V_new[i][j] != 0):
                    if (V_new[i,j] != V[i,j]):
                        error += abs(1-V[i,j]/V_new[i,j])
                        n+=1
                        V = V_new
                if (n != 0):
                    error = error/n

while True:
          error = 0
          Jacobi()
          error_es()
          #print(error)
          if error < 1.e-2:
              break

print(V_new,error)
