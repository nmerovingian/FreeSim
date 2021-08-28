from concurrent.futures import ProcessPoolExecutor
import os
from simulation import simulation,simulation_series
import numpy as np
import itertools

np.random.seed(0)

def foo(a0,a1,a2):
    #print(a0,a1,a2)
    print('executed')
     



if __name__ == "__main__":
    
    
    variables1 = np.array([5e-3]) # SCAN RATE, V/s
    variables2 = np.logspace(-3,-7,num=50) #keq M
    variables3 = np.logspace(0,8,num=100)#kf, /s
    variables4 = np.array([1e-5]) #K0， m/s
    variables5 = np.array([1.0]) #alpha, dimensionless 
    variables6 = np.array([[0.01,0.015,0.02,0.025,0.03,0.035,0.04]]) #bulk concentrtaion of acetic acid 
    directory  = np.array(['./Series Learning'])
    commands = list(itertools.product(variables1,variables2,variables3,variables4,variables5,variables6,directory))
    commands = [(variables1,variables2,variables3,variables4,variables5,variables6,directory) for (variables1,variables2,variables3,variables4,variables5,variables6,directory) in commands if variables3/variables2 < 1e9 ]
    
    
    """
    variables1 = np.array([5e-3]) # SCAN RATE, V/s
    variables2 = np.array([5e-5]) #keq M
    variables3 = np.array([1e5])#kf, /s
    variables4 = np.array([1e-6,1e-5,1e-4,1e-3,1e-2,1e-1]) #K0， m/s
    variables5 = np.array([1.0]) #alpha, dimensionless 
    variables6 = np.array([1e-2]) #bulk concentrtaion of acetic acid 
    directory  = ['./k0'] 
    commands = list(itertools.product(variables1,variables2,variables3,variables4,variables5,variables6,directory))
    """
    commands = [(i,*commands[i]) for i in range(len(commands))]
    np.random.shuffle(commands)
    
    print(type(commands[0]),len(commands),commands[0])

    
    
    with ProcessPoolExecutor(max_workers=19) as executor:

        executor.map(simulation_series,commands)
    
    print('\a')
    
    
    

