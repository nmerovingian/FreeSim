from PyQt5.QtWidgets import QAction, QBoxLayout, QComboBox, QFormLayout, QGroupBox, QLabel, QListWidget, QMessageBox, QProgressBar, QWidget,QLineEdit,QCheckBox,QRadioButton,QMainWindow,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QApplication,QFileDialog,QGroupBox,QButtonGroup,QToolBar,QTabWidget


def getValue(widget):
    if isinstance(widget,QLineEdit):
        return float(widget.text())
    elif isinstance(widget,QCheckBox):
        return bool(widget.isChecked())
    elif isinstance(widget,QComboBox):
        return int(widget.currentIndex())


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
