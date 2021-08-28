# FreeSim
 An Open-Source Electrochemical Reaction Simulator

FreeSim is a free simultor for electrochemical reaction. It now has implemented 7 mechanisms, including:

* A + e = B, simple one electron reuduction 
* Stochastic A + e = B, stochastic one electron reduction using random walk algorithm
* A + e = B, B + e = C, two electron reduction
* A + e = B, B + B = C, EC2 reaction 
* A + e = B, B = C, EC reaction 
* X = A, A + e = B, CE reaction 
* X = A + C, A + e = B, dissociative CE reaction
* A + e = B， A<sub>abs</sub> + e = B<abs>abs</abs>, one eletctron reduction with adsorbed species, adsorption described with Langmuir Isotherm theory

# Installs
A few common packages including PyQt5, Numpy, Pandas are required to be installed. Python version 3.6 and above is recommended

```
$ pip install PyQt5
$ pip install numpy
$ pip install pandas
```

To run,

```
$ python MainWindow.py
```

# Discailmers
Since the software is offered free of charge under GNU public license, we do not offer gurantees on the results of simulations and offer absolute no warranties to the software. The authors would try their best to correct any bugs as soon as possible. Thank you for your understanding.



