from PyQt5.QtWidgets import QAction, QBoxLayout, QComboBox, QFormLayout, QGroupBox, QLabel, QListWidget, QMessageBox, QProgressBar, QWidget,QLineEdit,QCheckBox,QRadioButton,QMainWindow,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QApplication,QFileDialog,QGroupBox,QButtonGroup,QToolBar,QTabWidget
import math

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
    pass