import numpy as np
from scipy.special import pbwa
from matplotlib import pyplot as plt

def chronoamperometry_macroElectrode(T):
    """
    The famous cottrell equation for chronoamperometery at a macroelectrode dominated by linear diffusion
    """
    J = 1/(np.sqrt(T*np.pi))
    return J

def chronoamperometry_sphericalElectrode(T):
    """
    The famous cottrell equation for chronoamperometery at a spherical electrode dominated by convergent diffusion
    """

    J = (1+np.sqrt(T*np.pi))/(np.sqrt(T*np.pi))

    return J

def chronoamperometry_microDiskElectrode_Shoup_Szabo(T):

    """
    The famous Schou-Szabo equation for chronoamperometry at a microdisk electrode. 
    Equation 8 of Journal of Electroanalytical Chemistry and Interfacial Electrochemistry,Volume 140, Issue 2, 23 November 1982, Pages 237-245
    The dimensionless time in the original paper was adapted for this work. 
    https://doi.org/10.1016/0022-0728(82)85171-1
    """
    J = 0.7854+0.4431/np.sqrt(T)+0.2146*np.exp(-0.39115/np.sqrt(T))
    return J

def chronoamperometry_microDiskElectrode_Aoki_Osteryoung(T):

    """
    The famous aoki_osteryong equation for chronoamperometery at a microdisk electrode
    Equation 7 and 8 of Journal of Electroanalytical Chemistry and Interfacial Electrochemistry Volume 160, Issues 1–2, 10 January 1984, Pages 335-339
    The dimensionless time in the original paper was adapted for this work. 
    https://doi.org/10.1016/S0022-0728(84)80136-9
    """

    tau = T*4
    flux_part1 = np.where(tau<=1,0.88623*tau**(-0.5)+0.78540+0.094*tau**(0.5),0)
    flux_part2 = np.where(tau>1,1.0+0.71835*tau**(-0.5)+0.05626*tau**(-1.5)-0.00646*tau**(-2.5),0)
    J = flux_part1 + flux_part2
    return J


def chronoamperometry_microbandElectrode_Aoki_short(T):
    """
    This equation is adapted from Equation 60  of JEAC 225(1987) 19-32 for simulation at a short interval. 
    https://doi.org/10.1016/0022-0728(87)80002-5
    """
    def U(a,x):
        return pbwa(a,x)[0]
    J = (np.pi*T)**(-0.5) + 1.0 - ((2.0**0.75)/np.pi)*(T**0.75)*np.exp(-1.0/(8.0*T)) * (U(2.0,(2.0*T)**(-0.5)))

    return J


def chronoamperometry_microbandElectrode_Aoki_long(T):
    """
    This equation is adapted from Equation 63  of JEAC 225(1987) 19-32 with three terms in the long interval. 
    Note that there is a typo in the original paper and the exponent of the last term should be "-2" instead of "2"
    https://doi.org/10.1016/0022-0728(87)80002-5
    """
    J = 2.0*np.pi*((np.log(T)+3.0)**(-1.0))*(1.0-0.577*((np.log(T)+3.0)**(-1.0))-1.312*((np.log(T)+3.0)**(-2)))
    return J


def chronoamperometry_microcylinder_Matsuda(T):
    """
    The Matsuda expression for chronoamperometry at a microcylinder electrode of infinite lengths.
    Equation 6 of Journal of Electroanalytical Chemistry and Interfacial Electrochemistry Volume 186, Issues 1-2, 10 May 1985, Pages 79-86
    https://doi.org/10.1016/0368-1874(85)85756-7
    """

    flux_part1 = np.where(np.log(T)<1.47,1.0/np.sqrt(np.pi*T)+0.422-0.0675*np.log(T)-0.0058*(np.log(T)-1.47)**2,0)
    flux_part2 = np.where(np.log(T)>=1.47,1.0/np.sqrt(np.pi*T)+0.422-0.0675*np.log(T)+0.0058*(np.log(T)-1.47)**2,0)

    J = flux_part1 + flux_part2

    return J
    

def chronoamperometry_microcylinder_Wightman(T,gamma=0.5772156):
    """
    The Wightman approximate solution to chronoamperometry at a microcylinder electrode of infinite lengths
    Equation 5 of Journal of Electroanalytical Chemistry and Interfacial Electrochemistry Volume 217, Issue 2, 10 February 1987, Pages 417-423
    https://doi.org/10.1016/0022-0728(87)80233-4
    """
    J = np.exp(-np.sqrt(np.pi*T)/10)/np.sqrt(np.pi*T) + 1.0/np.log(4*np.exp(-gamma*T)**0.5+np.exp(5.0/3.0)) 
    return J



if __name__ == "__main__":
    T = np.linspace(0,10)
    J1 = chronoamperometry_microDiskElectrode_Aoki_Osteryoung(T)
    J2 = chronoamperometry_microDiskElectrode_Shoup_Szabo(T)

    plt.plot(T,J1,label='Aoki and Osteryoung')
    plt.plot(T,J2,label='SS')
    plt.legend()
    plt.show()