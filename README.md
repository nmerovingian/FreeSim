# FreeSim
 An Open-Source Electrochemical Reaction Simulator

![Intro](Icons/FreeSimIntro.jpg)

FreeSim is a free simultor for electrochemical reaction by Haotian Chen. Part of FreeSim is developed during Haotian's PhD study with Prof. Richard G. Compton at University of Oxford.  
We have now implemented ***7*** mechanisms, including:

* A + e = B, simple one electron reuduction 
* Stochastic A + e = B, stochastic one electron reduction using random walk algorithm
* A + e = B, B + e = C, two electron reduction
* A + e = B, B + B = C, EC2 reaction 
* A + e = B, B = C, EC reaction 
* X = A, A + e = B, CE reaction 
* X = A + C, A + e = B, dissociative CE reaction
* A + e = B， A<sub>abs</sub> + e = B<sub>abs</sub>, one eletctron reduction with adsorbed species, adsorption described with Langmuir Isotherm theory

Most of the mechanism support Butler-Volmer, Nernst and asymmetric Marcus-Hush kinetics. Radial and linear diffusions are also supported in most mechanisms. Prequilibrium of species are supported in CE and dissociative CE reactions. Semi-infinite and thin-layer boundary conditions are supported.

Chronoamperometry of most mechanisms are supported. 


# Installs
A few common packages including PyQt5, pyqtgraph, Sympy, Numpy and Pandas are required to be installed. Python version 3.6 and above is recommended

```
$ pip install PyQt5
$ pip install pyqtgraph
$ pip install matplotlib
$ pip install sympy
$ pip install numpy
$ pip install pandas
$ pip install scipy
```

The packages can also be installed using the *requirement.txt*

```
$ pip install -r requirement.txt
```

To run,

```
$ python MainWindow.py
```
# Finite Difference Simulation Tutorials
The authors have provided a Colab notebook tutorials for voltammetry simulation from scratch. Users interested in learning, applying and advancing voltammetry simulations should try to run and understand simulations. 

A Google Colab  [Notebook](https://colab.research.google.com/drive/1dv3ZKD5io7FAsoq-KWWVFZOnAWLW5cnT?usp=sharing) is provided with the following sections
* My first voltammetry simulation! Linear diffusion, Nernst equation and reproducing the famous RuHex experiment.
  * Simulator: Voltammetry simulation with linear diffusion and Nernst equation boundary condition
  * Exercise: Simulate RuHex reduction and compare with experiment
  * Validation: Validating simulation results with specific equations on peak flux, peak potential, half-wave potential, and peak-to-peak separation
* Butler-Volmer Equation and Electrochemical Reversibility
  * Simulator: Voltammetry simulation with linear diffusion and Butler–Volmer boundary condition
  * Exercise: Using simulation to examine the interplay between scan rate, electrochemical rate constant, and reversibility
  * Validation: Validating simulation with BV kinetics on peak flux and peak potential in the fully irreversible limit
* Spherical Electrode
  * Simulator: Voltammetry simulation with radial diffusion onto a (hemi)spherical electrode with Butler–Volmer or Nernst boundary condition
  * Exercise: Simulate 2-methyl-2-nitropropane (MeNP) reduction at a hemispherical electrode and compare with experiments
* Chronoamperometry at at microdisk electrode (2D Simulation)
  * Simulator: 2D Simulator: Chronoamperometry at a microdisk electrode
  * Validation: Comparing chronoamperogram with Shoup–Szabo equation
* Voltammetry on Rotating Disk Electrode
  * Voltammetry on a rotating disk electrode with convection-diffusion mass transport and Nernst boundary condition
  * Validation: Comparing steady state flux with Levich equation


# Case Studies
Case studies are perfect starting point for simulations. The cases allow you to input simulation parameters according to the parameter guide provided and see the nice agreement with experiments! The cases provided in the *Case Study* folder are:

* Case Study\MeNP reduction at a hemispherical electrode
* Case Study\RuHex Au macroelectrode CV

Each case comes with a *Background and Parameters.md* file for the experimental backgrounds and parameters. An experimental voltammogram is provided too. In addition, if you don't want to type these parameters mannually, **you can just load the *Simulation Seeting.pkl* file and run the simulations!**





# Future plans
The authors may include 2-D simulation of a microdisc elelctrode. You may also leave your preferred mechanism in the discussion forum and we will try our best to consider that! 


# Disclaimers
Since the software is offered free of charge under GNU public license, we do not offer gurantees on the results of simulations and offer absolute no warranties to the software. The authors would try their best to respond to any bugs as soon as possible. Thanks for your understanding.

# Citation 
Please cite the FreeSim paper published at [Journal of Chemical Education](https://pubs.acs.org/doi/full/10.1021/acs.jchemed.5c01092). 


