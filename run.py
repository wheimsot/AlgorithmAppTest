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


        self.alg = Algorithm()
        self.inFile = ''
        self.run = False

    @QtCore.pyqtSignature("")
    def on_fileButton_clicked(self):
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.AnyFile)
        dlg.setFilter("Wave files (*.wav)")
        #filenames = QStringList()
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames)

    @QtCore.pyqtSignature("")
    def on_startButton_clicked(self):
        self.run = True
        self.alg.start()
        #thread = Algorithm()
        #thread.run()

    @QtCore.pyqtSignature("")
    def on_stopButton_clicked(self):
        print('Stopping')
        self.run = False
        self.alg.terminate()

    def closeEvent(self, *args, **kwargs):
        print('implement this')


class Algorithm(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def run(self):
        while self.run:
            print('implement')
            time.sleep(1)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
