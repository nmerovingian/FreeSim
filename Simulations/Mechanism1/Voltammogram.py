from Parameters import Parameters
import numpy as np
import pandas as pd

import csv 

class Voltammogram(object):
    def __init__(self,p):
        self.p = p
        nTimeSteps = int(p.nTimeSteps / p.cycles)
        self.E = np.arange(nTimeSteps,dtype=np.float64)
        self.I = np.zeros(p.nTimeSteps, dtype=np.float64)

        # initialize time steps
        self.t = np.arange(p.nTimeSteps) * p.dt


        self.E = np.where(self.E<nTimeSteps/2.0, p.EMax - p.v * p.dt *self.E, p.EMin + p.v*p.dt * (self.E - nTimeSteps/2.0))
        self.E = np.tile(self.E,p.cycles)




    def averageAndSave(self,output_file_name,saveFile=False):

        self.I_average = np.average(self.I.reshape((int(self.p.nTimeSteps/self.p.nOversampling),int(self.p.nOversampling))),axis=1)


        t = self.t[::self.p.nOversampling]
        E = self.E[::self.p.nOversampling]

        voltammogram = np.stack((E,self.I_average,t),axis=1)

        if saveFile:
            df = pd.DataFrame(voltammogram,columns=['Potential, V','Current,A','Time, s'])
            df.to_csv(output_file_name,index=False)

        return voltammogram








