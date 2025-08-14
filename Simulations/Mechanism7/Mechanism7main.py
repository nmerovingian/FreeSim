import numpy as np
import time
from Simulations.Mechanism7.coeff import Coeff
from Simulations.Mechanism7.grid import Grid
from helper import toDimensional
import csv
import scipy
from scipy import sparse
from scipy.sparse import linalg
import time
import os
import math
from matplotlib import pyplot as plt
import pickle
import time
# the total concentration of X added before any chemical equilibrium happen 

P0 = 1.0 # reference pressure, 1 bar



def Mechanism_7_simulation_single_thread_Gui(signals=None,input_parameters=None)->None:
    cRef=1.0#input_parameters.chemical_parameters_22[3]
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
    output_file_name = f'{directory}/{file_name}{file_type}'
    dimensional = input_parameters.file_options_parameters[5]
    Temperature = input_parameters.cv_parameters_1[7]
    theta_i = (input_parameters.cv_parameters_1[0]-E0f)*96485/(8.314*Temperature)
    theta_v = (input_parameters.cv_parameters_1[1]- E0f)*96485/(8.314*Temperature)
    dimScanRate = input_parameters.cv_parameters_1[3]
    cycles = int(input_parameters.cv_parameters_1[4])
    #space step
    deltaX = 1e-5
    #potential step
    deltaTheta = input_parameters.model_parameters_30[0]*96485/(8.314*Temperature)
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

    if input_parameters.chemical_parameters_2[0] == 1:
        kinetics = 'BV'
    elif input_parameters.chemical_parameters_2[0] == 2:
        kinetics = 'MH'
        raise ValueError('Marcus Harsh is an unimplemented Electrode kinetics ')
    else:
        raise ValueError('Unknown/Unimplemented Electrode kinetics ')
     
    mechanism = input_parameters.mechanism_parameters_0[0]
    k0 = input_parameters.chemical_parameters_2[3]
    # standard electrochemical rate constant. Only useful if using Butler-Volmer equation for boundary conditions

    K0 = k0*dElectrode / Dref

    alpha = input_parameters.chemical_parameters_2[4]

    GammaMax = input_parameters.adsorption_parameters_5[0]
    kads_A = input_parameters.adsorption_parameters_5[1]
    kdes_A = input_parameters.adsorption_parameters_5[2]
    kads_B = input_parameters.adsorption_parameters_5[3]
    kdes_B = input_parameters.adsorption_parameters_5[4]
    Gamma_A = input_parameters.adsorption_parameters_5[5]
    Gamma_B = input_parameters.adsorption_parameters_5[6]
    E0_ads = input_parameters.adsorption_parameters_5[7]
    k0_ads = input_parameters.adsorption_parameters_50[0]
    alpha_ads  = input_parameters.adsorption_parameters_50[1]
    Kads_A = kads_A * GammaMax * dElectrode/Dref
    Kdes_A = kdes_A * GammaMax * dElectrode/Dref
    Kads_B = kads_B * GammaMax * dElectrode/Dref
    Kdes_B = kdes_B * GammaMax * dElectrode/Dref
    beta = cRef*dElectrode/GammaMax
    Theta_diff = (E0_ads - E0f)*(98485/(8.314*Temperature))
    K0_ads = k0_ads * dElectrode * dElectrode /Dref

    zeta_A = Gamma_A / GammaMax
    zeta_B = Gamma_B / GammaMax

    if not os.path.exists(directory):
        os.mkdir(directory)




    sigma = dElectrode*dElectrode/Dref*(96485/(8.314*298)) *dimScanRate
    




    nTimeSteps_cycles = int(2*np.fabs(theta_v-theta_i)/deltaTheta)*cycles
    nTimeSteps = int(2*np.fabs(theta_v-theta_i)/deltaTheta)
    Esteps = np.arange(nTimeSteps,dtype=np.float64)
    E = np.where(Esteps<nTimeSteps/2.0,theta_i-deltaTheta*Esteps,theta_v+deltaTheta*(Esteps-nTimeSteps/2.0))
    E = np.tile(E,cycles)








 


    concA = input_parameters.chemical_parameters_22[3]/cRef
    concB = input_parameters.chemical_parameters_22[7]/cRef
    concC = input_parameters.chemical_parameters_22[11]/cRef
    concY = input_parameters.chemical_parameters_22[15]/cRef
    concZ = input_parameters.chemical_parameters_22[19]/cRef

    print(f"concA {concA}, concB{concB}, concY {concY}, concZ {concZ}")

    # dimensionless diffusion coefficients of every species
    dA =DA/Dref
    dB =DB/Dref   # diffusion coefficient of H+
    dC =DC/Dref
    dY =DY/Dref  # diffusion coeffficient of acetate+
    dZ =DZ/Dref    # diffusion coefficient of H_2 

    # the maximum number of iterations for Newton method
    number_of_iteration = int(input_parameters.model_parameters_30[1])

    deltaT = deltaTheta/sigma
    print('sigma',sigma,'DeltaT',deltaT)
    # The maximum distance of simulation

    maxT = 2.0*abs(theta_v-theta_i)/sigma
    SimulationSpaceMultiple  = input_parameters.model_parameters_3[2]
    if diffusion_mode == 'linear':
        maxX = SimulationSpaceMultiple * np.sqrt(maxT)
    elif diffusion_mode =='radial':
        maxX = 1.0 +  SimulationSpaceMultiple * np.sqrt(maxT)




    coeff = Coeff(deltaT,maxX,kinetics,diffusion_mode,zeta,K0,K0_ads,Kads_A,Kdes_A,Kads_B,Kdes_B,alpha,alpha_ads,beta,gamma,Theta_diff,dA,dB,dC,dY,dZ,mechanism)
    coeff.calc_n(deltaX)

    #simulation steps


    # initialzie matrix for Coeff object
    coeff.ini_jacob()
    coeff.ini_fx()
    coeff.ini_dx()
    # initialze matrix for Grid objectd
    grid = Grid(coeff.n,diffusion_mode,beta)
    grid.grid(deltaX,gamma)
    grid.init_c(concA,concB,concC,concY,concZ,zeta_A,zeta_B,theta_i)

    coeff.get_XX(grid.x)
   
    
 


    start_time = time.time()

    for index in range(0,len(E)):
        if len(E)> 100:
            if index%int(len(E)*0.01) ==0:

                with open('.status.pkl','rb') as f:
                    dict = pickle.load(f)
                if dict['stop']:
                    return 0
                while dict['pause']:
                    time.sleep(0.2)
                    with open('.status.pkl','rb') as f:
                        dict = pickle.load(f)
                    if not dict['pause']:
                        break 

                progress =index/len(E)
                signals.progress.emit(int(progress*100))
                if input_parameters.ViewOption[1]:
                    grid.updateAll()
                    ConcProfile = grid.packageAllConc()
                    ConcProfile[:,0] *= dElectrode
                    signals.concProfile.emit(ConcProfile)

        Theta = E[index]
        

        #Theta  = Theta + deltaTheta
        
        if index == 2:
            print(f'Total run time is {(time.time()-start_time)*len(E)/60:.2f} mins')


        coeff.update(grid.conc,concA,concB,concC,concY,concZ)
        coeff.Allcalc_abc(deltaT,Theta,deltaX)
        for ii in range(number_of_iteration):
            coeff.calc_jacob(grid.conc,Theta)
            coeff.calc_fx(grid.conc,Theta)
            try:
                coeff.dx=linalg.spsolve(sparse.csr_matrix(coeff.J),sparse.csr_matrix(coeff.fx[:,np.newaxis]))
            except:
                print("Using lstsq solver! ")
                coeff.dx = np.linalg.lstsq(coeff.J,coeff.fx,rcond=None)[0]
            grid.conc = coeff.xupdate(grid.conc,Theta)

            if np.mean(np.absolute(coeff.dx)) < 1e-12:
                #print(f'Exit: Precision satisfied!\nExit at iteration {ii}')
                break
            
        if not np.isnan(grid.grad(coeff.d,deltaT)):
            grid.fluxes.append([Theta,grid.grad(coeff.d,deltaT)/concA])
            if input_parameters.ViewOption[0]: 
                fluxes = np.array(grid.fluxes)
                if dimensional:
                    fluxes[:,0],fluxes[:,1] = toDimensional(fluxes[:,0],fluxes[:,1],geometry_number,dElectrode,lElectrode,E0f,Temperature,Dref,cRef)
                signals.fluxesProfile.emit(fluxes)
        else:
            print('Bad solution')

        






    grid.saveVoltammogram(E,output_file_name,dimensional,geometry_number,Temperature,E0f,dElectrode,lElectrode,Dref,cRef)

    signals.output_file_name.emit(output_file_name)
    signals.progress.emit(100)
    signals.finished.emit()



    


if __name__ == "__main__":
    import pickle
    import sys
    sys.path.append('../..')
    np.set_printoptions(threshold=sys.maxsize)
    with open('RGCUserSetting.pkl','rb') as f:
        input_parameter = pickle.load(f)

    Mechanism_7_simulation_single_thread_Gui(input_parameters=input_parameter)
    













    

    


