from PyQt5.QtWidgets import QAction, QBoxLayout, QFormLayout, QGroupBox, QLabel, QListWidget, QMessageBox, QWidget,QLineEdit,QCheckBox,QRadioButton,QMainWindow,QVBoxLayout,QHBoxLayout,QGridLayout,QPushButton,QApplication,QFileDialog,QGroupBox,QButtonGroup,QToolBar
class LabelDirInput(QHBoxLayout):
    def __init__(self,label='',input_class = QLineEdit,input_var = None,input_args = None,label_args = None,**kwargs):
        super().__init__(**kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var
        self.input_class = input_class

        if input_class in (QCheckBox,QPushButton,QRadioButton):
            raise TypeError

        if input_class in (QLineEdit,):
            self.label = QLabel()
            self.input = QLineEdit()
            self.addWidget(self.label)
            self.addWidget(self.input)
            self.label.setText(label)

        if input_class in (QFileDialog,):
            self.label = QPushButton(label)
            self.addWidget(self.label)
            self.label.clicked.connect(self.openDirDialog)

        def get():
            if self.input_class == QFileDialog:
                return self.variable

    def openDirDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self.label, 'Save your file at', options=options)
        if directory:
            print(directory)