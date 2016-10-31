from PyQt4 import QtGui,QtCore
import sys
import main_window
import numpy as np
import scipy.io.wavfile
import pyqtgraph
import time
import pyaudio
import queue


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

        self.inFile = ''
        self.run = False
        self.queued_data = queue.Queue()
        self.all_data = np.empty(shape=(0,0), dtype=np.int16)
        self.p = pyaudio.PyAudio()


    @QtCore.pyqtSignature("")
    def on_fileButton_clicked(self):
        """
        Update the file plot figure when the choose file button is pressed. Plots the raw audio with annotated
        beat times over top. Only works for the training set provided by the challenge.
        """
        dlg = QtGui.QFileDialog()
        dlg.setFileMode(QtGui.QFileDialog.AnyFile)
        dlg.setFilter("Wave files (*.wav)")
        if dlg.exec_():
            wav_path = dlg.selectedFiles()[0]
            beats_path = wav_path.replace('.wav', '.txt')
            lines = open(beats_path).read().splitlines()
            self.beat_times = np.asarray(lines, dtype=np.float)
            self.beatTable.clear()
            for i in range(self.beat_times.size):
                self.beatTable.setItem(1, i, QtGui.QTableWidgetItem(str(self.beat_times[i])))
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
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.fileButton.setEnabled(False)
        # Start the callback thread
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=22050, input=True,
                                  frames_per_buffer=4096, stream_callback=self.callback)
        # Begin the algorithm by calling it once. It will call itself repeatedly until the user clicks stop
        self.algorithm()

    @QtCore.pyqtSignature("")
    def on_stopButton_clicked(self):
        print('Stopping...')
        # Set the run flag to False to trigger the algorithm to start
        self.run = False
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.fileButton.setEnabled(True)

    def closeEvent(self, *args, **kwargs):
        print('Closing...')
        # Close the stream and exit
        self.stream.close()

    def algorithm(self):
        self.all_data = np.append(self.all_data, self.queued_data.get())
        #data = self.queued_data.get()
        pen = pyqtgraph.mkPen(color='b')
        t = np.arange(0, 4096/22050, step=1/22050)
        self.inputPlot.plot(np.arange(0, stop=self.all_data.size/22050, step=1/22050), self.all_data, pen=pen, clear=True)#np.random.uniform(size=4096), pen=pen, clear=True)
        if self.run:
            # Call itself
            QtCore.QTimer.singleShot(1, self.algorithm)

    def callback(self, in_data, frame_count, time_info, status):
        # This thread is constantly running when the run flag is True
        data = np.fromstring(in_data, dtype=np.int16)
        print(data)
        self.queued_data.put(data)
        if self.run:
            flag = pyaudio.paContinue
        else:
            flag = pyaudio.paComplete
        return data, flag


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
