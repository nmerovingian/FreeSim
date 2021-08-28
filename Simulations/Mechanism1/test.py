from matplotlib import pyplot as plt 
import pandas as pd 
import numpy as np


df = pd.read_csv('data.txt',header=None)

df.plot(x=1,y=2)

plt.show()


