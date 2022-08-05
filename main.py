from PyQt5 import QtCore, QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from collections import deque   

from devices import device


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('ui.ui', self)
        #flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(flags)
        self.sdr_device = device()
        self.sdr_device.sample_rate = 250e3
        self.sdr_device.center_freq = 433.975e6
        self.sdr_device.gain = 0
        self.sdr_device.rx_chan = 0
        self.sdr_device.startStream()
        self.status = 0
        self.samples = np.array([0])
        self.num_samps = 1024
        # create sample_deque
        self.sample_deque = deque(maxlen=int(self.sdr_device.sample_rate/10))

        # plotUpdateTimer
        self.plotUpdateTimer = QtCore.QTimer()
        self.plotUpdateTimer.timeout.connect(self.updatePlot)
        self.plotUpdateTimer.start(10)
    
    def updatePlot(self):
        self.status, self.samples = self.sdr_device.readStream()
        #self.matplot.canvas.axes.clear()
        #self.matplot.canvas.axes.plot(self.sample_deque)
        self.matplot.canvas.axes.specgram(self.samples, Fs=self.sdr_device.sample_rate, cmap='jet', mode='psd')
        self.matplot.canvas.draw()
        self.samples = np.array([0])

    def closeEvent(self, event):
        print("Closing")
        try:
            sdr.stopStream()
        except:
            print('No stream to close')
        event.accept()
        sys.exit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()