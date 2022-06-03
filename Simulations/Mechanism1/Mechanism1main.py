import queue
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from Simulations.Mechanism1.Constants import Constants
from Simulations.Mechanism1.Parameters import Parameters
Parameters.evalImplicitParameters(Constants)
from Simulations.Mechanism1.Voltammogram import Voltammogram
from Simulations.Mechanism1.Molecule import Molecule
from random import random,seed
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue,Lock,Pool,Process,Manager
import pickle
import time 
seed(1)




def singleMolecule(args):
    index , l = args
    print(index)
    v = Voltammogram(Parameters)
    m = Molecule(random(),Parameters,Constants)


    for i in range(Parameters.nTimeSteps):
        evalChargeTransfer = m.move(bool(round(random())))

        if evalChargeTransfer:
            l[i] += m.evalChargeTransfer(v.E[i],random())






def simulation():
    for n in np.arange(0,int(Parameters.nMolecules)):
        #print(f"{n} of {Parameters.nMolecules}")
        # Initialize molecuels
        m = Molecule(random(),Parameters,Constants)

        # calculate paths
        for i in range(Parameters.nTimeSteps):
            evalChargeTransfer = m.move(bool(round(random())))

            if evalChargeTransfer:
                v.I[i] += m.evalChargeTransfer(v.E[i],random())


def Mechanism_1_simulation_single_thread_GUI(signals,input_parameters):
    from Parameters import Parameters
    Parameters.modifyDefaultParameters(input_parameters=input_parameters)
    from Constants import Constants
    Constants.modifyConstants(input_parameters=input_parameters)
    Parameters.evalImplicitParameters(Constants)
    from Voltammogram import Voltammogram
    from Molecule import Molecule
    
    v = Voltammogram(Parameters)
    for n in range(0,int(Parameters.nMolecules)):
        if Parameters.nMolecules > 100:
            if n%int(Parameters.nMolecules*0.01) ==0:


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

                print(f"{n} of {Parameters.nMolecules}")
                progress =n/Parameters.nMolecules
                signals.progress.emit(int(progress*100))
                voltammogram = v.averageAndSave(Parameters.output_file_name,saveFile=False)
                signals.fluxesProfile.emit(voltammogram)
        m = Molecule(random(),Parameters,Constants)

        # calculate paths
        for i in range(Parameters.nTimeSteps):
            evalChargeTransfer = m.move(bool(round(random())))

            if evalChargeTransfer:
                v.I[i] += m.evalChargeTransfer(v.E[i],random())
    v.averageAndSave(Parameters.output_file_name,saveFile=True)
    signals.output_file_name.emit(Parameters.output_file_name)
    signals.progress.emit(100)
    signals.finished.emit()
    return None



if __name__ == "__main__":
    multiprocessing_mode = True
    
    # generate instance of voltammograms


    if not multiprocessing_mode:
    # calcualte random walks
        v = Voltammogram(Parameters)
        for n in range(0,int(Parameters.nMolecules)):
            print(f"{n} of {Parameters.nMolecules}")
            m = Molecule(random(),Parameters,Constants)

            # calculate paths
            for i in range(Parameters.nTimeSteps):
                evalChargeTransfer = m.move(bool(round(random())))

                if evalChargeTransfer:
                    v.I[i] += m.evalChargeTransfer(v.E[i],random())
        v.averageAndSave()


    
    else:
        v = Voltammogram(Parameters)
        with Manager() as manager:
            l = manager.list([0.0 for i in range(Parameters.nTimeSteps)])
            pool =Pool(processes=5)
            pool.map(singleMolecule,[(index,l) for index in range(Parameters.nMolecules)])





            for i in range(Parameters.nTimeSteps):
                v.I[i] = l[i] 

            v.averageAndSave()

            print('job done ')
