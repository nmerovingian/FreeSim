import math
import sys


class Parameters(object):

    # Scan Rate 
    v = 1.0

    # cycles
    cycles = 2

    # target concentrtaion before discretisation , mol/m^3
    c0 = 1e-2

    dElectrode = 100e-9
    #Electrode surface area , radius is 100 nm
    A = math.pi * dElectrode * dElectrode

    # formal potential, V 

    EF = 0.0 

    # Min Elctrode potential 
    EMin = -0.2 

    # Max Electrode Potential 
    EMax = 0.2

    # diffusion coefficient [m^2 s^-1]
    D = 1e-9 

    # Sampling rate potentialstat, Hz 
    fs = 500.0

    # oversampling in the random walk
    # (f_rw = nOversampling * f_s)
    nOversampling = 100 


    # length of the simulated time interval [s]
    tMax =0.0

    # width of the simulated space, m
    xMax = 0.0 

    # number of molecules

    nMolecules  = 0.0 


    # number of time steps

    nTimeSteps  = 0.0 

    # Random Walk Temporal Step Length [s]
    dt = 0.0

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def modifyDefaultParameters(cls,input_parameters):
        directory = input_parameters.file_options_parameters[1]
        file_name = input_parameters.file_options_parameters[2]
        if input_parameters.file_options_parameters[3] == 0:
            file_type ='.txt'
        elif input_parameters.file_options_parameters[3] == 1:
            file_type ='.csv'
        else:
            raise ValueError('Unknwon file type')
        cls.output_file_name = f'{directory}/{file_name}{file_type}'
        cls.EMax= input_parameters.cv_parameters_1[0] # starting potential
        cls.EMin = input_parameters.cv_parameters_1[1] # Ereverse 
        cls.V = input_parameters.cv_parameters_1[3]
        cls.cycles = int(float(input_parameters.cv_parameters_1[4]))
        cls.c0 = input_parameters.cv_parameters_10[0] * 1000
        cls.D = input_parameters.chemical_parameters_22[1]
        cls.dElectrode = input_parameters.cv_parameters_11[1]
        cls.A =cls.dElectrode * cls.dElectrode * math.pi

        


    @classmethod
    def evalImplicitParameters(cls,c):
        cls.tMax = 2.0 * (cls.EMax - cls.EMin)/cls.v * cls.cycles
        cls.xMax = 6.0 * math.sqrt(cls.D * cls.tMax)
        cls.nMolecules = int(c.NA * cls.c0 * cls.xMax * cls.A) 
        cls.nTimeSteps = int(cls.tMax * cls.fs * cls.nOversampling)
        cls.dt = 1.0 / cls.fs / cls.nOversampling





if __name__ == "__main__":
    from Constants import Constants
    Parameters.evalImplicitParameters(Constants)

    print(Parameters.nMolecules) 






