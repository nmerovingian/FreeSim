from errno import EPIPE
from PyQt5.QtWidgets import QAction, QBoxLayout, QComboBox, QFormLayout, QGroupBox, QLabel, QListWidget, QMessageBox, QProgressBar, QWidget,QLineEdit,QCheckBox,QRadioButton,QMainWindow,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QApplication,QFileDialog,QGroupBox,QButtonGroup,QToolBar,QTabWidget
import math
from scipy.integrate import quad
import numpy as np

def getValue(widget):
    if isinstance(widget,QLineEdit):
        return float(widget.text())
    elif isinstance(widget,QCheckBox):
        return bool(widget.isChecked())
    elif isinstance(widget,QComboBox):
        return int(widget.currentIndex())
    elif isinstance(widget,QCheckBox):
        return widget.isChecked()


def setDisabled(widget):
    if isinstance(widget,QLineEdit):
        widget.setEnabled(False)
    elif isinstance(widget,QCheckBox):
        widget.setEnabled(False)
    elif isinstance(widget,QComboBox):
        widget.setEnabled(False)
    elif isinstance(widget,QPushButton):
        widget.setEnabled(False)



def setEnabled(widget):
    if isinstance(widget,QLineEdit):
        widget.setEnabled(True)
    elif isinstance(widget,QCheckBox):
        widget.setEnabled(True)
    elif isinstance(widget,QComboBox):
        widget.setEnabled(True)
    elif isinstance(widget,QPushButton):
        widget.setEnabled(True)



def setHided(widget):
    if isinstance(widget,QWidget):
        widget.hide()
def setVisible(widget):
    if isinstance(widget,QWidget):
        widget.show()



def toDimensional(potential,fluxes,geometry,dElectrode,lElectrode,E0f,Temperature,Dref,cRef):
    potential = potential / (96485/(8.314*Temperature)) + E0f
    if geometry == 0:
        fluxes = math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 1:
        fluxes = 2*math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 2:
        fluxes = 4*math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 4:
        fluxes = 2*math.pi*lElectrode*96485*Dref*cRef*fluxes
    else:
        raise ValueError

    return potential,fluxes


def toDimensionalCA(time,fluxes,geometry,dElectrode,lElectrode,E0f,Temperature,Dref,cRef):
    
    time = time*dElectrode*dElectrode/Dref

    if geometry == 0:
        fluxes = math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 1:
        fluxes = 2*math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 2:
        fluxes = 4*math.pi*dElectrode*96485*Dref*cRef*fluxes
    elif geometry == 4:
        fluxes = 2*math.pi*lElectrode*96485*Dref*cRef*fluxes
    else:
        raise ValueError

    return time,fluxes


def calMHInt(theta,Lambda,gamma,red=True):
    """
    Lambda:Dimensionless reorgnization energy
    theta: dimensionless overpotential 
    gamma: asymmetric parameter taking value between -1 and 1
    """
    if red:
        def intexp(epsilon):
            term1 = Lambda/4 * (1 + (theta+epsilon)/Lambda) ** 2
            term2 = gamma*(theta+epsilon)/4 * (1-((theta+epsilon)/Lambda)**2)
            term3 = Lambda/16*gamma*gamma
            deltaG = term1+ term2 + term3
            return np.exp(-deltaG)/(1+np.exp(-epsilon)) 

    else:
        def intexp(epsilon):
            term1 = Lambda/4 * (1 - (theta+epsilon)/Lambda) ** 2
            term2 = gamma*(theta+epsilon)/4 * (1-((theta+epsilon)/Lambda)**2)
            term3 = Lambda/16*gamma*gamma
            deltaG = term1+ term2 + term3
            return np.exp(-deltaG)/(1+np.exp(+epsilon)) 

    return quad(intexp,-50,50)[0]



def calMH(K0,theta,Lambda,gamma):
    """
    Calculate rate constants using asymmetric Macus-Hush theory
    K0: dimensionless electrochemical rate constant
    theta: dimensionless overpotential 
    Lambda:Dimensionless reorgnization energy
    gamma: asymmetric parameter taking value between -1 and 1. Whe gamma == 0, it is the well-known symmetric MH equation
    """

    # The dimensionless activation energy of the reduction/oxidation processes in the asymmertic version of MH is calculated as: 
    IRed = calMHInt(theta,Lambda,gamma,red=True)
    IRedBase = calMHInt(0.0,Lambda,gamma,red=True)
    IOx = calMHInt(theta,Lambda,gamma,red=False)
    IOxBase = calMHInt(0.0,Lambda,gamma,red=False)

    Kred = K0 * IRed/IRedBase
    Kox = K0 * IOx/IOxBase
    return Kred,Kox




    

