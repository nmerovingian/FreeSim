import numpy as np
import csv
import pandas as pd

class Grid(object):
    def __init__(self,n,diffusion_mode,beta):
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
        self.beta = beta


    def grid(self,dX,gamma):
        if self.diffusion_mode =='linear':
            self.x[0] = 0.0
            self.x[1] = 0.0
        elif self.diffusion_mode =='radial':
            self.x[0] = 1.0
            self.x[1] = 1.0
        else:
            raise ValueError
        for i in range(2,self.n):
            self.x[i] = self.x[i-1] + dX
            dX = dX* (1.0 +gamma )

    
    # initialize the concentration matrix
    def init_c(self,A:float,B:float,C:float,Y:float,Z:float,zeta_A,zeta_B,Theta:float):
        self.conc[0] = zeta_A
        self.conc[1] = zeta_B
        self.conc[2] = C
        self.conc[3] = Y
        self.conc[4] = Z
        self.conc[5::5] = A
        self.conc[6::5] = B
        self.conc[7::5] = C
        self.conc[8::5] = Y
        self.conc[9::5] = Z

        self.concA[0] = zeta_A
        self.concB[0] = zeta_B
        self.concC[0] = C
        self.concY[0] = Y 
        self.concZ[0] = Z


        self.concA[1:] = A
        self.concB[1:] = B
        self.concC[1:] = C
        self.concY[1:] = Y 
        self.concZ[1:] = Z

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
    def grad(self,d,deltaTheta):
        self.g = -(self.conc[10]-self.conc[5]) / (self.x[2]-self.x[1])  + self.beta*(self.conc[0]-d[0])/(deltaTheta)
        return self.g

    def updateAll(self):
        self.concA = self.conc[5::5]
        self.concB = self.conc[6::5]
        self.concC = self.conc[7::5]
        self.concY = self.conc[8::5]
        self.concZ = self.conc[9::5]

    def packageAllConc(self):
        package = np.stack((self.x[1:],self.concA,self.concB,self.concC,self.concY,self.concZ),axis=1)
        return package

    def saveVoltammogram(self,E,output_file_name):
        voltammogram = np.array(self.fluxes)
        print(voltammogram.shape)
        df = pd.DataFrame(voltammogram,columns=['Potential,V','Current,A'])
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