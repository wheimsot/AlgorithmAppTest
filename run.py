from PyQt4 import QtGui,QtCore
import sys
import main_window
import numpy as np
import scipy.io.wavfile
import pyqtgraph
import time


class MainWindow(QtGui.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # Enable/disable required buttons
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.fileButton.setEnabled(True)

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
        if dlg.exec_():
            wav_path = dlg.selectedFiles()[0]
            beats_path = wav_path.replace('.wav', '.txt')
            lines = open(beats_path).read().splitlines()
            self.beat_times = np.asarray(lines, dtype=np.float)
            self.rate, self.wav_data = scipy.io.wavfile.read(wav_path)
            pen = pyqtgraph.mkPen(color='b')
            t = np.arange(0, self.wav_data.size/self.rate, step=1/self.rate)
            self.filePlot.plot(t, self.wav_data.astype(np.float), pen=pen, clear=True)
            self.filePlot.plot(self.beat_times, np.zeros_like(self.beat_times), pen=None, symbol='o', clear=False)
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.fileButton.setEnabled(True)


    @QtCore.pyqtSignature("")
    def on_startButton_clicked(self):
        print('Starting...')
        self.run = True
        self.alg.start()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.fileButton.setEnabled(False)
        #thread = Algorithm()
        #thread.run()

    @QtCore.pyqtSignature("")
    def on_stopButton_clicked(self):
        print('Stopping...')
        self.run = False
        self.alg.terminate()
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.fileButton.setEnabled(True)

    def closeEvent(self, *args, **kwargs):
        print('Closing...')


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
