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
    variables2 = np.array([0.0]) # kf
    variables3 = np.array([0.0]) # kb, s^-1
    variables4 = np.array([1e-8]) # k0, standard electrochemical rate constant, m/s
    variables5 = np.array([0.5]) #alpha 
    variables6 = np.array([0.0]) # reserved
    kinetics = np.array(['BV'])
    diffusion_mode  = np.array(['linear'])
    mechanism  = np.array([6])  # possible value includes 0,3,4,5,6
    directory  = np.array(['./Trash'])

    commands = list(itertools.product(variables1,variables2,variables3,variables4,variables5,variables6,kinetics,diffusion_mode,mechanism,directory))

    
    
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
    np.random.shuffle(commands)
    
    print(type(commands[0]),len(commands),commands[0])

    
    
    with ProcessPoolExecutor(max_workers=18) as executor:
        executor.map(simulation,commands)
    
    print('\a')
    
    
    

