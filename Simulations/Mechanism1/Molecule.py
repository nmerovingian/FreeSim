import numpy as np
import math
class Molecule(object):
    def __init__(self,xInit,p,c) -> None:
        self.Oxidized = True
        self.position = xInit * p.xMax
        self.p = p
        self.c = c

        # evaluate random walk displacement\
        self.dx = math.sqrt(2.0*self.p.D * self.p.dt)

    def move(self,up):
        # evaluate random walk, return true if contact with electrode 
        # random walk

        if up:
            self.position += self.dx

        else :
            self.position -= self.dx

        # Check electrode boundary
        if self.position <= 0.0:
            self.position = - self.position
            return True

        # check upper boundary 

        if self.position >= self.p.xMax:
            self.position = 2.0 * self.p.xMax - self.position

        return False 




    def evalChargeTransfer(self,E,r):
        # calculate the probability of the molecule being oxidised.
        p_ox = math.exp(self.c.F/self.c.R/self.c.T * E) / (1.0 + math.exp(self.c.F / self.c.R / self.c.T * E))

        # initialize aux variable
        currentContrib = 0.0

        # evaluate current 
        if (r < p_ox):
            if not self.Oxidized:
                currentContrib = self.c.e0 / self.p.dt
                self.Oxidized = True 

        else:
            if self.Oxidized:
                currentContrib = - self.c.e0 / self.p.dt

            self.Oxidized = False


        # return results
        
        return currentContrib

    