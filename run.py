from PyQt4 import QtGui,QtCore
import sys
import main_window
import numpy as np
import pyqtgraph
import time


class MainWindow(QtGui.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.inputPlot.plotItem.showGrid(True, True, 0.7)
        self.filePlot.plotItem.showGrid(True, True, 0.7)

        self.inFile = ''

    @QtCore.pyqtSignature("")
    def on_startButton_clicked(self):
        print('hello')

    def closeEvent(self, *args, **kwargs):
        print('implement this')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
