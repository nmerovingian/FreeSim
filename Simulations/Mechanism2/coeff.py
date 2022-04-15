import numpy as np

class Coeff(object):
    def __init__(self,Thetadiff,deltaT,maxX,kinetics,mode,zeta,K0AB,K0BC,Kcomp,Kdisp,alphaAB,alphaBC,gamma,dA,dB,dC,dY,dZ,mechanism):
        self.n = 0
        self.xi = 0.0
        self.Thetadiff = Thetadiff
        self.maxX = maxX
        self.kinetics = kinetics
        self.mode = mode
        self.zeta = zeta
        self.K0AB = K0AB
        self.K0BC =K0BC
        self.Kcomp = Kcomp*deltaT
        self.Kdisp = Kdisp*deltaT
        self.alphaAB = alphaAB
        self.alphaBC = alphaBC
        self.gamma = gamma
        self.dA = dA
        self.dB = dB
        self.dC = dC
        self.dY = dY
        self.dZ = dZ
        self.mechanism = mechanism

        if self.mode =='linear':
            self.xi = 0.0
        elif self.mode=='radial':
            self.xi = 1.0
        else:
            raise ValueError




    def calc_n(self,dX):
        while self.xi < self.maxX:
            self.xi += dX
            dX = dX*(1.0+self.gamma)
            self.n = self.n + 1

        self.n = self.n + 1 

        print(f"n is {self.n}")

        self.aA = np.zeros(self.n)
        self.bA = np.zeros(self.n)
        self.cA = np.zeros(self.n)
        self.aB = np.zeros(self.n)
        self.bB = np.zeros(self.n)
        self.cB = np.zeros(self.n)
        self.aC = np.zeros(self.n)
        self.bC = np.zeros(self.n)
        self.cC = np.zeros(self.n)
        self.aY = np.zeros(self.n)
        self.bY = np.zeros(self.n)
        self.cY = np.zeros(self.n)
        self.aZ = np.zeros(self.n)
        self.bZ = np.zeros(self.n)
        self.cZ = np.zeros(self.n)
        self.d = np.zeros(self.n*5)

        self.XX = np.zeros(self.n)


    

    def ini_jacob(self):
        self.J = np.zeros((5*self.n,5*self.n),dtype=np.float64)


    def ini_fx(self):
        self.fx = np.zeros(5*self.n,dtype=np.float64)


    def ini_dx(self):
        self.dx = np.zeros(5*self.n,dtype=np.float64)

    def get_XX(self,xx:np.ndarray):
        self.XX = xx.copy()


    # D value are different for a steady state simulation
    def update(self,x,A,B,C,Y,Z):
        self.d = x.copy()

        self.d[-1] = Z
        self.d[-2] = Y
        self.d[-3] = C
        self.d[-4] = B
        self.d[-5] = A

    
    def xupdate(self,x,Theta):
        x = x+ self.dx
        return x
    
    
    """
    def xupdate(self,x,Theta):
        t = 1.0

        self.calc_fx(x,Theta)
        original = np.mean(np.absolute(self.fx))
        self.calc_fx(x+t*self.dx,Theta)
        damped = np.mean(np.absolute(self.fx))

        while damped > original:
            t = t/2.0
            self.calc_fx(x+t*self.dx,Theta)
            damped = np.mean(np.absolute(self.fx))

            #print(t)

            if t < 1e-10:
                break

        x = x + t*self.dx
        return x"""
    
    
    
    def Acal_abc_radial(self,deltaT,Theta,deltaX):
        self.aA[0] = 0.0
        self.bA[0] = 0.0
        self.cA[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aA[i] = self.dA*((-(2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)) + self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
            self.bA[i] = self.dA*(((2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) + (2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)))) + 1.0
            self.cA[i] = self.dA*((-(2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) - self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))

        self.aA[-1] = 0.0
        self.bA[-1] = 0.0
        self.cA[-1] = 0.0

    def Bcal_abc_radial(self,deltaT,Theta,deltaX):
        self.aB[0] = 0.0
        self.bB[0] = 0.0
        self.cB[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aB[i] =self.dB*( (-(2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)) + self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
            self.bB[i] =self.dB*( ((2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) + (2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)))) + 1.0
            self.cB[i] =self.dB*((-(2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) - self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))

        self.aB[-1] = 0.0
        self.bB[-1] = 0.0
        self.cB[-1] = 0.0


    def Ccal_abc_radial(self,deltaT,Theta,deltaX):
        self.aC[0] = 0.0
        self.bC[0] = 0.0
        self.cC[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aC[i] =self.dC*( (-(2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)) + self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
            self.bC[i] =self.dC*( ((2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) + (2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)))) + 1.0
            self.cC[i] =self.dC*((-(2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) - self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))

        self.aC[-1] = 0.0
        self.bC[-1] = 0.0
        self.cC[-1] = 0.0


    def Ycal_abc_radial(self,deltaT,Theta,deltaX):
        self.aY[0] = 0.0
        self.bY[0] = 0.0
        self.cY[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aY[i] = self.dY*((-(2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)) + self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
            self.bY[i] = self.dY*(((2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) + (2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)))) + 1.0
            self.cY[i] = self.dY*((-(2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) - self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
        self.aY[-1] = 0.0
        self.bY[-1] = 0.0
        self.cY[-1] = 0.0

    def Zcal_abc_radial(self,deltaT,Theta,deltaX):
        self.aZ[0] = 0.0
        self.bZ[0] = 0.0
        self.cZ[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aZ[i] = self.dZ*((-(2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)) + self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
            self.bZ[i] = self.dZ*(((2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) + (2.0 * deltaT) / (deltaX_m * (deltaX_m + deltaX_p)))) + 1.0
            self.cZ[i] = self.dZ*((-(2.0 * deltaT) / (deltaX_p * (deltaX_m + deltaX_p)) - self.zeta / self.XX[i] * (deltaT / (deltaX_m + deltaX_p))))
        self.aZ[-1] = 0.0
        self.bZ[-1] = 0.0
        self.cZ[-1] = 0.0


    def Acal_abc_linear(self,deltaT,Theta,deltaX):
        self.aA[0] = 0.0
        self.bA[0] = 0.0
        self.cA[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aA[i] = self.dA*((-2.0*deltaT)/(deltaX_m*(deltaX_m+deltaX_p)))
            self.cA[i] = self.dA*((-2.0*deltaT)/(deltaX_p*(deltaX_m+deltaX_p)))
            self.bA[i] = 1.0-self.aA[i] - self.cA[i]
        self.aA[-1] = 0.0
        self.bA[-1] = 0.0
        self.cA[-1] = 0.0

    def Bcal_abc_linear(self,deltaT,Theta,deltaX):
        self.aB[0] = 0.0
        self.bB[0] = 0.0
        self.cB[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aB[i] = self.dB*((-2.0*deltaT)/(deltaX_m*(deltaX_m+deltaX_p)))
            self.cB[i] = self.dB*((-2.0*deltaT)/(deltaX_p*(deltaX_m+deltaX_p)))
            self.bB[i] = 1.0-self.aB[i] - self.cB[i]
        self.aB[-1] = 0.0
        self.bB[-1] = 0.0
        self.cB[-1] = 0.0

    def Ccal_abc_linear(self,deltaT,Theta,deltaX):
        self.aC[0] = 0.0
        self.bC[0] = 0.0
        self.cC[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aC[i] = self.dC*((-2.0*deltaT)/(deltaX_m*(deltaX_m+deltaX_p)))
            self.cC[i] = self.dC*((-2.0*deltaT)/(deltaX_p*(deltaX_m+deltaX_p)))
            self.bC[i] = 1.0-self.aC[i] - self.cC[i]
        self.aC[-1] = 0.0
        self.bC[-1] = 0.0
        self.cC[-1] = 0.0

    def Ycal_abc_linear(self,deltaT,Theta,deltaX):
        self.aY[0] = 0.0
        self.bY[0] = 0.0
        self.cY[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aY[i] = self.dY*((-2.0*deltaT)/(deltaX_m*(deltaX_m+deltaX_p)))
            self.cY[i] = self.dY*((-2.0*deltaT)/(deltaX_p*(deltaX_m+deltaX_p)))
            self.bY[i] = 1.0-self.aY[i] - self.cY[i]
        self.aY[-1] = 0.0
        self.bY[-1] = 0.0
        self.cY[-1] = 0.0

    def Zcal_abc_linear(self,deltaT,Theta,deltaX):
        self.aZ[0] = 0.0
        self.bZ[0] = 0.0
        self.cZ[0] = 0.0

        for i in range(1,self.n-1):
            deltaX_m = self.XX[i] - self.XX[i - 1]
            deltaX_p = self.XX[i + 1] - self.XX[i]
            self.aZ[i] = self.dZ*((-2.0*deltaT)/(deltaX_m*(deltaX_m+deltaX_p)))
            self.cZ[i] = self.dZ*((-2.0*deltaT)/(deltaX_p*(deltaX_m+deltaX_p)))
            self.bZ[i] = 1.0-self.aZ[i] - self.cZ[i]
        self.aZ[-1] = 0.0
        self.bZ[-1] = 0.0
        self.cZ[-1] = 0.0


    def Allcalc_abc(self,deltaT,Theta,deltaX,mode='linear'):
        if mode =='radial':
            self.Acal_abc_radial(deltaT,Theta,deltaX)
            self.Bcal_abc_radial(deltaT,Theta,deltaX)
            self.Ccal_abc_radial(deltaT,Theta,deltaX)
            self.Ycal_abc_radial(deltaT,Theta,deltaX)
            self.Zcal_abc_radial(deltaT,Theta,deltaX)
        elif mode =='linear':
            self.Acal_abc_linear(deltaT,Theta,deltaX)
            self.Bcal_abc_linear(deltaT,Theta,deltaX)
            self.Ccal_abc_linear(deltaT,Theta,deltaX)
            self.Ycal_abc_linear(deltaT,Theta,deltaX)
            self.Zcal_abc_linear(deltaT,Theta,deltaX)
    
    def calc_jacob(self,x,Theta):
        h = self.XX[1] - self.XX[0]
        self.J = np.zeros((5*self.n,5*self.n),dtype=np.float64)
        self.J[3,3] = -1.0
        self.J[3,8] = 1.0
        self.J[4,4] = -1.0
        self.J[4,9] = 1.0


        if self.kinetics =='BV':
            KredAB = self.K0AB*np.exp(-self.alphaAB*Theta)
            KoxAB = self.K0AB*np.exp((1.0-self.alphaAB)*Theta)
            KredBC = self.K0BC*np.exp(-self.alphaBC*(Theta-self.Thetadiff))
            KoxBC = self.K0BC*np.exp((1.0-self.alphaBC)*(Theta-self.Thetadiff))
            self.J[0,0] = KredAB*h/self.dA + 1.0
            self.J[0,1] = -KoxAB*h/self.dA
            self.J[0,5] = -1.0
            self.J[1,0] = -KredAB*h/self.dB
            self.J[1,1] = KoxAB*h/self.dB + KredBC*h/self.dB + 1.0
            self.J[1,2] = - KoxBC*h/self.dB
            self.J[1,6] = -1.0
            self.J[2,1] = -KredBC*h/self.dC
            self.J[2,2] = KoxBC*h/self.dC + 1.0 
            self.J[2,7] = -1.0
        else:
            raise ValueError
        

        

        for row in range(5,self.n*5-5,5):
            i = int(row/5)

            #initialize species A:
            self.J[row,row-5] = self.aA[i]
            self.J[row,row] = self.bA[i] 
            self.J[row,row+5] = self.cA[i]

            self.J[row+1,row-4] = self.aB[i]
            self.J[row+1,row+1] = self.bB[i]
            self.J[row+1,row+6] = self.cB[i]

            self.J[row+2,row-3] = self.aC[i]

            self.J[row+2,row+2] = self.bC[i] 
            self.J[row+2,row+7] = self.cC[i]

            self.J[row+3,row-2] = self.aY[i]
            self.J[row+3,row+3] = self.bY[i]
            self.J[row+3,row+8] = self.cY[i]

            self.J[row+4,row-1] = self.aZ[i]
            self.J[row+4,row+4] = self.bZ[i]
            self.J[row+4,row+9] = self.cZ[i]
            
            if self.mechanism == 2:
                self.J[row,row] += self.Kcomp*x[5*i+2]
                self.J[row,row+1] += -2.0*self.Kdisp*x[5*i+1]
                self.J[row,row+2] += self.Kcomp*x[5*i]

                self.J[row+1,row] += -2.0*self.Kcomp*x[5*i+2]
                self.J[row+1,row+1] += 4.0*self.Kdisp*x[5*i+1]
                self.J[row+1,row+2] += -2.0*self.Kcomp*x[5*i]

                self.J[row+2,row] += self.Kcomp*x[5*i+2]
                self.J[row+2,row+1] += -2.0*self.Kdisp*x[5*i+1]
                self.J[row+2,row+2] += self.Kcomp*x[5*i]
            else:
                raise ValueError

        self.J[5*self.n-5,5*self.n-5] = 1.0
        self.J[5*self.n-4,5*self.n-4] = 1.0
        self.J[5*self.n-3,5*self.n-3] = 1.0
        self.J[5*self.n-2,5*self.n-2] = 1.0
        self.J[5*self.n-1,5*self.n-1] = 1.0



    def calc_fx(self,x,Theta):
        h = self.XX[1] - self.XX[0]

        if self.kinetics =='BV':
            KredAB = self.K0AB*np.exp(-self.alphaAB*Theta)
            KoxAB = self.K0AB*np.exp((1.0-self.alphaAB)*Theta)
            KredBC = self.K0BC*np.exp(-self.alphaBC*(Theta-self.Thetadiff))
            KoxBC = self.K0BC*np.exp((1.0-self.alphaBC)*(Theta-self.Thetadiff))
            self.fx[0] = (1+KredAB*h/self.dA)*x[0] - KoxAB*h/self.dA * x[1] - x[5]
            self.fx[1] = (1+KoxAB*h/self.dB+KredBC*h/self.dB)*x[1] - KredAB*h/self.dB * x[0] - KoxBC*h/self.dB*x[2] - x[6]
            self.fx[2] = (1+KoxBC*h/self.dC)*x[2] - KredBC*h/self.dC*x[1] - x[7]
        else:
            raise ValueError
        
        self.fx[3] = x[8] - x[3]
        self.fx[4] = x[9] - x[4]
        """
        #BV boundary condition
        Kred = self.K0*self.Kappa*np.exp(-self.alpha*Theta)
        Kox = self.K0*np.exp((2.0-self.alpha)*Theta)
        self.fx[1] = x[1] + Kred*h* (1.0/self.dB)*x[1]*x[1] - Kox*h*(1/self.dB)*x[2]- x[5]
        self.fx[2] = x[2] - 0.5*Kred*h*(1.0/self.dY)*x[1]*x[1] + 0.5*Kox*h*(1.0/self.dY)*x[2] - x[6]
        """

        #self.fx[2] = self.dY*((x[6]-x[2])/h) + self.dB*((x[5]-x[1])/h)
        #self.fx[2] = x[1]/np.exp(Theta) - x[2]

        #self.fx[1]  =  x[1] - self.concB * (1.0/(1.0+np.exp(-Theta)))
        #self.fx[2]  = self.concB* (1.0/(1.0+np.exp(Theta))) - x[2]


        for j in range(5,5*self.n-5,5):
            i = int(j/5)

            self.fx[j] = self.aA[i]*x[5*i-5] + self.bA[i]*x[5*i]+ self.cA[i]*x[5*i+5]- self.d[5*i]
            self.fx[j+1] = self.aB[i]*x[5*i-4] + self.bB[i]*x[5*i+1] + self.cB[i]*x[5*i+6] - self.d[5*i+1]
            self.fx[j+2] = self.aC[i]*x[5*i-3] + self.bC[i]*x[5*i+2] + self.cC[i]*x[5*i+7] - self.d[5*i+2]
            self.fx[j+3] = self.aY[i]*x[5*i-2] + self.bY[i]*x[5*i+3] + self.cY[i]*x[5*i+8] - self.d[5*i+3]
            self.fx[j+4] = self.aZ[i]*x[5*i-1] + self.bZ[i]*x[5*i+4] + self.cZ[i]*x[5*i+9] - self.d[5*i+4]


            if self.mechanism == 2:
                self.fx[j] += -self.Kdisp*x[5*i+1]*x[5*i+1] + self.Kcomp*x[5*i]*x[5*i+2]
                self.fx[j+1] += 2.0*self.Kdisp*x[5*i+1]*x[5*i+1] - 2.0*self.Kcomp*x[5*i]*x[5*i+2]
                self.fx[j+2] += -self.Kdisp*x[5*i+1]*x[5*i+1] + self.Kcomp*x[5*i]*x[5*i+2]
            else:
                raise ValueError

        self.fx[5*self.n-5] = x[self.n*5-5] - self.d[5*self.n-5]
        self.fx[5*self.n-4] = x[self.n*5-4] - self.d[5*self.n-4]
        self.fx[5*self.n-3] = x[self.n*5-3] - self.d[5*self.n-3]
        self.fx[5*self.n-2] = x[self.n*5-2] - self.d[5*self.n-2]
        self.fx[5*self.n-1] = x[self.n*5-1] - self.d[5*self.n-1]

        self.fx = -self.fx