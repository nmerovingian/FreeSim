

class Constants(object):
    NA = 6.022e23  # Avogadro's number
    e0 = 1.602e-19 # Elementary Charge
    F = 96485.33
    R = 8.314  
    T = 298

    @classmethod
    def modifyConstants(cls,input_parameters):
        cls.T= input_parameters.cv_parameters_1[7]



if __name__ == '__main__':
    print(Constants.NA)