__author__ = 'Haotian Chen'
from tkinter.tix import Tree
from pyqtgraph.graphicsItems.PlotDataItem import dataType
from pyqtgraph.widgets.LayoutWidget import LayoutWidget
from PyQt5 import QtCore
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot 
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QBoxLayout, QComboBox, QFormLayout, QGroupBox, QLabel, QListWidget, QMessageBox, QProgressBar, QWidget,QLineEdit,QCheckBox,QRadioButton,QMainWindow,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QApplication,QFileDialog,QGroupBox,QButtonGroup,QToolBar,QTabWidget,QActionGroup,QStackedWidget,QScrollBar
from PyQt5.QtCore import QFile, QLine, QRect, QRunnable, QTimer, Qt,QSize,QThread,QThreadPool,QObject, pyqtBoundSignal, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon,QPixmap
import sys
import datetime
import json
import pickle
import os
import pandas as pd
import numpy as np
import sympy
import itertools
import time
import math
from pyqtgraph.widgets.TableWidget import TableWidget
from collections import OrderedDict
from InputParameters import DefaultInput, userInputParameters,Mechanism0Input,Mechanism1Input,Mechanism2Input,Mechanism3Input,Mechanism4Input,Mechanism5Input,Mechanism6Input,Mechanism7Input,Mechanism8Input
from helper import getValue,setDisabled,setEnabled,setHided,setVisible
from LabelInput import LabelDirInput


TIME_LIMIT = 100

class WorkerSignal(QObject):
    """
    Defines the signals available from a running worker thread
    """
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    started = pyqtSignal()
    concProfile = pyqtSignal(np.ndarray)
    fluxesProfile = pyqtSignal(np.ndarray)
    output_file_name  = pyqtSignal(str)

class SimulationWorker(QRunnable):
    def __init__(self,input_parameters):
        super().__init__()
        self.signals = WorkerSignal()
        self.input_parameters = input_parameters


    @pyqtSlot()
    def run(self):
        if self.input_parameters.mechanism_parameters_0[1] == 'CV':
            if self.input_parameters.mechanism_parameters_0[0] in [1]:
                from Simulations.Mechanism1.Mechanism1main import Mechanism_1_simulation_single_thread_GUI
                Mechanism_1_simulation_single_thread_GUI(self.signals,self.input_parameters)
            elif self.input_parameters.mechanism_parameters_0[0] in [0,3,4,5,6]:
                from Simulations.Mechanism4.Mechanism03456main import Mechanism_03456_simulation_single_thread_Gui
                Mechanism_03456_simulation_single_thread_Gui(self.signals,self.input_parameters)
            elif self.input_parameters.mechanism_parameters_0[0] in [2]:
                from Simulations.Mechanism2.Mechanism2main import Mechanism_2_simulation_single_thread_Gui
                Mechanism_2_simulation_single_thread_Gui(self.signals,self.input_parameters)
            elif self.input_parameters.mechanism_parameters_0[0] in [7]:
                from Simulations.Mechanism7.Mechanism7main import Mechanism_7_simulation_single_thread_Gui
                Mechanism_7_simulation_single_thread_Gui(self.signals,self.input_parameters)
            else:
                raise ValueError('Unsuppoted type')
        elif self.input_parameters.mechanism_parameters_0[1] == 'CA':
            if self.input_parameters.mechanism_parameters_0[0] in [0,3,4,5,6]:
                from Simulations.Mechanism4CA.Mechanism03456main import Mechanism_03456_simulation_single_thread_Gui
                Mechanism_03456_simulation_single_thread_Gui(self.signals,self.input_parameters)
        elif self.input_parameters.mechanism_parameters_0[1] =='AI':
            if self.input_parameters.mechanism_parameters_0[0] in [0]:
                from Simulations.Mechanism0AI.Mechanism0AImain import Mechanism_0_AI_single_thread_GUI
                Mechanism_0_AI_single_thread_GUI(self.signals,self.input_parameters)
            




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('FreeSim, Open-Source Electrochemical Reaction Simulator V1.0')

        self.layout = QVBoxLayout()

        self.widget = QWidget()
        self.tableWidget = MyTableWidget()
        self.button_start_simulation = QPushButton('Start Simulation')
        self.button_start_simulation.clicked.connect(self.onStartSimulation)
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(100)
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.onFileListDoubleClicked)
        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.button_start_simulation)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.progressbar)
        self.widget.setLayout(self.layout)
        self.createMenu()
        self.setCentralWidget(self.widget)
        self.setWindowIcon(QIcon('./Icons/CV-icon.png'))
        self.setGeometry(QRect(0,0,800,600))

        # Load default parameters after start
        self.tableWidget.loadInputParameters()
        self.threadpool = QThreadPool()
    

        self.graphWindow = None 
        self.graphWindowOverlay = None
        self.liveConcProfileWindow = None
        self.liveConcProfileWindowLineRef = OrderedDict() 
        self.liveSimulationWindow = None
        self.liveSimulationWindowLineRef = OrderedDict()


        
        



    
    def createMenu(self):
        button_action = QAction(QIcon('./Icons/ScreenShotIcon.png'),'&ScreenShot',self)
        button_action.triggered.connect(self.onScreenShot)
        button_action2 = QAction(QIcon('./Icons/ChemistIcon.png'),'&Authors',self)
        button_action2.triggered.connect(self.onAuthors)
        button_action3 = QAction(QIcon('./Icons/ClearIcon.png'),'&Clear Inputs',self)
        button_action3.triggered.connect(self.clearCommands)
        button_action4 = QAction(QIcon('./Icons/SetDefault.jpg'),'&Restore Default',self)
        button_action4.triggered.connect(lambda checked: self.tableWidget.loadInputParameters())
        button_action5 = QAction(QIcon('./Icons/OpenFile.png'),'&OpenFile',self)
        button_action5.triggered.connect(self.openFile)
        button_action6 = QAction(QIcon('./Icons/SimulationIcon.png'),'&Live Simulation',self)
        button_action6.setCheckable(True)
        button_action6.triggered.connect(self.onLiveSimulation)
        button_action7 = QAction(QIcon('./Icons/LiveConcProfile.png'),'&Live Conc Profile',self)
        button_action7.triggered.connect(self.onLiveConcProfile)
        button_action7.setCheckable(True)
        button_action8 = QAction(QIcon('./Icons/SaveSettingIcon.png'),'&Save Setting',self)
        button_action8.triggered.connect(self.onSaveSetting)
        button_action9 = QAction(QIcon('./Icons/LoadSettingIcon.png'),'&Load Setting',self)
        button_action9.triggered.connect(self.onLoadSetting)
        button_action10 = QAction(QIcon('./Icons/OverlayIcon.png'),'&Overlay',self)
        button_action10.triggered.connect(self.onOverlay)
        button_action10.setCheckable(True)
        button_action11 = QAction(QIcon('./Icons/CV-Icon.png'),'&Cyclic Voltammetry',self)
        button_action11.setCheckable(True)
        button_action11.toggled.connect(self.tableWidget.onCVModeToggled)
        button_action11.setChecked(True)
        button_action12 = QAction(QIcon('./Icons/CA-Icon.png'),'&Chronoamperometry',self)
        button_action12.setCheckable(True)
        button_action12.toggled.connect(self.tableWidget.onCAModeToggled)
        button_action13 = QAction(QIcon('./Icons/AI-icon.png'),'&CV (AI prediction) ')
        button_action13.toggled.connect(lambda:(self.tableWidget.onAIModeToggled(),self.tfInstalled()))
        button_action13.setCheckable(True)
        button_action14 = QAction(QIcon('./Icons/Dimension.png'),'&Dimensionless',self)
        button_action14.toggled.connect(self.onDimension)
        button_action14.setCheckable(True)

        button_group0 = QActionGroup(self)
        button_group0.addAction(button_action11)
        button_group0.addAction(button_action12)
        button_group0.addAction(button_action13)


        self.menu = self.menuBar()
        file_menu = self.menu.addMenu('&File')
        file_menu.addAction(button_action5)
        file_menu.addAction(button_action)
        file_menu.addAction(button_action3)
        file_menu.addAction(button_action4)
        file_menu.addAction(button_action8)
        file_menu.addAction(button_action9)

        mode_menu = self.menu.addMenu('&Mode')
        mode_menu.addAction(button_action11)
        mode_menu.addAction(button_action12)
        mode_menu.addSeparator()
        mode_menu.addAction(button_action13)

        view_menu = self.menu.addMenu('&View')
        view_menu.addAction(button_action6)
        view_menu.addAction(button_action7)
        view_menu.addAction(button_action10)
        view_menu.addAction(button_action14)

        about_menu = self.menu.addMenu('&About')
        about_menu.addAction(button_action2)

    def onScreenShot(self):
        screen = QApplication.primaryScreen()
        screen = screen.grabWindow(self.winId())
        screen.save(f"screenshot-{datetime.datetime.now().strftime(r'%Y-%m-%d %H%M%S')}.jpg",'jpg')
        print('Save screenshot success!')
    def onAuthors(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('About Authors')
        dlg.setText('GUI and Simulation: <a href = "mailto: haotian.chen@lmh.ox.ac.uk">Haotian Chen</a><br><br>General Enquiry: <a href = "mailto: richard.compton@chem.ox.ac.uk">Professor Richard Compton</a><br><br>We would like to hear your experience!')
        button = dlg.exec_()
    def clearCommands(self):
        print('Not implemented yet')

    def onSaveSetting(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Save your setting","","Pickle File (*.pkl)", options=options)
        if fileName:
            with open(f'{fileName}',mode='wb') as f:
                self.tableWidget.getUserInput()
                pickle.dump(self.tableWidget.userParameter,f)

    def onLoadSetting(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Load your setting", "","Pickle File (*.pkl)", options=options)
        if fileName:
            with open(fileName,mode='rb') as f:
                userInput = pickle.load(f)
                self.tableWidget.button_group.button(userInput.mechanism_parameters_0[0]).setChecked(True)
                self.tableWidget.loadInputParameters(userInput)

        


    def onLiveSimulation(self,checked):
        self.tableWidget.userParameter.ViewOption[0] = checked
    def onLiveConcProfile(self,checked):
        self.tableWidget.userParameter.ViewOption[1] = checked
    def onOverlay(self,checked):
        self.tableWidget.userParameter.ViewOption[2] = checked
    def onDimension(self,checked):
        self.tableWidget.userParameter.ViewOption[3] = checked


    @pyqtSlot(str)
    def onOutputFileName(self,filename):
        self.file_list.addItem(filename)

    def openFile(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Text File (*.txt);;Excel File (*.xls | *xlsx);;CSV File (*.csv)", options=options)
        if files:
            print(files)
            self.updateFileList(files=files)

    def updateFileList(self,files):
        self.file_list.addItems(files)

    def determineLabelTitle(self):
        if self.tableWidget.userParameter.mechanism_parameters_0[1] == 'CV':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Potential,\u03B8'
                ylabel = 'Flux, J'
                title ='Preview of Voltammogram, dimensionless'
            else:
                xlabel = 'Potential, V'
                ylabel = 'Current, A'
                title = 'Preview of Voltammogram'
        elif self.tableWidget.userParameter.mechanism_parameters_0[1] == 'CA':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Time, T'
                ylabel = 'Flux, J'
                title ='Preview of Chronoamperogram, dimensionless'
            else:
                xlabel = 'Time, s'
                ylabel = 'Current, A'
                title = 'Preview of Chronoamperogram'
        elif self.tableWidget.userParameter.mechanism_parameters_0[1] == 'AI':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Potential,\u03B1'
                ylabel = 'Flux, J'
                title ='Preview of Voltammogram, dimensionless'
            else:
                xlabel = 'Potential, V'
                ylabel = 'Current, A'
                title = 'Preview of Voltammogram'
        else:
            xlabel = 'Potential, V'
            ylabel = 'Current, A'
            title = 'Preview of Voltammogram'

        return xlabel,ylabel,title

    def onFileListDoubleClicked(self,item):
        print('double clicked')
        selectedFile = item.text()

        xlabel,ylabel,title = self.determineLabelTitle()


        # No overlay
        if self.tableWidget.userParameter.ViewOption[2] == False: 
            if self.graphWindow is None or isinstance(self.graphWindow,GraphWindow):
                self.graphWindow = GraphWindow()
                self.graphWindow.graphWidget.setBackground('w')
                
                if os.path.splitext(selectedFile)[1] == '.csv' or os.path.splitext(selectedFile)[1] =='.txt':
                    df = pd.read_csv(selectedFile)


                    pen = pg.mkPen(width=5,color=(0,0,0))
                    self.graphWindow.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen)
                    
                    self.graphWindow.graphWidget.setLabel('bottom',xlabel,**self.graphWindow.styles)
                    self.graphWindow.graphWidget.setLabel('left',ylabel,**self.graphWindow.styles)
                    self.graphWindow.graphWidget.setTitle(title,**self.graphWindow.styles)

                    self.graphWindow.graphWidget.showGrid(x=True,y=True)
                elif os.path.splitext(selectedFile)[1] =='.xls' or os.path.splitext(selectedFile)[1] =='.xlsx': 
                    df_dict = pd.read_excel(selectedFile,sheet_name=None)
                    # add legend
                    self.graphWindow.graphWidget.addLegend()
                    for key,df in df_dict.items():
                        pen = pg.mkPen(width=5,color=next(self.graphWindow.colorCycle))
                        self.graphWindow.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen,name=key)
                    
                    self.graphWindow.graphWidget.setLabel('bottom',xlabel,**self.graphWindow.styles)
                    self.graphWindow.graphWidget.setLabel('left',ylabel,**self.graphWindow.styles)
                    self.graphWindow.graphWidget.setTitle(title,**self.graphWindow.styles)

                    self.graphWindow.graphWidget.showGrid(x=True,y=True)
                else:
                    raise TypeError(f'Unsupported file type {os.path.splitext(selectedFile)[1]} ')
            
                self.graphWindow.show()
        
        else:
            # Now requires overlay
            if self.graphWindowOverlay is None or not self.graphWindowOverlay.isVisible():
                # If it does not exist or is not visible, instantiate it.
                self.graphWindowOverlay = GraphWindow()
                self.graphWindowOverlay.graphWidget.setBackground('w')
                
                if os.path.splitext(selectedFile)[1] == '.csv' or os.path.splitext(selectedFile)[1] =='.txt':
                    df = pd.read_csv(selectedFile)

                    self.graphWindowOverlay.graphWidget.addLegend()
                    pen = pg.mkPen(width=5,color=next(self.graphWindowOverlay.colorCycle))
                    self.graphWindowOverlay.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen,name=f'{selectedFile}')
                    
                    self.graphWindowOverlay.graphWidget.setLabel('bottom',xlabel,**self.graphWindowOverlay.styles)
                    self.graphWindowOverlay.graphWidget.setLabel('left',ylabel,**self.graphWindowOverlay.styles)
                    self.graphWindowOverlay.graphWidget.setTitle(title,**self.graphWindowOverlay.styles)

                    self.graphWindowOverlay.graphWidget.showGrid(x=True,y=True)
                elif os.path.splitext(selectedFile)[1] =='.xls' or os.path.splitext(selectedFile)[1] =='.xlsx': 
                    df_dict = pd.read_excel(selectedFile,sheet_name=None)
                    # add legend
                    self.graphWindowOverlay.graphWidget.addLegend()
                    for key,df in df_dict.items():
                        pen = pg.mkPen(width=5,color=next(self.graphWindowOverlay.colorCycle))
                        self.graphWindowOverlay.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen,name=f'{selectedFile}/{key}')
                    
                    self.graphWindowOverlay.graphWidget.setLabel('bottom',xlabel,**self.graphWindowOverlay.styles)
                    self.graphWindowOverlay.graphWidget.setLabel('left',ylabel,**self.graphWindowOverlay.styles)
                    self.graphWindowOverlay.graphWidget.setTitle(title,**self.graphWindowOverlay.styles)

                    self.graphWindowOverlay.graphWidget.showGrid(x=True,y=True)
                else:
                    raise TypeError(f'Unsupported file type {os.path.splitext(selectedFile)[1]} ')
                    
                self.graphWindowOverlay.show()
            elif isinstance(self.graphWindowOverlay,GraphWindow):

                if os.path.splitext(selectedFile)[1] == '.csv' or os.path.splitext(selectedFile)[1] =='.txt':
                    df = pd.read_csv(selectedFile)


                    pen = pg.mkPen(width=5,color=next(self.graphWindowOverlay.colorCycle))
                    self.graphWindowOverlay.graphWidget.addLegend()
                    self.graphWindowOverlay.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen,name=f'{selectedFile}')
                elif os.path.splitext(selectedFile)[1] =='.xls' or os.path.splitext(selectedFile)[1] =='.xlsx': 
                    df_dict = pd.read_excel(selectedFile,sheet_name=None)
                    # add legend
                    self.graphWindowOverlay.graphWidget.addLegend()
                    for key,df in df_dict.items():
                        pen = pg.mkPen(width=5,color=next(self.graphWindowOverlay.colorCycle))
                        self.graphWindowOverlay.graphWidget.plot(df.iloc[:,0],df.iloc[:,1],pen=pen,name=f'{selectedFile}/{key}')
                    
                else:
                    raise TypeError(f'Unsupported file type {os.path.splitext(selectedFile)[1]} ')

            else:

                raise TypeError('Unknwon type')


    def determineLabelTitleLiveSim(self):
        if self.tableWidget.userParameter.mechanism_parameters_0[1] == 'CV':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Potential,\u03B8'
                ylabel = 'Flux, J'
                title ='Live Voltammogram, dimensionless'
            else:
                xlabel = 'Potential, V'
                ylabel = 'Current, A'
                title = 'Live Voltammogram'
        elif self.tableWidget.userParameter.mechanism_parameters_0[1] == 'CA':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Time, T'
                ylabel = 'Flux, J'
                title ='Live Chronoamperogram, dimensionless'
            else:
                xlabel = 'Time, s'
                ylabel = 'Current, A'
                title = 'Live Chronoamperogram'
        elif self.tableWidget.userParameter.mechanism_parameters_0[1] == 'AI':
            if self.tableWidget.userParameter.ViewOption[3]:
                xlabel = 'Potential,\u03B1'
                ylabel = 'Flux, J'
                title ='Live Voltammogram, dimensionless'
            else:
                xlabel = 'Potential, V'
                ylabel = 'Current, A'
                title = 'Live Voltammogram'
        else:
            xlabel = 'Potential, V'
            ylabel = 'Current, A'
            title = 'Live Voltammogram'

        return xlabel,ylabel,title            
    @pyqtSlot(np.ndarray)
    def plotLiveSimulation(self,fluxesProfile):


        xlabel,ylabel,title = self.determineLabelTitleLiveSim()

        if self.liveSimulationWindow is None:
            self.liveSimulationWindow = GraphWindow(title='Live Voltammogram')
            self.liveSimulationWindow.graphWidget.setBackground('w')
            self.liveSimulationWindow.graphWidget.addLegend()
            pen = pg.mkPen(width=3,color=(0,0,0))
            self.liveSimulationWindowLineRef[0] = self.liveSimulationWindow.graphWidget.plot(fluxesProfile[:,0],fluxesProfile[:,1],pen=pen,name=f'Voltammogram')

            self.liveSimulationWindow.graphWidget.setLabel('bottom',xlabel,**self.liveSimulationWindow.styles)
            self.liveSimulationWindow.graphWidget.setLabel('left',ylabel,**self.liveSimulationWindow.styles)
            self.liveSimulationWindow.graphWidget.setTitle(title,**self.liveSimulationWindow.styles)

            self.liveSimulationWindow.graphWidget.showGrid(x=True,y=True)

        elif isinstance(self.liveSimulationWindow,GraphWindow):
            self.liveSimulationWindow.graphWidget.setLabel('bottom',xlabel,**self.liveSimulationWindow.styles)
            self.liveSimulationWindow.graphWidget.setLabel('left',ylabel,**self.liveSimulationWindow.styles)
            self.liveSimulationWindow.graphWidget.setTitle(title,**self.liveSimulationWindow.styles)
            self.liveSimulationWindowLineRef[0].setData(fluxesProfile[:,0],fluxesProfile[:,1])

        self.liveSimulationWindow.show()
        

    def speciesToggle(self,mechanism):
        if mechanism == 0:
            return OrderedDict([(0,'A'),(1,'B')])
        elif mechanism == 1:
            return OrderedDict([(0,'A'),(1,'B')])
        elif mechanism == 2:
            return OrderedDict([(0,'A'),(1,'B'),(2,'C')])
        elif mechanism == 3:
            return OrderedDict([(0,'A'),(1,'B'),(2,'C')])
        elif mechanism == 4:
            return OrderedDict([(0,'A'),(1,'B'),(2,'C')])
        elif mechanism == 5:
            return OrderedDict([(0,'A'),(1,'B'),(3,'X')])
        elif mechanism == 6:
            return OrderedDict([(0,'A'),(1,'B'),(2,'C'),(3,'X')])
        elif mechanism == 7:
            return OrderedDict([(0,'A'),(1,'B')])
        else:
            return OrderedDict([(0,'A'),(1,'B'),(2,'C'),(3,'X'),(4,'Y')])


    @pyqtSlot(np.ndarray)
    def plotLiveConcPorfile(self,concProfile):




        mechanism = self.tableWidget.userParameter.mechanism_parameters_0[0]

        speciesDict = self.speciesToggle(mechanism)



        if self.liveConcProfileWindow is None:
            self.liveConcProfileWindow = GraphWindow(title='Live Concentration')
            self.liveConcProfileWindow.graphWidget.setBackground('w')
            self.liveConcProfileWindow.graphWidget.addLegend()
            for index,species in speciesDict.items():
                pen = pg.mkPen(width=3,color=next(self.liveConcProfileWindow.colorCycle))
                self.liveConcProfileWindowLineRef[index]=self.liveConcProfileWindow.graphWidget.plot(concProfile[:,0],concProfile[:,index+1],pen=pen,name=f'{species}')

            self.liveConcProfileWindow.graphWidget.setLabel('left','Concentration, M',**self.liveConcProfileWindow.styles)
            self.liveConcProfileWindow.graphWidget.setLabel('bottom','Distance from elctrode, m',**self.liveConcProfileWindow.styles)
            self.liveConcProfileWindow.graphWidget.setTitle('Live of Concentration',**self.liveConcProfileWindow.styles)
            self.liveConcProfileWindow.graphWidget.showGrid(x=True,y=True)

        elif isinstance(self.liveConcProfileWindow,GraphWindow):
            for index,species in speciesDict.items():
                if index not in self.liveConcProfileWindowLineRef.keys():
                    pen = pg.mkPen(width=3,color=next(self.liveConcProfileWindow.colorCycle))
                    self.liveConcProfileWindowLineRef[index]=self.liveConcProfileWindow.graphWidget.plot(concProfile[:,0],concProfile[:,index+1],pen=pen,name=f'{species}')
                self.liveConcProfileWindowLineRef[index].setData(concProfile[:,0],concProfile[:,index+1])

        self.liveConcProfileWindow.show()




    def onStartSimulation(self):

        if self.threadpool.activeThreadCount() < 1:
            self.tableWidget.getUserInput()
            user_inputs = self.tableWidget.getUserInput()
            if user_inputs.mechanism_parameters_0[1] =='AI' and user_inputs.mechanism_parameters_0[0] in [0]:
                self.tableWidget.toDimlessAImode()
                user_inputs = self.tableWidget.getUserInput()

            worker = SimulationWorker(user_inputs)
            worker.signals.progress.connect(self.showProgress)
            worker.signals.finished.connect(self.workerFinished)
            worker.signals.output_file_name.connect(self.onOutputFileName)
            worker.signals.concProfile.connect(self.plotLiveConcPorfile)
            worker.signals.fluxesProfile.connect(self.plotLiveSimulation)
            self.threadpool.start(worker)

        else:
            self.unfinishedWorker()
        
        
        print('Please note development is ongoing. Report bugs in the issue section of the GitHub repository\n')



    @pyqtSlot(int)
    def showProgress(self,progress):
        self.progressbar.setValue(progress)
    
    def workerFinished(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Simulation Complete')
        dlg.setText('Congratulations!\nSimulations successfully completed!')
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec_()

    def unfinishedWorker(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('Too many tasks!')
        dlg.setText(f'Please allow last simulation to finish before the next simulation.')
        dlg.setIcon(QMessageBox.Warning)
        print('\a')
        button = dlg.exec_()


    def tfInstalled(self):
        try:
            import tensorflow
        except ImportError as e:
            error_string = repr(e)
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Tensorflow 2 may not be installed')
            dlg.setText(f'Import error:\n{error_string}\nPlease install Tensorflow 2 at https://www.tensorflow.org/\n')
            dlg.setIcon(QMessageBox.Warning)
            print('\a')
            button = dlg.exec_()



class MyTableWidget(QWidget):
    
    def __init__(self):
        super(QWidget, self).__init__()
        self.settingUpCompleted = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.onAutomaticFileNames)
        self.timer.start(1000)

        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab0 = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.FileTab = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab0,"Mechanism")
        self.tabs.addTab(self.tab1,"CV-Parameters")
        self.tabs.addTab(self.tab2,"Chemical Parameters")
        self.tabs.addTab(self.tab3,"Model Parameters")
        self.tabs.addTab(self.tab4,'Stochastic Process')
        self.tabs.addTab(self.tab5,'Adsorption Parameters')
        self.tabs.addTab(self.FileTab,'File Options')
        # Create the zeroth tab
        self.tab0.layout = QVBoxLayout()
        self.pushButton10 = QPushButton('A + e = B')
        self.pushButton10.setToolTip('1D simulation of Reduction of A to B using implicit finite difference method')
        self.pushButton11 = QPushButton("Stochastic A + e = B")
        self.pushButton11.setToolTip('The most classic mechanism of reduction of A to B using random walk algorithm')
        self.pushButton12 = QPushButton("A + e = B\nB + e = C")
        self.pushButton12.setToolTip('Two electron reduction described by Butler-Volmer')
        self.pushButton13 = QPushButton("A + e = B\nB + B = C")
        self.pushButton13.setToolTip('EC2 reaction')
        self.pushButton14 = QPushButton("A + e = B\nB = C")
        self.pushButton14.setToolTip('EC reaction')
        self.pushButton15 = QPushButton("X = A \nA + e = B")
        self.pushButton15.setToolTip('CE reaction')
        self.pushButton16 = QPushButton("X = A + C\nA + e = B")
        self.pushButton16.setToolTip('Dissociative CE reaction')
        self.pushButton17 = QPushButton("A + e = B\nAabs + e = Babs")
        self.pushButton17.setToolTip('Spcies A and B can adsorb to electrode surface.<br>The adsorbed species are also electrochemical active.')


        self.pushButton10.setCheckable(True)
        self.pushButton11.setCheckable(True)
        self.pushButton12.setCheckable(True)
        self.pushButton13.setCheckable(True)
        self.pushButton14.setCheckable(True)
        self.pushButton15.setCheckable(True)
        self.pushButton16.setCheckable(True)
        self.pushButton17.setCheckable(True)


        self.pushButton10.setEnabled(True)
        self.pushButton11.setEnabled(True)
        self.pushButton12.setEnabled(True)
        self.pushButton13.setEnabled(True)
        self.pushButton14.setEnabled(True)
        self.pushButton15.setEnabled(True)
        self.pushButton16.setEnabled(True)
        self.pushButton17.setEnabled(True)


        self.pushButton10.clicked.connect(self.onMechanism0ButtonClicked)
        self.pushButton11.clicked.connect(self.onMechanism1ButtonClicked)
        self.pushButton12.clicked.connect(self.onMechanism2ButtonClicked)
        self.pushButton13.clicked.connect(self.onMechanism3ButtonClicked)
        self.pushButton14.clicked.connect(self.onMechanism4ButtonClicked)
        self.pushButton15.clicked.connect(self.onMechanism5ButtonClicked)
        self.pushButton16.clicked.connect(self.onMechanism6ButtonClicked)
        self.pushButton17.clicked.connect(self.onMechanism7ButtonClicked)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.pushButton10,0)
        self.button_group.addButton(self.pushButton11,1)
        self.button_group.addButton(self.pushButton12,2)
        self.button_group.addButton(self.pushButton13,3)
        self.button_group.addButton(self.pushButton14,4)
        self.button_group.addButton(self.pushButton15,5)
        self.button_group.addButton(self.pushButton16,6)
        self.button_group.addButton(self.pushButton17,7)
        self.button_group.buttonClicked[int].connect(self.onModelButtonClicked)


        self.tab0.layout.addWidget(self.pushButton10)
        self.tab0.layout.addWidget(self.pushButton11)
        self.tab0.layout.addWidget(self.pushButton12)
        self.tab0.layout.addWidget(self.pushButton13)
        self.tab0.layout.addWidget(self.pushButton14)
        self.tab0.layout.addWidget(self.pushButton15)
        self.tab0.layout.addWidget(self.pushButton16)
        self.tab0.layout.addWidget(self.pushButton17)
        self.tab0.setLayout(self.tab0.layout)



        # Create first tab
        self.tab1.layout = QGridLayout()
        self.pushButton1 = QPushButton("reserved button")
        self.createFormGroupBox1()
        self.createFormGroupBox13()
        self.tab1Stack0 = QStackedWidget()
        self.tab1Stack0.addWidget(self.formGroupBox1)
        self.tab1Stack0.addWidget(self.formGroupBox13) 
        self.tab1.layout.addWidget(self.tab1Stack0,0,0)
        self.createFormGroupBox10()
        self.tab1.layout.addWidget(self.formGroupBox10,1,0)
        self.createFormGroupBox11()
        self.tab1.layout.addWidget(self.formGroupBox11,0,1)
        self.createFormGroupBox12()
        self.tab1.layout.addWidget(self.formGroupBox12,1,1)
        self.tab1.layout.addWidget(self.pushButton1,2,0,1,2)


        self.tab1.setLayout(self.tab1.layout)

        # create second tab 
        self.tab2.layout = QVBoxLayout()
        self.createFormGroupBox2()
        self.tab2.layout.addWidget(self.formGroupBox2)
        self.createFormGroupBox21()
        self.tab2.layout.addWidget(self.formGroupBox21)
        self.createFormGroupBox22()
        self.tab2.layout.addWidget(self.formGroupBox22)
        self.tab2.setLayout(self.tab2.layout)

        # create third tab 
        self.tab3.layout = QGridLayout()
        self.createFormGroupBox3()
        self.tab3.layout.addWidget(self.formGroupBox3,0,0)
        self.createFormGroupBox30()
        self.createFormGroupBox32()
        self.tab3Stack0 = QStackedWidget()
        self.tab3Stack0.addWidget(self.formGroupBox30)
        self.tab3Stack0.addWidget(self.formGroupBox32)
        self.tab3.layout.addWidget(self.tab3Stack0,1,0)
        self.createFormGroupBox31()
        self.tab3.layout.addWidget(self.formGroupBox31,0,1)
        self.pushButton30 = QPushButton('Default Parameters')
        self.pushButton30.clicked.connect(self.onModelParametersDefaultParameters)
        self.tab3.layout.addWidget(self.pushButton30,2,0,1,2)
        self.tab3.setLayout(self.tab3.layout)

        # create fourth tab 
        self.tab4.layout = QGridLayout()
        self.createFormGroupBox4()
        self.tab4.layout.addWidget(self.formGroupBox4,0,0)
        self.createFormGroupBox40()
        self.tab4.layout.addWidget(self.formGroupBox40,0,1)
        self.tab4.setLayout(self.tab4.layout)

        # create fifth tab
        self.tab5.layout = QGridLayout()
        self.createFormGroupBox5()
        self.tab5.layout.addWidget(self.formGroupBox5,0,0)
        self.createFormGroupBox50()
        self.tab5.layout.addWidget(self.formGroupBox50,0,1)
        self.tab5.setLayout(self.tab5.layout)

        # create the sixth tab 
        self.tab6.layout = QGridLayout()
        self.createFormGroupBox6()
        self.tab6.layout.addWidget(self.formGroupBox6,0,0)
        self.createFormGroupBox60()
        self.tab6.layout.addWidget(self.formGroupBox60,0,1)
        self.tab6.setLayout(self.tab6.layout)
        

        # create file tab
        self.FileTab.layout = QGridLayout()
        self.createFileFormGroupBox()
        self.FileTab.layout.addWidget(self.fileFormGroupBox)
        self.FileTab.setLayout(self.FileTab.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.settingUpCompleted = True

        self.userParameter = userInputParameters()
        self.fileParameter = OrderedDict()
        

    def onModelButtonClicked(self,id):
        for button in self.button_group.buttons():
            if button is self.button_group.button(id):
                print(id,button.text() + " Was Clicked ")


    def onMechanism0ButtonClicked(self):
        if self.pushButton10.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism0 = Mechanism0Input()
            Mechanism0.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism0)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())

    def onMechanism1ButtonClicked(self):
        if self.pushButton11.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism1 = Mechanism1Input()
            Mechanism1.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism1)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
    def onMechanism2ButtonClicked(self):
        if self.pushButton12.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism2 = Mechanism2Input()
            Mechanism2.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism2)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
    def onMechanism3ButtonClicked(self):
        if self.pushButton13.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism3 = Mechanism3Input()
            Mechanism3.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism3)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())

    
    def onMechanism4ButtonClicked(self):
        if self.pushButton14.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism4 = Mechanism4Input()
            Mechanism4.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism4)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
    def onMechanism5ButtonClicked(self):
        if self.pushButton15.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism5 = Mechanism5Input()
            Mechanism5.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism5)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
    def onMechanism6ButtonClicked(self):
        if self.pushButton16.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism6 = Mechanism6Input()
            Mechanism6.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism6)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
    def onMechanism7ButtonClicked(self):
        if self.pushButton17.isChecked():
            fileParameter = self.loadFileParameter()
            Mechanism7 = Mechanism7Input()
            Mechanism7.file_options_parameters = fileParameter
            self.loadInputParameters(Mechanism7)
        self.userParameter.mechanism_parameters_0[0] = self.button_group.id(self.button_group.checkedButton())
        self.calAds()

    def onCVModeToggled(self):
        self.defaultTabVisibility()
        self.defaultMechanismEnabled()
        self.tab1Stack0.setCurrentIndex(0)
        self.tab3Stack0.setCurrentIndex(0)
        self.userParameter.mechanism_parameters_0[1] = 'CV'
        print(self.userParameter.mechanism_parameters_0[1])
        if self.tabs.count() == 7:
            self.tabs.setTabText(1,'CV-Parameters')
        elif self.tabs.count() == 8:
            self.tabs.setTabText(2,'CV-Parameters')

    def onCAModeToggled(self):
        self.defaultTabVisibility()
        self.CAMechanismEnabled()
        self.tab1Stack0.setCurrentIndex(1)
        self.tab3Stack0.setCurrentIndex(1)
        self.userParameter.mechanism_parameters_0[1] = 'CA'
        print(self.userParameter.mechanism_parameters_0[1])
        if self.tabs.count() == 7:
            self.tabs.setTabText(1,'CA-Parameters')
        elif self.tabs.count() == 8:
            self.tabs.setTabText(2,'CA-Parameters')


    def onAIModeToggled(self):
        self.AIModeTabVisibility()
        self.AIModeMechanismEnabled()
        self.userParameter.mechanism_parameters_0[1] = 'AI'
        print(self.userParameter.mechanism_parameters_0[1])

    def AIModeTabVisibility(self):
        self.tab1.setEnabled(False)
        self.tab2.setEnabled(False)
        self.tab3.setEnabled(False)
        self.tab4.setEnabled(False)
        self.tab5.setEnabled(False)
        self.tab6.setEnabled(True)
        self.tabs.insertTab(1,self.tab6,'CV AI-prediction')

    def AIModeMechanismEnabled(self):
        setEnabled(self.pushButton10)
        setDisabled(self.pushButton11)
        setDisabled(self.pushButton12)
        setDisabled(self.pushButton13)
        setDisabled(self.pushButton14)
        setDisabled(self.pushButton15)
        setDisabled(self.pushButton16)
        setDisabled(self.pushButton17)

    def defaultTabVisibility(self):
        self.tab1.setEnabled(True)
        self.tab2.setEnabled(True)
        self.tab3.setEnabled(True)
        self.tab4.setEnabled(True)
        self.tab5.setEnabled(True)
        self.tab6.setEnabled(False)

    def defaultMechanismEnabled(self):
        setEnabled(self.pushButton10)
        setEnabled(self.pushButton11)
        setEnabled(self.pushButton12)
        setEnabled(self.pushButton13)
        setEnabled(self.pushButton14)
        setEnabled(self.pushButton15)
        setEnabled(self.pushButton16)
        setDisabled(self.pushButton17)

    def CAMechanismEnabled(self):
        #setDisabled(self.pushButton10)
        setDisabled(self.pushButton11)
        setDisabled(self.pushButton12)
        #setDisabled(self.pushButton13)
        #setDisabled(self.pushButton14)
        #setDisabled(self.pushButton15)
        #setDisabled(self.pushButton16)
        setDisabled(self.pushButton17)

    def onModelParametersDefaultParameters(self):
        print('Not implemented')
    
    def createFormGroupBox1(self):
        self.formGroupBox1 = QGroupBox('Simulation Parameters')
        layout = QFormLayout()
        self.input_widgets_dict1 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict1[i] = QLineEdit()

        layout.addRow(QLabel('E<sub>start</sub>, V'),self.input_widgets_dict1[0])
        layout.addRow(QLabel('E<sub>rev</sub>, V'),self.input_widgets_dict1[1])
        layout.addRow(QLabel('E<sub>end</sub>, V'),self.input_widgets_dict1[2])
        layout.addRow(QLabel('Scan Rate, V/s'),self.input_widgets_dict1[3])
        layout.addRow(QLabel('Cycles'),self.input_widgets_dict1[4])
        layout.addRow(QLabel('Ru, ohm'),self.input_widgets_dict1[5])
        layout.addRow(QLabel('Cdl, F'),self.input_widgets_dict1[6])
        self.input_widgets_dict1[6].setToolTip('Double Layer Capacitance')
        layout.addRow(QLabel('Temp, K'),self.input_widgets_dict1[7])
        layout.addRow(QLabel('Reserved'),self.input_widgets_dict1[8])
        layout.addRow(QLabel('Reserved'),self.input_widgets_dict1[9])
        self.formGroupBox1.setLayout(layout)

        self.input_widgets_dict1[0].setToolTip('Start potential of scan')
        self.input_widgets_dict1[1].setToolTip('Reverse potential of scan')
        self.input_widgets_dict1[2].setToolTip('End potential of scan, usually equal to the start potential')

        self.input_widgets_dict1[4].setToolTip('Number of cycles. Default to 1.')
        self.input_widgets_dict1[5].setToolTip('Internal resistance. Not implemented')
        self.input_widgets_dict1[6].setToolTip('Double Layer Capacitance. Not implemented.')


    def createFormGroupBox10(self):
        self.formGroupBox10 = QGroupBox('Concentration, mole/liter (Molar)')
        layout = QFormLayout()
        self.input_widgets_dict10 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict10[i] = QLineEdit()

        layout.addRow(QLabel('A'),self.input_widgets_dict10[0])
        layout.addRow(QLabel('B'),self.input_widgets_dict10[1])
        layout.addRow(QLabel('C'),self.input_widgets_dict10[2])
        layout.addRow(QLabel('X'),self.input_widgets_dict10[3])
        layout.addRow(QLabel('Y'),self.input_widgets_dict10[4])
        
        self.input_widgets_dict10[0].editingFinished.connect(lambda:(self.input_widgets_dict22[2].setText(self.input_widgets_dict10[0].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict22[2].setText(self.input_widgets_dict10[0].text()) )
        self.input_widgets_dict10[1].editingFinished.connect(lambda:(self.input_widgets_dict22[6].setText(self.input_widgets_dict10[1].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict22[6].setText(self.input_widgets_dict10[1].text()) )
        self.input_widgets_dict10[2].editingFinished.connect(lambda:(self.input_widgets_dict22[10].setText(self.input_widgets_dict10[2].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict22[10].setText(self.input_widgets_dict10[2].text()) )
        self.input_widgets_dict10[3].editingFinished.connect(lambda:(self.input_widgets_dict22[14].setText(self.input_widgets_dict10[3].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict22[14].setText(self.input_widgets_dict10[3].text()) )
        self.input_widgets_dict10[4].editingFinished.connect(lambda:(self.input_widgets_dict22[18].setText(self.input_widgets_dict10[4].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict22[18].setText(self.input_widgets_dict10[4].text()) )

        self.formGroupBox10.setLayout(layout)

    def createFormGroupBox11(self):
        self.formGroupBox11 = QGroupBox('Information of Electrode')
        layout = QFormLayout()
        self.input_widgets_dict11 = OrderedDict()

        self.input_widgets_dict11[0] = QComboBox()
        self.input_widgets_dict11[0].addItems(['Macro, Planar','Micro, Spherical','Mirco, Hemispherical','Micro, Microdisc','Micro, Cylinder'])
        self.input_widgets_dict11[0].currentIndexChanged.connect(self.electrodeGeometryInput)
        self.input_widgets_dict11[1] = QLineEdit()
        self.input_widgets_dict11[2] = QLineEdit()
        layout.addRow(QLabel('Geometry of electrode'),self.input_widgets_dict11[0])
        layout.addRow(QLabel('Radius, m'),self.input_widgets_dict11[1])
        layout.addRow(QLabel('Electrode length, m \n(cylinder electrode only)'),self.input_widgets_dict11[2])

        self.formGroupBox11.setLayout(layout)

    def electrodeGeometryInput(self,index):
        if index == 0:
            setDisabled(self.input_widgets_dict11[2])
        elif index == 1:
            setDisabled(self.input_widgets_dict11[2])
        elif index == 2:
            setDisabled(self.input_widgets_dict11[2])
        elif index == 3:
            setDisabled(self.input_widgets_dict11[2])
        elif index == 4:
            setEnabled(self.input_widgets_dict11[2])

    def createFormGroupBox12(self):
        self.formGroupBox12 = QGroupBox('Simulation Boundary')
        layout = QFormLayout()
        self.input_widgets_dict12 = OrderedDict()

        self.input_widgets_dict12[0] = QComboBox()
        self.input_widgets_dict12[0].addItems(['Semi-Infinite','Finite Space'])
        layout.addRow(QLabel('Mode of simulation'),self.input_widgets_dict12[0])

        self.formGroupBox12.setLayout(layout)


    def createFormGroupBox13(self):
        self.formGroupBox13 = QGroupBox('Simulation Parameters')
        layout = QFormLayout()
        self.input_widgets_dict13 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict13[i] = QLineEdit()

        layout.addRow(QLabel('E<sub>applied</sub>, V'),self.input_widgets_dict13[0])
        layout.addRow(QLabel('Time'),self.input_widgets_dict13[1])
        layout.addRow(QLabel('Ru, ohm'),self.input_widgets_dict13[2])
        layout.addRow(QLabel('Cdl, F'),self.input_widgets_dict13[3])
        self.input_widgets_dict13[3].setToolTip('Double Layer Capacitance')
        layout.addRow(QLabel('Temp, K'),self.input_widgets_dict13[4])
        layout.addRow(QLabel('Reserved'),self.input_widgets_dict13[5])
        layout.addRow(QLabel('Reserved'),self.input_widgets_dict13[6])
        self.formGroupBox13.setLayout(layout)



    def createFormGroupBox2(self):
        self.formGroupBox2 = QGroupBox('Heterogeneous Reactions')
        self.input_widgets_dict2 = OrderedDict()
        self.input_master_widgets_dict2 = OrderedDict()
        masterlayout = QHBoxLayout()
        layout1 = QFormLayout()


        self.input_widgets_dict2[0] = QComboBox()
        self.input_widgets_dict2[0].addItems(['Nernst','Butler-Volmer','Marcus-Hush'])
        self.input_widgets_dict2[0].currentIndexChanged.connect(self.mechanismTypeInput)
        self.input_widgets_dict2[1] = QLineEdit()
        self.input_widgets_dict2[2] = QLineEdit()
        self.input_widgets_dict2[3] = QLineEdit()
        self.input_widgets_dict2[4] = QLineEdit()
        self.input_widgets_dict2[10] = QLineEdit()


        layout1.addRow(QLabel('A + e = B'),QLabel(''))
        layout1.addRow(QLabel('Type of mechanism'),self.input_widgets_dict2[0])
        layout1.addRow(QLabel('Formal Potential, E<sub>0</sub>, V'),self.input_widgets_dict2[1])
        self.input_widgets_dict2[1].setToolTip('The formal potential is thus the reversible potential of an electrode at equilibrium\nimmersed in a solution where reactants and products are at unit concentration')
        layout1.addRow(QLabel('Reorganization Energy, eV'),self.input_widgets_dict2[2])
        self.input_widgets_dict2[2].setToolTip('Reorganization energy for Marcus-Hush Theory. Its unit is electronvolt')
        layout1.addRow(QLabel('Standard electrochemical rate constant<br> k<sub>0</sub>, m/s.'),self.input_widgets_dict2[3])
        self.input_widgets_dict2[3].setToolTip('Relevant for BV and MH kinetics. When k0 is large, they approximate Nernst kinetics')
        layout1.addRow(QLabel('Transfer coefficient,\u03B1'),self.input_widgets_dict2[4])
        self.input_widgets_dict2[4].setToolTip('Transfer coefficient for Butler-Volmer theory.\nRange=(0,1),default value is around 0.5')
        layout1.addRow(QLabel('Asymmetric parameter,\u03BB'),self.input_widgets_dict2[10])
        self.input_widgets_dict2[10].setToolTip('Asymmetric parameter for asymmetric Marcus-Hush theory.\nRange=(-1,1). Prefer |\u03BB|<0.3\nIf \u03BB == 0, it is the symmetric Marcus-Hush theory')



        layout2 = QFormLayout()
        self.input_widgets_dict2[5] = QComboBox()
        self.input_widgets_dict2[5].addItems(['Nernst','Butler-Volmer','Marcus-Hursh'])
        self.input_widgets_dict2[6] = QLineEdit()
        self.input_widgets_dict2[7] = QLineEdit()
        self.input_widgets_dict2[8] = QLineEdit()
        self.input_widgets_dict2[9] = QLineEdit()
        self.input_widgets_dict2[11] = QLineEdit()


        layout2.addRow(QLabel('B + e = C'),QLabel(''))
        layout2.addRow(QLabel('Type of mechanism'),self.input_widgets_dict2[5])
        layout2.addRow(QLabel('Formal Potential, E<sub>0</sub>, V'),self.input_widgets_dict2[6])
        layout2.addRow(QLabel('Reorgnization Energy, eV'),self.input_widgets_dict2[7])
        layout2.addRow(QLabel('Standard electrochemical rate constant<br> k<sub>0</sub>, m/s'),self.input_widgets_dict2[8])
        layout2.addRow(QLabel('Transfer coefficient,\u03B1'),self.input_widgets_dict2[9])
        layout2.addRow(QLabel('Asymmetric parameter,\u03BB'),self.input_widgets_dict2[11])

        masterWidget1 = QWidget()
        masterWidget1.setLayout(layout1)
        masterWidget2 = QWidget()
        masterWidget2.setLayout(layout2)

        masterlayout.addWidget(masterWidget1)
        masterlayout.addWidget(masterWidget2)
        self.formGroupBox2.setLayout(masterlayout)

        self.input_master_widgets_dict2[0] = masterWidget1
        self.input_master_widgets_dict2[1] = masterWidget2

    def mechanismTypeInput(self,index):
        if index == 0:
            setDisabled(self.input_widgets_dict2[2])
            setDisabled(self.input_widgets_dict2[3])
            setDisabled(self.input_widgets_dict2[4])
            setDisabled(self.input_widgets_dict2[10])
        elif index == 1:
            setDisabled(self.input_widgets_dict2[2])
            setEnabled(self.input_widgets_dict2[3])
            setEnabled(self.input_widgets_dict2[4])
            setDisabled(self.input_widgets_dict2[10])
        elif index == 2:
            setEnabled(self.input_widgets_dict2[2])
            setEnabled(self.input_widgets_dict2[3])
            setDisabled(self.input_widgets_dict2[4])
            setEnabled(self.input_widgets_dict2[10])
    def createFormGroupBox21(self):
        self.formGroupBox21 = QGroupBox('Homogeneous Chemical Reactions')
        layout = QFormLayout()
        self.input_widgets_dict21 = OrderedDict()
        self.input_widgets_dict21[0] = QLabel()
        self.input_widgets_dict21[1] = QLineEdit()
        self.input_widgets_dict21[2] = QLabel()
        self.input_widgets_dict21[3] = QLineEdit()
        self.input_widgets_dict21[4] = QCheckBox('Pre-equilibrium')
        self.input_widgets_dict21[4].toggled.connect(self.calculateCinit)

        layout.addRow(self.input_widgets_dict21[0],self.input_widgets_dict21[1])
        layout.addRow(self.input_widgets_dict21[2],self.input_widgets_dict21[3])
        layout.addRow(self.input_widgets_dict21[4])

        self.input_widgets_dict21[1].editingFinished.connect(self.calculateCinit)
        self.input_widgets_dict21[3].editingFinished.connect(self.calculateCinit)
        self.formGroupBox21.setLayout(layout)

    def createFormGroupBox22(self):
        self.formGroupBox22 = QGroupBox('Species Parameters')
        layout = QFormLayout()
        self.input_widgets_dict22 = OrderedDict()
        

        self.input_widgets_dict22[0] = QCheckBox()
        self.input_widgets_dict22[1] = QLineEdit()
        self.input_widgets_dict22[2] = QLineEdit()
        self.input_widgets_dict22[3] = QLineEdit()
        self.input_widgets_dict22[3].setReadOnly(True)
        header0 = QVBoxLayout()
        header0.addWidget(QLabel(''))
        header0.addWidget(self.input_widgets_dict22[0])
        header1 = QVBoxLayout()
        header1.addWidget(QLabel('D, m<sup>2</sup>/s'))
        header1.addWidget(self.input_widgets_dict22[1])
        header2 = QVBoxLayout()
        header2.addWidget(QLabel('c<sub>anal</sub>, M'))
        header2.addWidget(self.input_widgets_dict22[2])
        header3 = QVBoxLayout()
        header3.addWidget(QLabel('c<sub>init</sub>, M'))
        header3.addWidget(self.input_widgets_dict22[3])
        QuadrupleInputLayout = QHBoxLayout()
        textlayout = QVBoxLayout()
        textlayout.addWidget(QLabel(''))
        textlayout.addWidget(QLabel('A'))
        QuadrupleInputLayout.addLayout(textlayout)
        QuadrupleInputLayout.addLayout(header0)
        QuadrupleInputLayout.addLayout(header1)
        QuadrupleInputLayout.addLayout(header2)
        QuadrupleInputLayout.addLayout(header3)
        layout.addRow(QuadrupleInputLayout)

        self.input_widgets_dict22[4] = QCheckBox()
        self.input_widgets_dict22[5] = QLineEdit()
        self.input_widgets_dict22[6] = QLineEdit()
        self.input_widgets_dict22[7] = QLineEdit()
        self.input_widgets_dict22[7].setReadOnly(True)
        QuadrupleInputLayout = QHBoxLayout()
        QuadrupleInputLayout.addWidget(QLabel('B'))
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[4])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[5])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[6])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[7])
        layout.addRow(QuadrupleInputLayout)


        self.input_widgets_dict22[8] = QCheckBox()
        self.input_widgets_dict22[9] = QLineEdit()
        self.input_widgets_dict22[10] = QLineEdit()
        self.input_widgets_dict22[11] = QLineEdit()
        self.input_widgets_dict22[11].setReadOnly(True)
        QuadrupleInputLayout = QHBoxLayout()
        QuadrupleInputLayout.addWidget(QLabel('C'))
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[8])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[9])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[10])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[11])
        layout.addRow(QuadrupleInputLayout)

        self.input_widgets_dict22[12] = QCheckBox()
        self.input_widgets_dict22[13] = QLineEdit()
        self.input_widgets_dict22[14] = QLineEdit()
        self.input_widgets_dict22[15] = QLineEdit()
        self.input_widgets_dict22[15].setReadOnly(True)
        QuadrupleInputLayout = QHBoxLayout()
        QuadrupleInputLayout.addWidget(QLabel('X'))
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[12])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[13])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[14])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[15])
        layout.addRow(QuadrupleInputLayout)

        self.input_widgets_dict22[16] = QCheckBox()
        self.input_widgets_dict22[17] = QLineEdit()
        self.input_widgets_dict22[18] = QLineEdit()
        self.input_widgets_dict22[19] = QLineEdit()
        self.input_widgets_dict22[19].setReadOnly(True)
        QuadrupleInputLayout = QHBoxLayout()
        QuadrupleInputLayout.addWidget(QLabel('Y'))
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[16])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[17])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[18])
        QuadrupleInputLayout.addWidget(self.input_widgets_dict22[19])
        layout.addRow(QuadrupleInputLayout)

        self.input_widgets_dict22[2].editingFinished.connect(lambda:(self.input_widgets_dict10[0].setText(self.input_widgets_dict22[2].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict10[0].setText(self.input_widgets_dict22[2].text()))
        self.input_widgets_dict22[6].editingFinished.connect(lambda:(self.input_widgets_dict10[1].setText(self.input_widgets_dict22[6].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict10[1].setText(self.input_widgets_dict22[6].text()))
        self.input_widgets_dict22[10].editingFinished.connect(lambda:(self.input_widgets_dict10[2].setText(self.input_widgets_dict22[10].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict10[2].setText(self.input_widgets_dict22[10].text()))
        self.input_widgets_dict22[14].editingFinished.connect(lambda:(self.input_widgets_dict10[3].setText(self.input_widgets_dict22[14].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict10[3].setText(self.input_widgets_dict22[14].text()))
        self.input_widgets_dict22[18].editingFinished.connect(lambda:(self.input_widgets_dict10[4].setText(self.input_widgets_dict22[18].text()),self.calculateCinit()) if self.settingUpCompleted else self.input_widgets_dict10[4].setText(self.input_widgets_dict22[18].text()))
        self.formGroupBox22.setLayout(layout)


    def calculateCinit(self):
        if not self.input_widgets_dict21[4].isChecked():
            self.input_widgets_dict22[3].setText(self.input_widgets_dict10[0].text())
            self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
            self.input_widgets_dict22[11].setText(self.input_widgets_dict10[2].text())
            self.input_widgets_dict22[15].setText(self.input_widgets_dict10[3].text())
            self.input_widgets_dict22[19].setText(self.input_widgets_dict10[4].text())
        elif self.input_widgets_dict21[4].isChecked():
            kf = getValue(self.input_widgets_dict21[1])
            kb = getValue(self.input_widgets_dict21[3])
            cA = getValue(self.input_widgets_dict10[0])
            cB = getValue(self.input_widgets_dict10[1])
            cC = getValue(self.input_widgets_dict10[2])
            cX = getValue(self.input_widgets_dict10[3])
            cY = getValue(self.input_widgets_dict10[4])
            if math.isclose(kf,0.0,abs_tol=1e-8) and math.isclose(kb,0.0,abs_tol=1e-8):
                self.input_widgets_dict22[3].setText(self.input_widgets_dict10[0].text())
                self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                self.input_widgets_dict22[11].setText(self.input_widgets_dict10[2].text())
                self.input_widgets_dict22[15].setText(self.input_widgets_dict10[3].text())
                self.input_widgets_dict22[19].setText(self.input_widgets_dict10[4].text())
                return
            if math.isclose(kf,0.0,abs_tol=1e-8):
                if self.userParameter.mechanism_parameters_0[0] == 3:
                    # No pre-equilibrium for EC2 reaction 
                    pass
                elif self.userParameter.mechanism_parameters_0[0] == 4:
                    # No pre-equilibrium for EC reaction 
                    pass
                elif self.userParameter.mechanism_parameters_0[0] == 5:
                    self.input_widgets_dict22[3].setText(f'{0.0:.2E}')
                    self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                    self.input_widgets_dict22[15].setText(f'{cA+cX}')
                elif self.userParameter.mechanism_parameters_0[0] == 6:
                    if cA> cC:

                        self.input_widgets_dict22[3].setText(f'{cA-cC:.2E}')
                        self.input_widgets_dict22[11].setText(f'{0.0:.2E}')
                        self.input_widgets_dict22[15].setText(f'{cX+cC:.2E}')
                    elif cA <=cC:
                        self.input_widgets_dict22[3].setText(f'{0.0:.2E}')
                        self.input_widgets_dict22[11].setText(f'{cC-cA:.2E}')
                        self.input_widgets_dict22[15].setText(f'{cX+cA:.2E}')
                return
            if math.isclose(kb,0.0,abs_tol=1e-8):
                if self.userParameter.mechanism_parameters_0[0] == 3:
                    pass
                elif self.userParameter.mechanism_parameters_0[0] == 4:
                    pass
                elif self.userParameter.mechanism_parameters_0[0] == 5:
                    self.input_widgets_dict22[3].setText(f'{cA+cX:.2E}')
                    self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                    self.input_widgets_dict22[15].setText(f'{0.0:.2E}')
                elif self.userParameter.mechanism_parameters_0[0] == 6:
                    self.input_widgets_dict22[3].setText(f'{cA+cX:.2E}')
                    self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                    self.input_widgets_dict22[11].setText(f'{cC+cX:.2E}')
                    self.input_widgets_dict22[15].setText(f'{0.0:.2E}')
                return

            # now kf and kb all have positive values.
            if self.userParameter.mechanism_parameters_0[0] == 3:
                pass
            elif self.userParameter.mechanism_parameters_0[0] == 4:
                pass
            elif self.userParameter.mechanism_parameters_0[0] == 5:
                keq = kf/kb
                X = sympy.Symbol('X')
                X = sympy.solve((cA+X)/(cX-X)-keq,X)
                X = X[0]
                self.input_widgets_dict22[3].setText(f'{cA+X:.2E}')
                self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                self.input_widgets_dict22[15].setText(f'{cX-X:.2E}')
            elif self.userParameter.mechanism_parameters_0[0] == 6:
                keq = kf/kb
                X = sympy.Symbol('X')
                X = sympy.solve((cA+X)*(cC+X)/(cX-X)-keq,X)
                print(X)
                if len(X) == 2:
                    X = X[1]
                    self.input_widgets_dict22[3].setText(f'{cA+X:.2E}')
                    self.input_widgets_dict22[7].setText(self.input_widgets_dict10[1].text())
                    self.input_widgets_dict22[11].setText(f'{cC+X:.2E}')
                    self.input_widgets_dict22[15].setText(f'{cX-X:.2E}')



    def createFormGroupBox3(self):
        self.formGroupBox3 = QGroupBox('Space grid in x direction')
        layout = QFormLayout()
        self.input_widgets_dict3 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict3[i] = QLineEdit()

        layout.addRow(QLabel('Expanding Grid Factor'),self.input_widgets_dict3[0])
        layout.addRow(QLabel('D*/k*'),self.input_widgets_dict3[1])
        layout.addRow(QLabel('Xmax/SQRT(Dt)'),self.input_widgets_dict3[2])
        layout.addRow(QLabel('R0*,minimum'),self.input_widgets_dict3[3])


        self.formGroupBox3.setLayout(layout)
        self.input_widgets_dict3[0].setToolTip('Simulation uses expanding spatial grid and this parameter determines how refine the space grid is.\nThe smaller the parameter, the more refine the grid is. It must be larger than 0.')
        self.input_widgets_dict3[2].setToolTip('A hyperparamter determining the maximum distance of simulation.\nFor semi-infinit boundary condition, it is usually 6.\nFor finite space boundary condition, it is usually less than 1')


    def createFormGroupBox30(self):
        self.formGroupBox30 = QGroupBox('Time grid in cyclic voltammetry')
        layout = QFormLayout()
        self.input_widgets_dict30 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict30[i] = QLineEdit()

        layout.addRow(QLabel('Potential Step (V)'),self.input_widgets_dict30[0])
        layout.addRow(QLabel('Gauss-Newton iteration'),self.input_widgets_dict30[1])
        layout.addRow(QLabel('Gaussian Noise level (A)'),self.input_widgets_dict30[2])

        self.formGroupBox30.setLayout(layout)

        self.input_widgets_dict30[1].setToolTip('Maximum number of iterations for Newton method.\nIncrease if simulation is not converged')





    def createFormGroupBox31(self):
        self.formGroupBox31 = QGroupBox('Space grid in y direction')
        layout = QFormLayout()
        self.input_widgets_dict31 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict31[i] = QLineEdit()

        layout.addRow(QLabel('Expanding grid factor in y direction'),self.input_widgets_dict31[0])

        self.formGroupBox31.setLayout(layout)
        self.input_widgets_dict31[0].setToolTip('Expanding grid factor for 2D simulation. No effect yet.')


    def createFormGroupBox32(self):
        self.formGroupBox32 = QGroupBox('Time grid in chronoamperometry')
        layout = QFormLayout()
        self.input_widgets_dict32 = OrderedDict()
        for i in range(10):
            self.input_widgets_dict32[i] = QLineEdit()

        layout.addRow(QLabel('Initial Time Step'),self.input_widgets_dict32[0])
        layout.addRow(QLabel('Expanding Time Factor'),self.input_widgets_dict32[1])
        layout.addRow(QLabel('Gaussian Noise Level (A)'),self.input_widgets_dict32[2])

        self.formGroupBox32.setLayout(layout)

    def createFormGroupBox4(self):
        self.formGroupBox4 = QGroupBox('Stochastic Parameters')
        layout = QFormLayout()
        self.input_widgets_dict4 = OrderedDict()

        for i in range(10):
            self.input_widgets_dict4[i] = QLineEdit()

        layout.addRow(QLabel('Sampling rate,Hz'),self.input_widgets_dict4[0])
        layout.addRow(QLabel('Number of oversampling'),self.input_widgets_dict4[1])
        self.formGroupBox4.setLayout(layout)
        
        self.input_widgets_dict4[0].setToolTip('Sampling frequency of potentiostat')
        self.input_widgets_dict4[1].setToolTip('Simulation resampling rate based on the original sampling rate.\nThe discrete time interval is thus 1/sampling rate/oversampling rate (second)')

    def createFormGroupBox40(self):
        self.formGroupBox40 = QGroupBox('Simulation Parameters')
        layout = QFormLayout()
        self.input_widgets_dict40 = OrderedDict()

        self.input_widgets_dict40[0] = QLineEdit()
        self.input_widgets_dict40[0].setReadOnly(True)
        self.input_widgets_dict40[1] = QPushButton('Calculate')
        self.input_widgets_dict40[1].clicked.connect(self.calcNMolecules)
        

        layout.addRow(QLabel('Number of molecules'),self.input_widgets_dict40[0])
        layout.addRow(self.input_widgets_dict40[1])
        self.input_widgets_dict40[0].setToolTip('The number of molecules in 1D simulation.\nThe higher the concentration, the more molecules to simulate')
        self.formGroupBox40.setLayout(layout)


    def calcNMolecules(self):
        EMax = getValue(self.input_widgets_dict1[0])
        EMin = getValue(self.input_widgets_dict1[1])
        v  = getValue(self.input_widgets_dict1[3])
        cycles = int(getValue(self.input_widgets_dict1[4]))
        c0 = getValue(self.input_widgets_dict10[0]) * 1000
        dElectrode = getValue(self.input_widgets_dict11[1])
        D = getValue(self.input_widgets_dict22[1])
        NA = 6.0221409e23
        tMax = 2.0*(EMax-EMin)/v * cycles
        xMax = 6.0*math.sqrt(D*tMax)
        A = math.pi * dElectrode * dElectrode
        nMolecules = int(NA*c0*xMax*A)
        self.input_widgets_dict40[0].setText(f'{nMolecules}')


    def createFormGroupBox5(self):
        self.formGroupBox5 = QGroupBox('Adsorption Parameters,Langmuir adsorption model')
        layout = QFormLayout()
        self.input_widgets_dict5 = OrderedDict()

        self.input_widgets_dict5[0] = QLineEdit()
        self.input_widgets_dict5[1] = QLineEdit()
        self.input_widgets_dict5[2] = QLineEdit()
        self.input_widgets_dict5[3] = QLineEdit()
        self.input_widgets_dict5[4] = QLineEdit()
        self.input_widgets_dict5[5] = QLineEdit()
        self.input_widgets_dict5[6] = QLineEdit()
        self.input_widgets_dict5[7] = QLineEdit()
        self.input_widgets_dict5[8] = QPushButton('Refresh and Calculate')
        self.input_widgets_dict5[0].editingFinished.connect(self.calAds) 
        self.input_widgets_dict5[1].editingFinished.connect(self.calAds)
        self.input_widgets_dict5[2].editingFinished.connect(self.calAds)
        self.input_widgets_dict5[3].editingFinished.connect(self.calAds)
        self.input_widgets_dict5[4].editingFinished.connect(self.calAds)
        self.input_widgets_dict5[8].clicked.connect(self.calAds)

        layout.addRow(QLabel('Maximum surface concentrtaion, \u0393<sub>max</sub>, mol m<sup>-2</sup>'),self.input_widgets_dict5[0])
        layout.addRow(QLabel('Rate of adsorption, species A, k<sub>ads</sub><sup>A</sup>, mol<sup>-1</sup>m<sup>3</sup>s<sup>-1</sup>'),self.input_widgets_dict5[1])
        layout.addRow(QLabel('Rate of desorption, species A, k<sub>des</sub><sup>A</sup>, s<sup>-1</sup> '),self.input_widgets_dict5[2])
        layout.addRow(QLabel('Rate of adsorption, species B, k<sub>ads</sub><sup>B</sup>, mol<sup>-1</sup>m<sup>3</sup>s<sup>-1</sup>'),self.input_widgets_dict5[3])
        layout.addRow(QLabel('Rate of desorption, species B, k<sub>des</sub><sup>B</sup>, s<sup>-1</sup>'),self.input_widgets_dict5[4])
        layout.addRow(QLabel('Initial surface concentrtaion, species A, \u0393<sub>A</sub>, mol m<sup>-2</sup>'),self.input_widgets_dict5[5])
        layout.addRow(QLabel('Initial surface concentrtaion, species B, \u0393<sub>B</sub>, mol m<sup>-2</sup>'),self.input_widgets_dict5[6])
        layout.addRow(QLabel('E<sub>0,abs</sub>, formal potential of adsorbed species, V'),self.input_widgets_dict5[7])
        layout.addRow(self.input_widgets_dict5[8])
        self.formGroupBox5.setLayout(layout)

    def calAds(self):
        GammaMax = getValue(self.input_widgets_dict5[0])
        E0 = getValue(self.input_widgets_dict2[1])
        Temperature = getValue(self.input_widgets_dict1[7])
        kA_ads = getValue(self.input_widgets_dict5[1])
        kA_des = getValue(self.input_widgets_dict5[2])
        kB_ads = getValue(self.input_widgets_dict5[3])
        kB_des = getValue(self.input_widgets_dict5[4])
        E0_ads = E0 - 8.314*Temperature/96485 * math.log((kA_ads/kA_des)/(kB_ads/kB_des))
        cA = getValue(self.input_widgets_dict22[3])
        cB = getValue(self.input_widgets_dict22[7])

        GammaA = GammaMax * (kA_ads/kA_des*cA)/(1.0+kA_ads/kA_des*cA+kB_ads/kB_des*cB)
        GammaB = GammaMax * (kB_ads/kB_des*cB)/(1.0+kA_ads/kA_des*cA+kB_ads/kB_des*cB)
        self.input_widgets_dict5[5].setText(f'{GammaA}')
        self.input_widgets_dict5[6].setText(f'{GammaB}')
        self.input_widgets_dict5[7].setText(f'{E0_ads}')
        


    def createFormGroupBox50(self):
        self.formGroupBox50 = QGroupBox('Electrochemical Reaction, adsorbed species')
        layout = QFormLayout()
        self.input_widgets_dict50 = OrderedDict()
        self.input_widgets_dict50[0] = QLineEdit()
        self.input_widgets_dict50[1] = QLineEdit()
        layout.addRow(QLabel('k<sub>0,ads</sub>, s<sup>-1</sup>'),self.input_widgets_dict50[0])
        layout.addRow(QLabel('\u03B1<sub>ads</sub>'),self.input_widgets_dict50[1])
        self.formGroupBox50.setLayout(layout)
        
    def createFormGroupBox6(self):
        self.formGroupBox6 = QGroupBox('AI prediction, dimensional parameters')
        layout = QFormLayout()
        self.input_widgets_dict6 = OrderedDict()


        self.input_widgets_dict6[0] = QLineEdit()
        self.input_widgets_dict6[1] = QLineEdit()
        self.input_widgets_dict6[2] = QLineEdit()
        self.input_widgets_dict6[3] = QLineEdit()
        self.input_widgets_dict6[4] = QLineEdit()
        self.input_widgets_dict6[5] = QLineEdit()
        self.input_widgets_dict6[6] = QLineEdit()
        self.input_widgets_dict6[7] = QLineEdit()
        self.input_widgets_dict6[8] = QLineEdit()
        self.input_widgets_dict6[9] = QLineEdit()
        self.input_widgets_dict6[10] = QLineEdit()

        
        self.input_widgets_dict6[11] = QComboBox()
        self.input_widgets_dict6[11].addItems(['Bulter-Volmer'])
        self.input_widgets_dict6[12] = QLineEdit()
        self.input_widgets_dict6[13] = QLineEdit()
        self.input_widgets_dict6[14] = QComboBox()
        self.input_widgets_dict6[14].addItems(['Linear','Radial'])
        self.input_widgets_dict6[15] = QPushButton('Convert to dimensionless')
        self.input_widgets_dict6[15].clicked.connect(lambda: (self.toDimlessAImode(),self.checkAImodeInputRange()))

        
        layout.addRow(QLabel('E<sub>start</sub>, V'),self.input_widgets_dict6[0])
        layout.addRow(QLabel('E<sub>rev</sub>, V'),self.input_widgets_dict6[1])
        layout.addRow(QLabel('E<sub>0,f</sub>, V'),self.input_widgets_dict6[2])
        layout.addRow(QLabel('Scan Rate, V/s'),self.input_widgets_dict6[3])
        layout.addRow(QLabel('Cycles'),self.input_widgets_dict6[4])
        layout.addRow(QLabel('c<sub>A<\sub>, M'),self.input_widgets_dict6[5])
        layout.addRow(QLabel('c<sub>B<\sub>, M'),self.input_widgets_dict6[6])
        layout.addRow(QLabel('D<sub>A<\sub>, m<sup>2</sup> s<sup>-1</sup>'),self.input_widgets_dict6[7])
        layout.addRow(QLabel('D<sub>B<\sub>, m<sup>2</sup> s<sup>-1</sup>'),self.input_widgets_dict6[8])
        layout.addRow(QLabel('k<sub>0<\sub>'),self.input_widgets_dict6[9])
        layout.addRow(QLabel('\u03B1, transfer coefficient'),self.input_widgets_dict6[10])
        layout.addRow(QLabel('Electrode Kinetics'),self.input_widgets_dict6[11])
        layout.addRow(QLabel('Temp, K'),self.input_widgets_dict6[12])
        layout.addRow(QLabel('r<sub>e</sub>, m'),self.input_widgets_dict6[13])
        layout.addRow(QLabel('Diffusion Mode'),self.input_widgets_dict6[14])
        layout.addRow(self.input_widgets_dict6[15])
        
        self.formGroupBox6.setLayout(layout)

    def toDimlessAImode(self):
        E_start = getValue(self.input_widgets_dict6[0])
        E_rev = getValue(self.input_widgets_dict6[1])
        E_0f = getValue(self.input_widgets_dict6[2])
        scan_rate = getValue(self.input_widgets_dict6[3])
        cycles = getValue(self.input_widgets_dict6[4])
        c_A = getValue(self.input_widgets_dict6[5])
        c_B = getValue(self.input_widgets_dict6[6])
        D_A = getValue(self.input_widgets_dict6[7])
        D_B = getValue(self.input_widgets_dict6[8])
        k0 = getValue(self.input_widgets_dict6[9])
        alpha = getValue(self.input_widgets_dict6[10])
        kinetics = getValue(self.input_widgets_dict6[11])
        T = getValue(self.input_widgets_dict6[12])
        r_e = getValue(self.input_widgets_dict6[13])
        diffusion_mode = getValue(self.input_widgets_dict6[14])
        R = 8.314
        F = 96485

        self.input_widgets_dict60[0].setText(f'{(E_start-E_0f)*F/(R*T):.2f}')
        self.input_widgets_dict60[1].setText(f'{(E_rev-E_0f)*F/(R*T):.2f}')
        self.input_widgets_dict60[2].setText(f'{(E_0f-E_0f)*F/(R*T):.2f}')
        self.input_widgets_dict60[3].setText(f'{(r_e*r_e/D_A*F/(R*T)*scan_rate):.2E}')
        self.input_widgets_dict60[4].setText(f'{int(cycles)}')
        self.input_widgets_dict60[5].setText(f'{c_A/c_A:.2f}')
        self.input_widgets_dict60[6].setText(f'{c_B/c_A:2f}')
        self.input_widgets_dict60[7].setText(f'{D_A/D_A:.2f}')
        self.input_widgets_dict60[8].setText(f'{D_B/D_A:.2f}')
        self.input_widgets_dict60[9].setText(f'{k0*r_e/D_A:.2E}')
        self.input_widgets_dict60[10].setText(f'{alpha:.2f}')
        self.input_widgets_dict60[11].setCurrentIndex(kinetics)
        self.input_widgets_dict60[12].setCurrentIndex(diffusion_mode)

        


    def createFormGroupBox60(self):
        self.formGroupBox60 = QGroupBox('AI prediction, dimensionless parameters')
        layout = QFormLayout()
        self.input_widgets_dict60 = OrderedDict()


        self.input_widgets_dict60[0] = QLineEdit()
        self.input_widgets_dict60[1] = QLineEdit()
        self.input_widgets_dict60[2] = QLineEdit()
        self.input_widgets_dict60[3] = QLineEdit()
        self.input_widgets_dict60[4] = QLineEdit()


        self.input_widgets_dict60[5] = QLineEdit()
        self.input_widgets_dict60[6] = QLineEdit()
        self.input_widgets_dict60[7] = QLineEdit()
        self.input_widgets_dict60[8] = QLineEdit()
        self.input_widgets_dict60[9] = QLineEdit()
        self.input_widgets_dict60[10] = QLineEdit()
        self.input_widgets_dict60[11] = QComboBox()
        self.input_widgets_dict60[11].addItems(['Butler-Volmer'])
        self.input_widgets_dict60[12] = QComboBox()
        self.input_widgets_dict60[12].addItems(['Linear','Radial'])

        layout.addRow(QLabel('\u03B8<sub>start</sub>'),self.input_widgets_dict60[0])
        layout.addRow(QLabel('\u03B8<sub>rev</sub>'),self.input_widgets_dict60[1])
        layout.addRow(QLabel('\u03B8<sub>0,f</sub>'),self.input_widgets_dict60[2])
        layout.addRow(QLabel('\u03C3, scan rate, [10<sup>-12</sup>,10<sup>15</sup>]'),self.input_widgets_dict60[3])
        layout.addRow(QLabel('Cycles'),self.input_widgets_dict60[4])
        layout.addRow(QLabel('C<sub>A</sub>'),self.input_widgets_dict60[5])
        layout.addRow(QLabel('C<sub>B</sub>'),self.input_widgets_dict60[6])
        layout.addRow(QLabel('d<sub>A</sub>'),self.input_widgets_dict60[7])
        layout.addRow(QLabel('d<sub>B</sub>, [0.01,100]'),self.input_widgets_dict60[8])
        layout.addRow(QLabel('K<sub>0</sub>, [10<sup>-12</sup>,10<sup>8</sup>]'),self.input_widgets_dict60[9])
        layout.addRow(QLabel('\u03B1,[0.05,0.95]'),self.input_widgets_dict60[10])
        layout.addRow(QLabel('Electrode Kinetics'),self.input_widgets_dict60[11])
        layout.addRow(QLabel('Diffusion Mode'),self.input_widgets_dict60[12])


        
        self.formGroupBox60.setLayout(layout)


    def checkAImodeInputRange(self):
        default_qss = "background: white"
        warning_qss = "background: yellow"
        error_string = ""
        if  1e-12 <= getValue(self.input_widgets_dict60[3]) <= 1e15:
            self.input_widgets_dict60[3].setStyleSheet(default_qss)
        else:
            error_string += "The dimensionless scan rate is suggested to be within 10^-12 to 10^15\n"
            self.input_widgets_dict60[3].setStyleSheet(warning_qss)

        if 1e-2 <= getValue(self.input_widgets_dict60[8]) <=100:
            self.input_widgets_dict60[8].setStyleSheet(default_qss)
        else:
            error_string +=  "The dimensionless diffusion coefficient of B is suggested to be within 0.01 and 100\n"
            self.input_widgets_dict60[8].setStyleSheet(warning_qss)

        if 1e-12 <= getValue(self.input_widgets_dict60[9]) <= 1e8:
            self.input_widgets_dict60[9].setStyleSheet(default_qss)
        else:
            error_string += "The dimensionless electrochemical rate constant is suggested to be within 10^-12 to 10^8\n"
            self.input_widgets_dict60[9].setStyleSheet(warning_qss)

        if 0.05 <= getValue(self.input_widgets_dict60[10]) <= 0.95:
            self.input_widgets_dict60[10].setStyleSheet(default_qss)
        else:
            error_string += "The transfer coefficient is suggested to be within 0.05 and 0.95"
            self.input_widgets_dict60[10].setStyleSheet(warning_qss)

        if error_string:
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Check Input Range')
            dlg.setText(error_string)
            dlg.setIcon(QMessageBox.Warning)
            print('\a')
            button = dlg.exec_()




    def createFileFormGroupBox(self):
        self.fileFormGroupBox = QGroupBox('File Output')
        layout = QFormLayout()
        self.file_widgetes_dict = OrderedDict()

        self.file_widgetes_dict[0] = QPushButton('Select folder')
        self.file_widgetes_dict[1] = QLineEdit()
        self.file_widgetes_dict[2] = QLineEdit()
        self.file_widgetes_dict[3] = QComboBox()
        self.file_widgetes_dict[4] = QCheckBox('Automatic File Names')
        self.file_widgetes_dict[5] = QCheckBox('Dimensional form of voltammogram')

        self.file_widgetes_dict[0].clicked.connect(self.saveDirectoryDialog)
        self.file_widgetes_dict[3].addItems(['.txt','.csv'])


        layout.addRow(QLabel(),self.file_widgetes_dict[0])
        layout.addRow(QLabel('Folder name') ,self.file_widgetes_dict[1])
        layout.addRow(QLabel('File name') ,self.file_widgetes_dict[2])
        layout.addRow(QLabel('File type') ,self.file_widgetes_dict[3])
        layout.addRow(self.file_widgetes_dict[4])
        layout.addRow(self.file_widgetes_dict[5])
        self.fileFormGroupBox.setLayout(layout)




    def saveDirectoryDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, 'Save your file at', options=options)
        if directory:
            self.file_widgetes_dict[1].setText(directory)

    def onAutomaticFileNames(self):
        if self.file_widgetes_dict[4].isChecked():
            setDisabled(self.file_widgetes_dict[2])
            self.file_widgetes_dict[2].setText(datetime.datetime.now().strftime(r'%Y-%m-%d %H%M%S'))
        else:
            setEnabled(self.file_widgetes_dict[2])

    def loadInputParameters(self,inputParameter = DefaultInput()):



        for key,value in inputParameter.cv_parameters_1.items():
            self.input_widgets_dict1[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict1[key])

        for key,value in inputParameter.cv_parameters_10.items():
            self.input_widgets_dict10[key].setText(f'{value:.2E}')
            setEnabled(self.input_widgets_dict10[key])

        for key,value in inputParameter.cv_parameters_11.items():
            if key == 0:
                self.input_widgets_dict11[key].setCurrentIndex(value)
            else:
                self.input_widgets_dict11[key].setText(f'{value:.2E}')
            setEnabled(self.input_widgets_dict11[key])

        for key,value in inputParameter.cv_parameters_12.items():
            if key == 0:
                self.input_widgets_dict11[key].setCurrentIndex(value)
            setEnabled(self.input_widgets_dict11[key])

        for key,value in inputParameter.cv_parameters_13.items():
            self.input_widgets_dict13[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict13[key])
            
        for key,value in inputParameter.chemical_parameters_2.items():
            if key in [0,5]:
                self.input_widgets_dict2[key].setCurrentIndex(value)
            else:
                self.input_widgets_dict2[key].setText(f'{value:.2E}')
            setEnabled(self.input_widgets_dict2[key])

        for key,value in inputParameter.chemical_parameters_21.items():
            if key in [0,2]:
                self.input_widgets_dict21[key].setText(value)
            elif key in [4]:
                self.input_widgets_dict21[key].setChecked(value)
            else:
                self.input_widgets_dict21[key].setText(f'{value:.2E}')
            setEnabled(self.input_widgets_dict21[key])
            
        for key,value in inputParameter.chemical_parameters_22.items():
            if key in [0,4,8,12,16]:
                self.input_widgets_dict22[key].setChecked(value)
            else:
                self.input_widgets_dict22[key].setText(f'{value:2E}')
            setEnabled(self.input_widgets_dict22[key])
    
        for key,value in inputParameter.model_parameters_3.items():
            self.input_widgets_dict3[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict3[key])

        for key,value in inputParameter.model_parameters_30.items():
            if key  in [0]:
                self.input_widgets_dict30[key].setText(f'{value:.2E}')
            else:
                self.input_widgets_dict30[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict30[key])

        for key,value in inputParameter.model_parameters_31.items():
            self.input_widgets_dict31[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict31[key])

        for key,value in inputParameter.model_parameters_32.items():
            if key in [0]:
                self.input_widgets_dict32[key].setText(f'{value:.2E}')
            else:
                self.input_widgets_dict32[key].setText(f'{value:.2f}')
            setEnabled(self.input_widgets_dict32[key])

        for key,value in inputParameter.stochastic_process_parameters_4.items():
            self.input_widgets_dict4[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict4[key])

        for key,value in inputParameter.stochastic_process_parameters_40.items():
            if key in [1]:
                pass
            else:
                self.input_widgets_dict40[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict40[key])

        for key,value in inputParameter.adsorption_parameters_5.items():
            if key in [8]:
                setEnabled(self.input_widgets_dict5[key])
            else:
                self.input_widgets_dict5[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict5[key])

        for key,value in inputParameter.adsorption_parameters_50.items():
            self.input_widgets_dict50[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict50[key])

        for key,value in inputParameter.AI_parameters_6.items():
            if key in [11,14]:
                self.input_widgets_dict6[key].setCurrentIndex(value)
            else:
                self.input_widgets_dict6[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict6[key])

        for key,value in inputParameter.AI_parameters_60.items():
            if key in [11,12]:
                self.input_widgets_dict60[key].setCurrentIndex(value)
            else:
                self.input_widgets_dict60[key].setText(f'{value}')
            setEnabled(self.input_widgets_dict60[key])

        for key,value in inputParameter.file_options_parameters.items():
            if key  in [1,2]: 
                self.file_widgetes_dict[key].setText(f'{value}')
                setEnabled(self.file_widgetes_dict[key])
            elif key in [3]:
                self.file_widgetes_dict[key].setCurrentIndex(value)
                setEnabled(self.file_widgetes_dict[key])
            elif key in [4,5]:
                self.file_widgetes_dict[key].setChecked(value)
                setEnabled(self.file_widgetes_dict[key])
        for key,value in inputParameter.chemical_parameters_hided_21.items():
            if value:
                setHided(self.input_master_widgets_dict2[key])
            else:
                setVisible(self.input_master_widgets_dict2[key])
        
        for key,value in inputParameter.cv_parameters_enabled_1.items():
            setDisabled(self.input_widgets_dict1[key])
        for key,value in inputParameter.cv_parameters_enabled_10.items():
            setDisabled(self.input_widgets_dict10[key])
        for key,value in inputParameter.cv_parameters_enabled_11.items():
            setDisabled(self.input_widgets_dict11[key])
        for key,value in inputParameter.cv_parameters_enabled_12.items():
            setDisabled(self.input_widgets_dict12[key])
        for key,value in inputParameter.cv_parameters_enabled_13.items():
            setDisabled(self.input_widgets_dict13[key])
        for key,value in inputParameter.chemical_parameters_enabled_2.items():
            setDisabled(self.input_widgets_dict2[key])
        for key,value in inputParameter.chemical_parameters_enabled_21.items():
            setDisabled(self.input_widgets_dict21[key])
        for key,value in inputParameter.chemical_parameters_enabled_22.items():
            setDisabled(self.input_widgets_dict22[key])
        for key,value in inputParameter.model_parameters_enabled_3.items():
            setDisabled(self.input_widgets_dict3[key])
        for key,value in inputParameter.model_parameters_enabled_30.items():
            setDisabled(self.input_widgets_dict30[key])
        for key,value in inputParameter.model_parameters_enabled_31.items():
            setDisabled(self.input_widgets_dict31[key])
        for key,value in inputParameter.stochastic_parameters_enabled_4.items():
            setDisabled(self.input_widgets_dict4[key])
        for key,value in inputParameter.stochastic_parameters_enabled_40.items():
            setDisabled(self.input_widgets_dict40[key])
        for key,value in inputParameter.adsorption_parameters_enabled_5.items():
            setDisabled(self.input_widgets_dict5[key])
        for key,value in inputParameter.adsorption_parameters_enabled_50.items():
            setDisabled(self.input_widgets_dict50[key])

        for key,value in inputParameter.AI_parameters_enabled_6.items():
            setDisabled(self.input_widgets_dict6[key])    
        
        for key,value in inputParameter.AI_parameters_enabled_60.items():
            setDisabled(self.input_widgets_dict60[key])
    
    def getUserInput(self):

        for key,value in self.userParameter.cv_parameters_1.items():

            self.userParameter.cv_parameters_1[key] = getValue(self.input_widgets_dict1[key])
        
        for key,value in self.userParameter.cv_parameters_10.items():
            self.userParameter.cv_parameters_10[key] = getValue(self.input_widgets_dict10[key])

        for key,value in self.userParameter.cv_parameters_11.items():
            self.userParameter.cv_parameters_11[key] = getValue(self.input_widgets_dict11[key])
        
        for key, value in self.userParameter.cv_parameters_12.items():
            self.userParameter.cv_parameters_12[key] = getValue(self.input_widgets_dict12[key])

        for key,value in self.userParameter.cv_parameters_13.items():
            self.userParameter.cv_parameters_13[key] = getValue(self.input_widgets_dict13[key])

        for key,value in self.userParameter.chemical_parameters_2.items():
            self.userParameter.chemical_parameters_2[key] = getValue(self.input_widgets_dict2[key])

        for key,value in self.userParameter.chemical_parameters_21.items():
            self.userParameter.chemical_parameters_21[key] = getValue(self.input_widgets_dict21[key])

        for key,value in self.userParameter.chemical_parameters_22.items():
            self.userParameter.chemical_parameters_22[key] = getValue(self.input_widgets_dict22[key])


        for key,value in self.userParameter.model_parameters_3.items():
            self.userParameter.model_parameters_3[key] = getValue(self.input_widgets_dict3[key])

        for key,value in self.userParameter.model_parameters_30.items():
            self.userParameter.model_parameters_30[key] = getValue(self.input_widgets_dict30[key])

        for key,value in self.userParameter.model_parameters_31.items():
            self.userParameter.model_parameters_31[key] = getValue(self.input_widgets_dict31[key])

        for key,value in self.userParameter.model_parameters_32.items():
            self.userParameter.model_parameters_32[key] = getValue(self.input_widgets_dict32[key])  

        for key,value in self.userParameter.stochastic_process_parameters_4.items():
            self.userParameter.stochastic_process_parameters_4[key] = getValue(self.input_widgets_dict4[key])
        
        for key,value in self.userParameter.stochastic_process_parameters_40.items():
            self.userParameter.stochastic_process_parameters_40[key] = getValue(self.input_widgets_dict40[key])


        for key,value in self.userParameter.adsorption_parameters_5.items():
            self.userParameter.adsorption_parameters_5[key] = getValue(self.input_widgets_dict5[key])

        for key,value in self.userParameter.adsorption_parameters_50.items():
            self.userParameter.adsorption_parameters_50[key] = getValue(self.input_widgets_dict50[key])

        for key,value in self.userParameter.file_options_parameters.items():
            if key ==1 or key == 2:
                self.userParameter.file_options_parameters[key] = self.file_widgetes_dict[key].text()
            else:
                self.userParameter.file_options_parameters[key] =  getValue(self.file_widgetes_dict[key])

        for key,value in self.userParameter.AI_parameters_60.items():
            self.userParameter.AI_parameters_60[key] = getValue(self.input_widgets_dict60[key])

        return self.userParameter


    def loadFileParameter(self):
        for key,value in self.userParameter.file_options_parameters.items():
            if key ==1 or key == 2:
                self.fileParameter[key] = self.file_widgetes_dict[key].text()
            else:
                self.fileParameter[key] =  getValue(self.file_widgetes_dict[key])

        return self.fileParameter

    def loadModelParameters(self,inputParameter = DefaultInput()):
        for key,value in inputParameter.model_parameters_3.items():
            self.input_widgets_dict3[key].setText(f'{value:.2f}')

        for key,value in inputParameter.model_parameters_30.items():
            self.input_widgets_dict3[key].setText(f'{value:.2f}')

        for key,value in inputParameter.model_parameters_31.items():
            self.input_widgets_dict3[key].setText(f'{value:.2f}')


class GraphWindow(QWidget):
    """
    This "window" is a Qwidget. It it has no parent, it will be a free floating window. 
    
    """


    def __init__(self,title='Voltammogram Graph',IconFile='./Icons/CV-icon.png'):
        super().__init__()
        
        self.graphWidget = PlotWidget(self)
        self.layout = QVBoxLayout() 
        self.resize(500,400)
        self.graphWidget.resize(400,300)
        self.layout.addWidget(self.graphWidget)



        self.setLayout(self.layout)

        self.styles = {'color':'k','font-size':'20pt'}

        self.colorCycle =  itertools.cycle([u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd', u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf'])
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(IconFile))

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()