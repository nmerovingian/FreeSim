import json
from collections import OrderedDict
import os
import datetime
class DefaultInput(object):
    def __init__(self) -> None:
        super().__init__()

        self.cv_parameters = {'Estart':0.3,'Erev':-0.3,'Eend':0.3,'Scan Rate':1.0,'Cycles':1,'Ru':0.0,'Cdl':0.0,'Temp':298.15,'cA':1e-4,'cB':0.0,'cC':0.0,'cX':0.0,'Geometry of electrode':0,'Area':1e-6,'Mode of simulation':0}
        self.chemical_parameters = {'Type of mechanism':0,'Formal Potential':0.0,'Reorgnization energy':0.0,'k0':1e7,'ACheck':True,'DA':1e-9,'canalA':0.0,'cinitA':0.0,'BCheck':True,'DB':1e-9,'canalB':0.0,'cinitB':0.0,'CCheck':False,'DC':1e-9,'canalC':0.0,'cinitC':0.0,'DCheck':True,'DD':1e-9,'canalD':0.0,'cinit':0.0}
        self.model_prameters = {'Expanding Grid Factor':0.05,'D*/k*':0.0,'Xmax/SQRT(Dt)':6.0,'R0*':1e-6,'Potential Step':1e-5,'Gaussian-Newton iteration':5,'Gaussian Noise level':0.0,'Expanding grid factor in y direction':0.05}
        self.stochastic_process_parameters = {'Sampling rate':100,'Number of oversampling':500,'Number of molecules':0.0}
        self.cv_parameters_disabled = {}
        self.chemical_parameters_disabled = {}
        self.model_parameters_disabled = {}
        self.cv_parameters_disabled = {}

        self.mechanism_parameters_0 = OrderedDict([(0,3)])

        self.cv_parameters_1 = OrderedDict([(0,0.4),(1,-0.4),(2,0.4),(3,1.0),(4,1),(5,0.0),(6,0.0),(7,298),(8,0.0),(9,0.0)])
        self.cv_parameters_10 = OrderedDict([(0,1e-5),(1,0.0),(2,0.0),(3,0.0),(4,0.0)])
        self.cv_parameters_11 = OrderedDict([(0,0),(1,1e-5)])
        self.cv_parameters_12 = OrderedDict([(0,0)])

        self.chemical_parameters_2 = OrderedDict([(0,0),(1,0.0),(2,0.0),(3,1.0),(4,0.5),(5,1),(6,-0.2),(7,0.0),(8,1.0),(9,0.5)])
        self.chemical_parameters_21 = OrderedDict([(0,''),(1,0.0),(2,''),(3,0.0),(4,False)])
        self.chemical_parameters_22 = OrderedDict([(0,True),(1,1e-9),(2,1e-5),(3,1e-5),(4,True),(5,1e-9),(6,0.0),(7,0.0),(8,False),(9,1e-9),(10,0.0),(11,0.0),(12,False),(13,1e-9),(14,0.0),(15,0.0),(16,False),(17,1e-9),(18,0.0),(19,0.0)])



        self.model_parameters_3 = OrderedDict([(0,0.05),(1,0),(2,6.0),(3,1e-8)])
        self.model_parameters_30 = OrderedDict([(0,5e-3),(1,6),(2,0.0)])
        self.model_parameters_31 = OrderedDict([(0,0.05)])

        self.stochastic_process_parameters_4 = OrderedDict([(0,100),(1,500),])
        self.stochastic_process_parameters_40 = OrderedDict([(0,0),(1,True)])

        self.adsorption_parameters_5 = OrderedDict([(0,0.0),(1,0.0),(2,0.0),(3,0.0),(4,0.0),(5,0.0),(6,0.0),(7,0.0),(8,0.0)])
        self.adsorption_parameters_50 = OrderedDict([(0,1.0),(1,0.5)])



        self.cv_parameters_enabled_1 = OrderedDict([(5,False),(6,False),(8,False),(9,False)])
        self.cv_parameters_enabled_10 = OrderedDict()
        self.cv_parameters_enabled_11 = OrderedDict()
        self.cv_parameters_enabled_12 = OrderedDict()


        self.chemical_parameters_enabled_2 = OrderedDict()
        self.chemical_parameters_enabled_21 = OrderedDict()
        self.chemical_parameters_enabled_22 = OrderedDict()

        self.model_parameters_enabled_3= OrderedDict()
        self.model_parameters_enabled_30 = OrderedDict()
        self.model_parameters_enabled_31 = OrderedDict()
        
        self.stochastic_parameters_enabled_4= OrderedDict()
        self.stochastic_parameters_enabled_40 = OrderedDict()
        self.adsorption_parameters_enabled_5 = OrderedDict([(0,False),(1,False),(2,False),(3,False),(4,False),(5,False),(6,False),(7,False),(8,False)])
        self.adsorption_parameters_enabled_50 = OrderedDict([(0,False),(1,False)])

        self.chemical_parameters_hided_21 = OrderedDict([(1,True)])
        
        self.file_options_parameters = OrderedDict([(0,True),(1,os.getcwd() + '\Data'),(2,datetime.datetime.now().strftime(r'%Y-%m-%d')),(3,False),(4,False),(5,True)])

class Mechanism0Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[2] = False
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_enabled_22[8] = False 
        self.chemical_parameters_enabled_22[9] = False 
        self.chemical_parameters_enabled_22[10] = False 
        self.chemical_parameters_enabled_22[11] = False 
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_enabled_21[0] = False
        self.chemical_parameters_enabled_21[1] = False 
        self.chemical_parameters_enabled_21[2] = False 
        self.chemical_parameters_enabled_21[3] = False
        self.chemical_parameters_enabled_21[4] = False 
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False
class Mechanism1Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()


        self.cv_parameters_11[1] = 1e-7
        self.cv_parameters_enabled_10[2] = False
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_enabled_22[8] = False 
        self.chemical_parameters_enabled_22[9] = False 
        self.chemical_parameters_enabled_22[10] = False 
        self.chemical_parameters_enabled_22[11] = False 
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_enabled_21[0] = False
        self.chemical_parameters_enabled_21[1] = False 
        self.chemical_parameters_enabled_21[2] = False 
        self.chemical_parameters_enabled_21[3] = False
        self.chemical_parameters_enabled_21[4] = False

class Mechanism2Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_2[0] = 1
        self.chemical_parameters_2[3] = 1
        self.chemical_parameters_22[8] = True
        self.chemical_parameters_enabled_2[0] = False
        self.chemical_parameters_enabled_2[5] = False
        self.chemical_parameters_enabled_2[2] = False
        self.chemical_parameters_enabled_2[7] = False
        self.chemical_parameters_enabled_21[4] = False
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_hided_21 = OrderedDict([(1,False)])
        self.chemical_parameters_21[0] = 'k<sub>comp</sub>, M<sup>-1</sup>s<sup>-1</sup>'
        self.chemical_parameters_21[2] = 'k<sub>disp</sub>, M<sup>-1</sup>s<sup>-1</sup>'

        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False

class Mechanism3Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_22[8] = True
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_21[0] = 'k<sub>f</sub>, M<sup>-1</sup>s<sup>-1</sup>'
        self.chemical_parameters_21[2] = 'k<sub>b</sub>, s<sup>-1</sup>'
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False

class Mechanism4Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_22[8] = True
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_21[0] = 'k<sub>f</sub>, s<sup>-1</sup>'
        self.chemical_parameters_21[2] = 'k<sub>b</sub>, s<sup>-1</sup>'
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False


class Mechanism5Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[2] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_22[12] = True
        self.chemical_parameters_enabled_22[8] = False 
        self.chemical_parameters_enabled_22[9] = False 
        self.chemical_parameters_enabled_22[10] = False 
        self.chemical_parameters_enabled_22[11] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_21[0] = 'k<sub>f</sub>, s<sup>-1</sup>'
        self.chemical_parameters_21[2] = 'k<sub>b</sub>, s<sup>-1</sup>'
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False


class Mechanism6Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_22[8] = True
        self.chemical_parameters_22[12] = True
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_21[0] = 'k<sub>f</sub>, M<sup>-1</sup>s<sup>-1</sup>'
        self.chemical_parameters_21[2] = 'k<sub>b</sub>, s<sup>-1</sup>'
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.stochastic_parameters_enabled_40[1] = False

class Mechanism7Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()
        self.cv_parameters_enabled_10[2] = False
        self.cv_parameters_enabled_10[3] = False
        self.cv_parameters_enabled_10[4] = False
        self.chemical_parameters_2[0] = 1
        self.chemical_parameters_enabled_2[0] = False
        self.chemical_parameters_enabled_22[8] = False 
        self.chemical_parameters_enabled_22[9] = False 
        self.chemical_parameters_enabled_22[10] = False 
        self.chemical_parameters_enabled_22[11] = False 
        self.chemical_parameters_enabled_22[12] = False 
        self.chemical_parameters_enabled_22[13] = False 
        self.chemical_parameters_enabled_22[14] = False 
        self.chemical_parameters_enabled_22[15] = False
        self.chemical_parameters_enabled_22[16] = False 
        self.chemical_parameters_enabled_22[17] = False 
        self.chemical_parameters_enabled_22[18] = False
        self.chemical_parameters_enabled_22[19] = False
        self.chemical_parameters_enabled_21[0] = False
        self.chemical_parameters_enabled_21[1] = False 
        self.chemical_parameters_enabled_21[2] = False 
        self.chemical_parameters_enabled_21[3] = False
        self.chemical_parameters_enabled_21[4] = False 
        self.stochastic_parameters_enabled_4[0]= False
        self.stochastic_parameters_enabled_4[1] = False
        self.stochastic_parameters_enabled_40[0] = False
        self.adsorption_parameters_enabled_5 = OrderedDict([(5,False),(6,False),(7,False)])
        self.adsorption_parameters_enabled_50 = OrderedDict()
        self.adsorption_parameters_5[0] = 0.1
        self.adsorption_parameters_5[1] = 10.0
        self.adsorption_parameters_5[2] = 1.0
        self.adsorption_parameters_5[3] = 1.0
        self.adsorption_parameters_5[4] = 1.0
        self.adsorption_parameters_5[5] = 0.0
        self.adsorption_parameters_5[6] = 0.0
        self.stochastic_parameters_enabled_40[1] = False


class Mechanism8Input(DefaultInput):
    def __init__(self) -> None:
        super().__init__()


class userInputParameters(DefaultInput):
    def __init__(self) -> None:
        super().__init__()

        self.ViewOption = OrderedDict([(0,False),(1,False),(2,False)])
