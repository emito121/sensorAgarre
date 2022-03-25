from socket import timeout
import serial
import numpy as np
import time

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
# print(x)

serie = serial.Serial(port = 'COM11', baudrate = 9600, timeout = 1)
time.sleep(2)
#serie.set_buffer_size = 1

while True:
    if serie.in_waiting:
        mensaje = serie.read()
        mensaje = int.from_bytes(mensaje, 'little')
        #mensaje = int(mensaje.decode())
        
        valor = mensaje*5/255
        valor1 = np.array(valor)
        valor2= np.reshape(valor1,(-1,1))
        
        #print(mensaje)      
        #print(serie.inWaiting())
        fuerza = RFlog.predict(valor2)
        print(fuerza)
        #time.sleep(1)

