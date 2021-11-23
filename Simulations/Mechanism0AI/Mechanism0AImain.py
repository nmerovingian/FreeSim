import tensorflow as tf 
from tensorflow.keras.layers import Dense,BatchNormalization,Dropout,Input
from tensorflow.keras.models import Sequential,Model
import numpy as np
import math
import pandas as pd

theta_i = -1.0*96485/(298*8.314)
theta_v = 1.0*96485/(298*8.314)
forward_theta = np.linspace(theta_i,theta_v,num=100)
reverse_theta = np.linspace(theta_v,theta_i,num=100)

scan = np.concatenate((forward_theta,reverse_theta))


meta_dict = {'Nernst':0,'BV':1,'linear':0,'radial':1}
kinetics_index_dict = {0:'BV'}
diffusion_index_dict = {0:'linear',1:'radial'}



def create_model_flux(input_shape,output_shape=None,optimizer='Adam',loss='mean_absolute_error',activation='relu'):
    model = Sequential()
    model.add(Dense(512,input_dim =input_shape ,activation=activation))
    model.add(Dense(1024,activation=activation))
    model.add(Dense(2048,activation=activation))
    model.add(Dense(4096,activation=activation))
    model.add(Dense(output_shape,activation='linear'))
    model.compile(optimizer=optimizer,loss=loss,metrics=['mean_squared_error','mean_absolute_error'])
    return model



def load_parameter(input_parameters):
    sigma = input_parameters.AI_parameters_60[3]
    dB = input_parameters.AI_parameters_60[8]
    K0 = input_parameters.AI_parameters_60[9]
    alpha = input_parameters.AI_parameters_60[10]
    kinetics_index = input_parameters.AI_parameters_60[11]
    diffusion_index = input_parameters.AI_parameters_60[12]
    kinetics = meta_dict[kinetics_index_dict[kinetics_index]]
    diffusion = meta_dict[diffusion_index_dict[diffusion_index]]

    return np.array([[np.log10(sigma),0.0,0.0,np.log10(K0),alpha,np.log10(dB),kinetics,diffusion]])
    


def saveVoltammogram(voltammogram,output_file_name,dimensional = True,Temperature = None, E0f=None,dElectrode = None,Dref=None,cref=None):
    df = pd.DataFrame(voltammogram,columns=['Potential,V','Current,A'])
    if dimensional:
        df.iloc[:,0] = df.iloc[:,0] / (96485/(8.314*Temperature)) + E0f

        df.iloc[:,1] = df.iloc[:,1] * math.pi*dElectrode*96485*Dref*cref

    df.to_csv(output_file_name,index=False)

def Mechanism_0_AI_single_thread_GUI(signals,input_parameters) -> None:

    directory = input_parameters.file_options_parameters[1]
    file_name = input_parameters.file_options_parameters[2]
    dimensional = input_parameters.file_options_parameters[5]
    Temperature = input_parameters.AI_parameters_6[12]
    sigma = input_parameters.AI_parameters_60[3]
    E0f = input_parameters.AI_parameters_6[2]
    dElectrode = input_parameters.AI_parameters_6[13]
    Dref = input_parameters.AI_parameters_6[7]
    cref = input_parameters.AI_parameters_6[5]

    if input_parameters.file_options_parameters[3] == 0:
        file_type ='.txt'
    elif input_parameters.file_options_parameters[3] == 1:
        file_type ='.csv'
    else:
        raise ValueError('Unknwon file type')
    output_file_name = f'{directory}/{file_name}{file_type}'


    vars = load_parameter(input_parameters)
    model = create_model_flux(8,200)
    model.load_weights('./Simulations/Mechanism0AI/weights.h5')
    pred = model.predict(vars)
    pred *= np.sqrt(sigma) # now denormalize the voltammogram
    Voltammogram = np.stack([scan,pred[0]],axis=1)

    saveVoltammogram(Voltammogram,output_file_name,dimensional,Temperature,E0f,dElectrode,Dref,cref)


    signals.output_file_name.emit(output_file_name)



    

