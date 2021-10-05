import numpy as np
import csv
import pandas as pd
import math

class Grid(object):
    def __init__(self,n,diffusion_mode):
        self.n = n
        self.x = np.zeros(self.n,dtype=np.float64)
        self.conc = np.zeros(self.n*5,dtype=np.float64)
        self.concA = np.zeros(self.n,dtype=np.float64)
        self.concB = np.zeros(self.n,dtype=np.float64)
        self.concC = np.zeros(self.n,dtype=np.float64)
        self.concY = np.zeros(self.n,dtype=np.float64)
        self.concZ = np.zeros(self.n,dtype=np.float64)
        self.diffusion_mode = diffusion_mode
        self.fluxes = list()
        self.g = 0.0


    def grid(self,dX,gamma):
        if self.diffusion_mode =='linear':
            self.x[0] = 0.0
        elif self.diffusion_mode =='radial':
            self.x[0] = 1.0
        else:
            raise ValueError
        for i in range(1,self.n):
            self.x[i] = self.x[i-1] + dX
            dX = dX* (1.0 +gamma )

    
    # initialize the concentration matrix
    def init_c(self,A:float,B:float,C:float,Y:float,Z:float,Theta:float):
        self.conc[::5] = A
        self.conc[1::5] = B
        self.conc[2::5] = C
        self.conc[3::5] = Y
        self.conc[4::5] = Z

        self.concA[:] = A
        self.concB[:] = B
        self.concC[:] = C
        self.concY[:] = Y 
        self.concZ[:] = Z

    # A better initialized concentration vector
    
    
    
    """
    def init_c(self,A:float,B:float,Y:float,Z:float,Theta:float):
        NernstB = B*1.0/(1.0 + np.exp(-Theta))
        NernstY = B*1.0/(1.0 + np.exp(Theta))

        self.concB = np.linspace(NernstB,B,num=self.n,endpoint=True)
        self.concY = np.linspace(NernstY,Y,num=self.n,endpoint=True)
        self.concZ[:] = Z
        self.concA[:] = A

        self.conc[::4] = self.concA
        self.conc[1::4] = self.concB
        self.conc[2::4] = self.concY
        self.conc[3::4] = self.concZ

        #print(self.conc)
    """
    """
    
    def init_c(self,A:float,B:float,Y:float,Z:float,Theta:float):
        NernstB = B*1.0/(1.0 + np.exp(-Theta))
        NernstY = B*1.0/(1.0 + np.exp(Theta))

        self.conc[::4] = A
        self.conc[1::4] = B
        self.conc[2::4] = Y
        self.conc[3::4] = Z

        self.conc[1] = NernstB
        self.conc[2] = NernstY

        self.concA = self.conc[::4]
        self.concB = self.conc[1::4]
        self.concY = self.conc[2::4]
        self.concZ = self.conc[3::4]  

    """
    def grad(self):
        self.g = -(self.conc[5]-self.conc[0]) / (self.x[1]-self.x[0])
        return self.g

    def updateAll(self):
        self.concA = self.conc[::5]
        self.concB = self.conc[1::5]
        self.concC = self.conc[2::5]
        self.concY = self.conc[3::5]
        self.concZ = self.conc[4::5]

    def packageAllConc(self):
        package = np.stack((self.x,self.concA,self.concB,self.concC,self.concY,self.concZ),axis=1)
        return package

    def saveVoltammogram(self,E,output_file_name,dimensional = True,Temperature = None, E0f=None,dElectrode = None,Dref=None,Cref=None):
        voltammogram = np.array(self.fluxes)
        print(voltammogram.shape)
        df = pd.DataFrame(voltammogram,columns=['Potential,V','Current,A'])
        if dimensional:
            df.iloc[:,0] = df.iloc[:,0] / (96485/(8.314*Temperature)) + E0f
            df.iloc[:,1] = df.iloc[:,1] *math.pi*dElectrode*96485*Dref*Cref

        df.to_csv(output_file_name,index=False)

        

    def saveA(self,filename):
        f=open(filename,mode='w',newline='')
        writer = csv.writer(f)
        for i in range(self.n):
            writer.writerow([self.x[i],self.concA[i]])
        f.close()

    def saveB(self,filename):
        f=open(filename,mode='w',newline='')
        writer = csv.writer(f)
        for i in range(self.n):
            writer.writerow([self.x[i],self.concB[i]])
        f.close()
    
    def saveY(self,filename):
        f=open(filename,mode='w',newline='')
        writer = csv.writer(f)
        for i in range(self.n):
            writer.writerow([self.x[i],self.concY[i]])
        f.close()
    
    def saveZ(self,filename):
        f=open(filename,mode='w',newline='')
        writer = csv.writer(f)
        for i in range(self.n):
            writer.writerow([self.x[i],self.concZ[i]])
        f.close()