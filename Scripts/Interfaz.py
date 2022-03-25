from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from PyQt5 import uic
import time
import pyqtgraph as pg
import serial
import pickle
from sklearn.compose import TransformedTargetRegressor
import os
import sys

class MainWindow(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow.ui", self)
        self.initBtn.clicked.connect(self.Iniciar)
        self.closeBtn.clicked.connect(self.Cerrar)

    def Iniciar(self):
        puerto = str(self.lineCOM.text())
        baudrate = int(self.lineBaudrate.text())
        fm = int(self.lineFM.text())
        Ventana = Visualizacion(puerto, baudrate, fm)
        Ventana.exec_()

    def Cerrar(self):
        self.close()

class Visualizacion(QDialog):
    def __init__(self, puerto, baudrate = 9600, fm = 100):
        super().__init__()
        uic.loadUi("Visualizacion.ui", self)
        # self.puerto = puerto
        # self.baudrate = baudrate
        self.CancelBTN.clicked.connect(self.volver)
        self.btnStart.clicked.connect(self.iniciar)
        self.btnStop.clicked.connect(self.parar)
        # fichero = open(os.path.realpath('C:/Users/usuario_2/Documents/sensorAgarre/Modelo de funciones mediante ML/RF'), 'rb')
        # self.RF = pickle.load(fichero)
        y = [a for a in range(0,1100,100)]
        y.insert(1, 50)
        y.insert(1, 25)
        x = [0, 1, 1.4, 1.75, 2.25, 2.5, 2.75, 2.90, 3, 3.15, 3.25, 3.4, 3.5]
        from sklearn.ensemble import RandomForestRegressor

        self.RF = RandomForestRegressor()
        x= np.reshape(x,(-1,1))
        y= np.reshape(y,(-1,1))

        from sklearn.compose import TransformedTargetRegressor
        # RFlog = TransformedTargetRegressor(RF,
        #                                   func = lambda x: x,
        #                                   inverse_func = lambda x: np.clip(x, 0, 1000))

        #self.RF.fit(x,y)
        self.RFlog = TransformedTargetRegressor(self.RF,
                                  func = lambda x: x,
                                  inverse_func = lambda x: np.clip(x, 0, 1000))
        self.RFlog.fit(x,y)
        self.Worker1 = Worker1(puerto =puerto, baudrate = baudrate, fm = fm)
        self.Worker1.update.connect(self.actualizar)
        self.sampling = False
        self.traces = dict()
        pg.setConfigOptions(antialias=True)
        self.Worker1.start()

    def actualizar(self, valor, tiempo):
        #if self.Worker1.serie.is_open:
        valor1= np.reshape(np.array(valor),(-1,1))
        valor2 = int(self.RFlog.predict(valor1))
        
        #for i in valor:
        self.progressBar.setValue(valor2)
        self.labelPeso.setText(f'Peso: {valor2} gramos')
        # name = 'Peso'
        # if name in self.traces:
        #     self.traces[name].setData(tiempo,valor)
        # else:
        #     self.traces[name] = self.graphicsView.plot(pen='y')

    def iniciar(self):
        try:
            self.Worker1.serie.open()
        except:
            pass

    def parar(self):
        self.Worker1.serie.close()

    def volver(self):
        self.close()

class Worker1(QThread):

    update = pyqtSignal(float, float)

    def __init__(self, puerto, fm, baudrate = 9600):
        super().__init__()
        self.muestreo = 1/fm
        self.puerto = puerto
        self.baudrate = baudrate
        self.tiempo = 0
        self.serie = serial.Serial(port = self.puerto, baudrate = self.baudrate)
        # self.tiempos  = []
        # self.valores = []

    def run(self):
        try:
            self.serie.close()
            self.serie.open()
        except:
            self.serie.open()
        while self.serie.isOpen():
            if self.serie.in_waiting:
                bits = int.from_bytes(self.serie.read(), 'little')
                #print(valor)
                voltaje = float(bits*5/1023) #Si 1023 son 5V, cuanto es el valor que tenemos ahora en en Voltaje segun bit
                #valor = 2
                self.tiempo += self.muestreo
                #self.tiempos.append(self.tiempo)
                #self.valores.append(valor)
                self.update.emit(voltaje, self.tiempo)
                # self.valores = []
                # self.tiempos = []
                time.sleep(1)

App = QApplication(sys.argv)
Root = MainWindow()
Root.show()
App.exec_()
