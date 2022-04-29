import numpy as np
import time
#from coeff import Coeff
from Simulations.Mechanism4CA.coeff import Coeff
#from grid import Grid
from Simulations.Mechanism4CA.grid import Grid
from helper import toDimensionalCA
import csv
import scipy
from scipy import sparse
from scipy.sparse import linalg
import time
import os
import math
from matplotlib import pyplot as plt
# the total concentration of X added before any chemical equilibrium happen 

P0 = 1.0 # reference pressure, 1 bar





def Mechanism_03456_simulation_single_thread_Gui(signals,input_parameters)->None:

    cRef=input_parameters.chemical_parameters_22[3]
    Dref = input_parameters.chemical_parameters_22[1]

    DA = input_parameters.chemical_parameters_22[1]
    DB = input_parameters.chemical_parameters_22[5]
    DC = input_parameters.chemical_parameters_22[9]
    DY = input_parameters.chemical_parameters_22[13]
    DZ = input_parameters.chemical_parameters_22[17]

    dElectrode = input_parameters.cv_parameters_11[1] # unit is m
    lElectrode = input_parameters.cv_parameters_11[2] # unit is m, for cylinder electrode only
    E0f = input_parameters.chemical_parameters_2[1] # The formal potential of the couple couple
    directory = input_parameters.file_options_parameters[1]
    file_name = input_parameters.file_options_parameters[2]

    if input_parameters.file_options_parameters[3] == 0:
        file_type ='.txt'
    elif input_parameters.file_options_parameters[3] == 1:
        file_type ='.csv'
    else:
        raise ValueError('Unknwon file type')
    dimensional = input_parameters.file_options_parameters[5]
    output_file_name = f'{directory}/{file_name}{file_type}'
    Temperature = input_parameters.cv_parameters_13[4]
    theta_i = (input_parameters.cv_parameters_13[0]-E0f)*96485/(8.314*Temperature)
    time_dim = input_parameters.cv_parameters_13[1]
    maxT = time_dim * Dref / (dElectrode**2)
    #space step
    deltaX = 1e-6
    #initial step
    deltaT= input_parameters.model_parameters_32[0] * Dref / (dElectrode**2)
    gammaT = input_parameters.model_parameters_32[1]

    #expanding grid factor
    gamma = input_parameters.model_parameters_31[0]


    zeta = 2 
    geometry_number = input_parameters.cv_parameters_11[0]
    # information of electrode
    if geometry_number == 0:
        diffusion_mode = 'linear'
    elif geometry_number == 1:
        diffusion_mode = 'radial'
        zeta = 2 
    elif geometry_number == 2:
        diffusion_mode = 'radial'
        zeta = 2
    elif geometry_number == 4:
        diffusion_mode = 'radial'
        zeta = 1
    else:
        raise ValueError('Unknown geometry')


    # information about electrode kinetics
    if input_parameters.chemical_parameters_2[0] == 0:
        kinetics = 'Nernst'
    elif input_parameters.chemical_parameters_2[0] == 1:
        kinetics = 'BV'
    elif input_parameters.chemical_parameters_2[0] == 2:
        kinetics = 'MH'
        raise ValueError('Marcus Harsh is an unimplemented Electrode kinetics ')
     
    else:
        raise ValueError('Unknown/Unimplemented Electrode kinetics ')
     
    mechanism = input_parameters.mechanism_parameters_0[0]
    k0 = input_parameters.chemical_parameters_2[3]


    alpha = 0.5

    if not os.path.exists(directory):
        os.mkdir(directory)





    

    #start and end potential of voltammetric scan
    dimkf = input_parameters.chemical_parameters_21[1]
    dimkb = input_parameters.chemical_parameters_21[3]
    if mechanism ==0:
        Kf = 0.0 
        Kb = 0.0
    elif mechanism == 4:
        Kf = dimkf*dElectrode*dElectrode/Dref
        Kb = dimkb*dElectrode*dElectrode/Dref
    elif mechanism ==3:
        Kf = dimkf*dElectrode*dElectrode*cRef/Dref
        Kb = dimkb*dElectrode*dElectrode/Dref
    elif mechanism == 5:
        Kf = dimkf*dElectrode*dElectrode/Dref
        Kb = dimkb*dElectrode*dElectrode/Dref
    elif mechanism == 6:
        Kf = dimkf*dElectrode*dElectrode/Dref
        Kb = dimkb*dElectrode*dElectrode*cRef/Dref
    else:
        raise ValueError









    # standard electrochemical rate constant. Only useful if using Butler-Volmer equation for boundary conditions

    K0 = k0*dElectrode / Dref


 


    concA = input_parameters.chemical_parameters_22[3]/cRef
    concB = input_parameters.chemical_parameters_22[7]/cRef
    concC = input_parameters.chemical_parameters_22[11]/cRef
    concY = input_parameters.chemical_parameters_22[15]/cRef
    concZ = input_parameters.chemical_parameters_22[19]/cRef

    print(f"concA {concA}, concB{concB}, concY {concY}, concZ {concZ}")

    # dimensionless diffusion coefficients of every species
    dA =DA/Dref
    dB =DB/Dref   
    dC =DC/Dref
    dY =DY/Dref  
    dZ =DZ/Dref    

    # the maximum number of iterations for Newton method
    number_of_iteration = int(input_parameters.model_parameters_30[1])




    if diffusion_mode == 'linear':
        maxX = 6.0 * np.sqrt(maxT)
    elif diffusion_mode =='radial':
        maxX = 1.0 +  6.0 * np.sqrt(maxT)

    

    coeff = Coeff(deltaT,maxX,kinetics,diffusion_mode,zeta,K0,Kf,Kb,alpha,gamma,dA,dB,dC,dY,dZ,mechanism)
    coeff.calc_n(deltaX)
    coeff.calc_time_steps(maxT,deltaT,gammaT)

    #simulation steps


    # initialzie matrix for Coeff object
    coeff.ini_jacob()
    coeff.ini_fx()
    coeff.ini_dx()
    # initialze matrix for Grid objectd
    grid = Grid(coeff.n,diffusion_mode,coeff.nT)
    grid.grid(deltaX,deltaT,gamma,gammaT)
    print('Time step',len(grid.t))
    grid.init_c(concA,concB,concC,concY,concZ,theta_i)

    coeff.get_XX(grid.x)
    

    
    


    start_time = time.time()

    for index in range(1,len(grid.t)):
        deltaT = grid.t[index] - grid.t[index-1]
        if len(grid.t)> 100:
            if index%int(len(grid.t)*0.01) ==0:
                progress =index/len(grid.t)
                signals.progress.emit(int(progress*100))
                if input_parameters.ViewOption[1]:
                    grid.updateAll()
                    ConcProfile = grid.packageAllConc()
                    ConcProfile[:,0] *= dElectrode
                    ConcProfile[:,1:] *= cRef
                    signals.concProfile.emit(ConcProfile)

        Theta = theta_i
        
        
        if index == 2:
            print(f'Total run time is {(time.time()-start_time)*len(grid.t)/60:.2f} mins')


        coeff.update(grid.conc,concA,concB,concC,concY,concZ)
        coeff.Allcalc_abc(deltaT,Theta,deltaX,mode=diffusion_mode)
        for ii in range(number_of_iteration):
            coeff.calc_jacob(grid.conc,Theta,Kf,Kb,deltaT)
            coeff.calc_fx(grid.conc,Theta,Kf,Kb,deltaT)
            try:
                coeff.dx=linalg.spsolve(sparse.csr_matrix(coeff.J),sparse.csr_matrix(coeff.fx[:,np.newaxis]))
            except:
                print("Using lstsq solver! ")
                coeff.dx = np.linalg.lstsq(coeff.J,coeff.fx,rcond=None)[0]
            grid.conc = coeff.xupdate(grid.conc,Theta)

            if np.mean(np.absolute(coeff.dx)) < 1e-12:
                #print(f'Exit: Precision satisfied!\nExit at iteration {ii}')
                break
            
        if not np.isnan(grid.grad()):
            grid.fluxes.append([grid.t[index],grid.grad()])
            if input_parameters.ViewOption[0]:

                fluxes = np.array(grid.fluxes)
                if dimensional: 
                    fluxes[:,0],fluxes[:,1] = toDimensionalCA(fluxes[:,0],fluxes[:,1],geometry_number,dElectrode,lElectrode,E0f,Temperature,Dref,cRef)
                signals.fluxesProfile.emit(fluxes)
        else:
            print('Bad solution')

        






    grid.saveVoltammogram(grid.t,output_file_name,dimensional,geometry_number,Temperature,E0f,dElectrode,lElectrode,Dref,cRef)

    signals.output_file_name.emit(output_file_name)
    signals.progress.emit(100)
    signals.finished.emit()



    

if __name__ == "__main__":
    pass
    














    

    


