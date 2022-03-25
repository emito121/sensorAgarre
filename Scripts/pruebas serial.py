import serial
import numpy as np
import time

serie = serial.Serial(port = 'COM3', baudrate = 9600)

y = [a for a in range(0,1100,100)]
y.insert(1, 50)
y.insert(1, 25)
x = [0, 1, 1.4, 1.75, 2.25, 2.5, 2.75, 2.90, 3, 3.15, 3.25, 3.4, 3.5]
from sklearn.ensemble import RandomForestRegressor

RF = RandomForestRegressor()
x= np.reshape(x,(-1,1))
y= np.reshape(y,(-1,1))

from sklearn.compose import TransformedTargetRegressor

RFlog = TransformedTargetRegressor(RF,
                        func = lambda x: x,
                        inverse_func = lambda x: np.clip(x, 0, 1000))
RFlog.fit(x,y)

try:
    serie.open()
except:
    while serie.isOpen():
        if serie.in_waiting:
            bits = serie.read(8)

            bits = int.from_bytes(bits, 'little')
            
            voltaje = float(bits*5/255)

            print(voltaje)

            valor1= np.reshape(np.array(voltaje),(-1,1))
            valor2 = int(RFlog.predict(valor1))

            print(valor2)
            
            # RFlog = TransformedTargetRegressor(RF,
            #                                   func = lambda x: x,
            #                                   inverse_func = lambda x: np.clip(x, 0, 1000))

            #self.RF.fit(x,y)

