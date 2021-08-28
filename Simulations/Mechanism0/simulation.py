import numpy as np
import time
from coeff import Coeff
from grid import Grid
import csv
import scipy
from scipy import sparse
from scipy.sparse import linalg
import sympy
import time
import os
import math
from matplotlib import pyplot as plt
# the total concentration of X added before any chemical equilibrium happen 
cRef=1.0 # reference concentration, 1M
P0 = 1.0 # reference pressure, 1 bar
dElectrode = 2.0*5e-6 / math.pi
KH_2 = 1292  # Henry law constant for H2
E0f = 0.142 # The formal potential of H+/H2 couple

DA = 1e-9
DB = 1e-9
DC = 1e-9
DY = 1e-9
DZ = 1e-9
Dref = 1e-9

def simulation_series(commands:tuple):
    index,variable1,variable2,variable3,variable4,variable5,variables6,directory = commands

    for variable6 in variables6:
        simulation((index,variable1,variable2,variable3,variable4,variable5,variable6,directory))



def simulation(commands:tuple)->None:
    index,variable1,variable2,variable3,variable4,variable5,variable6,directory = commands

    #variable4 is K0, variable5 is alpha, variable6 are reserved. 

    if not os.path.exists(directory):
        os.mkdir(directory)
    directory = f'{directory}/{index}'
    if not os.path.exists(directory):
        os.mkdir(directory)


    dimScanRate = variable1
    sigma = dElectrode*dElectrode/Dref*(96485/(8.314*298)) *dimScanRate
    

    #start and end potential of voltammetric scan
    theta_i = 20
    theta_v = -20

    cycles = 2
    #space step
    deltaX = 1e-5
    #potential step
    deltaTheta = 1e-2
    #expanding grid factor
    gamma = 0.06

    nTimeSteps_cycles = int(2*np.fabs(theta_v-theta_i)/deltaTheta)*cycles
    nTimeSteps = int(2*np.fabs(theta_v-theta_i)/deltaTheta)
    Esteps = np.arange(nTimeSteps,dtype=np.float64)
    E = np.where(Esteps<nTimeSteps/2.0,theta_i-deltaTheta*Esteps,theta_v+deltaTheta*(Esteps-nTimeSteps/2.0))
    E = np.tile(E,cycles)





    # standard electrochemical rate constant. Only useful if using Butler-Volmer equation for boundary conditions
    k0 = variable4
    K0 = k0*dElectrode / Dref
    alpha = variable5

 


    concA = 1.0
    concB = 0.0
    concC = 0.0
    concZ = 0.0
    concY = 0.0

    print(f"concA {concA}, concB{concB}, concY {concY}, concZ {concZ}")

    # dimensionless diffusion coefficients of every species
    dA =DA/Dref
    dB =DB/Dref   # diffusion coefficient of H+
    dC =DC/Dref
    dY =DY/Dref  # diffusion coeffficient of acetate+
    dZ =DZ/Dref    # diffusion coefficient of H_2 

    # the maximum number of iterations for Newton method
    number_of_iteration = 10

    deltaT = deltaTheta/sigma
    print('sigma',sigma,'DeltaT',deltaT)
    # The maximum distance of simulation
    maxT = 2.0*abs(theta_v-theta_i)/sigma
    maxX = 6.0 * np.sqrt(maxT)



    # create the csv file to save data
    CVLocation  = f'{directory}/var1={variable1:.4E}var2={variable2:.4E}var3={variable3:.4E}var4={variable4:.4E}var5={variable5:.2E}var6={variable6:.2E}.txt'

    if os.path.exists(CVLocation):
        print(F'{CVLocation} File exists, skipping!')
        #return
    coeff = Coeff(deltaT,maxX,K0,alpha,gamma,dA,dB,dC,dY,dZ)
    coeff.calc_n(deltaX)

    #simulation steps


    # initialzie matrix for Coeff object
    coeff.ini_jacob()
    coeff.ini_fx()
    coeff.ini_dx()
    # initialze matrix for Grid objectd
    grid = Grid(coeff.n)
    grid.grid(deltaX,gamma)
    grid.init_c(concA,concB,concC,concY,concZ,theta_i)

    coeff.get_XX(grid.x)
    coeff.update(grid.conc,concA,concB,concC,concY,concZ)
    coeff.Allcalc_abc(deltaT,theta_i,deltaX)
    coeff.calc_jacob(grid.conc,theta_i)
    coeff.calc_fx(grid.conc,theta_i)

    # use spsolve for sparse matrix for acceleration
    coeff.dx = linalg.spsolve(sparse.csr_matrix(coeff.J),sparse.csr_matrix(coeff.fx[:,np.newaxis]))

    coeff.xupdate(grid.conc,theta_i)

    for i in range(number_of_iteration):
        coeff.calc_jacob(grid.conc,theta_i)

        coeff.calc_fx(grid.conc,theta_i)
        print(coeff.fx[:10])

        coeff.dx = linalg.spsolve(sparse.csr_matrix(coeff.J),sparse.csr_matrix(coeff.fx[:,np.newaxis]))
        grid.conc = coeff.xupdate(grid.conc,theta_i)
        if np.mean(np.absolute(coeff.dx)) < 1e-12:
            #print('Exit: Precision satisfied!')
            break
    

    
    
    f=open(CVLocation,mode='w')


    f.write(f'{E[0]},{grid.grad()}\n')
    Theta = theta_i

    start_time = time.time()

    for index in range(1,len(E)):
        Theta = E[index]
        

        #Theta  = Theta + deltaTheta
        
        if index == 2:
            print(f'Total run time is {(time.time()-start_time)*len(E)/60/2:.2f} mins')


        coeff.update(grid.conc,concA,concB,concC,concY,concZ)
        coeff.Allcalc_abc(deltaT,Theta,deltaX)
        for ii in range(number_of_iteration):
            coeff.calc_jacob(grid.conc,Theta)
            coeff.calc_fx(grid.conc,Theta)
            try:
                #coeff.dx = np.linalg.solve(coeff.J,coeff.fx)
                #coeff.dx = scipy.linalg.solve_banded((4,4),coeff.J,coeff.fx)
                coeff.dx=linalg.spsolve(sparse.csr_matrix(coeff.J),sparse.csr_matrix(coeff.fx[:,np.newaxis]))
            except:
                print("Using lstsq solver! ")
                coeff.dx = np.linalg.lstsq(coeff.J,coeff.fx,rcond=None)[0]
            grid.conc = coeff.xupdate(grid.conc,Theta)

            if np.mean(np.absolute(coeff.dx)) < 1e-12:
                #print(f'Exit: Precision satisfied!\nExit at iteration {ii}')
                break
            
        if not np.isnan(grid.grad()):
            f.write(f'{Theta},{grid.grad()}\n')
        else:
            print('Bad solution')




    f.close()
    
    #When task completed, send an email

    #sendMail("Task completed",f"var1={variable1},var2={variable2},var3={variable3}")

        


    


    













if __name__ == "__main__":
    simulation((305, 0.005, 0.0003906939937054617, 100000000.0, 1e-05, 1.0, 0.1, './Trash'))
    

    


