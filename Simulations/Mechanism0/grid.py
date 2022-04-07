import numpy as np
import csv

class Grid(object):
    def __init__(self,n):
        self.n = n
        self.x = np.zeros(self.n,dtype=np.float64)
        self.conc = np.zeros(self.n*5,dtype=np.float64)
        self.concA = np.zeros(self.n,dtype=np.float64)
        self.concB = np.zeros(self.n,dtype=np.float64)
        self.concC = np.zeros(self.n,dtype=np.float64)
        self.concY = np.zeros(self.n,dtype=np.float64)
        self.concZ = np.zeros(self.n,dtype=np.float64)

        self.g = 0.0


    def grid(self,dX,gamma):
        self.x[0] = 0.0
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

    
    
    

    def grad(self):
        self.g = -(self.conc[5]-self.conc[0]) / (self.x[1]-self.x[0])
        return self.g

    def updateAll(self):
        self.concA = self.conc[::4]
        self.concB = self.conc[1::4]
        self.concY = self.conc[2::4]
        self.concZ = self.conc[3::4]

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