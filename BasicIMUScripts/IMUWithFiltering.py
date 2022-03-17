import time
import board
import adafruit_icm20x
import numpy as np
import skinematics as skin

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

numSamples = 100
acc = np.zeros((numSamples,3))
gyro = np.zeros((numSamples,3))
mag = np.zeros((numSamples,3))

for i in range(numSamples):
    acc[i] = icm.acceleration
    gyro[i] = icm.gyro
    mag[i] = icm.magnetic


while True:
    tstart = time.time()
    acc = np.append(acc[1:], [icm.acceleration], axis = 0)
    gyro = np.append(gyro[1:], [icm.gyro], axis = 0)
    mag = np.append(mag[1:], [icm.magnetic], axis = 0)
    
    qOut = skin.imus.kalman(1.0/(time.time()-tstart), acc, gyro, mag)
    print(skin.quat.quat2deg(qOut[-1]))
    print(time.time()-tstart)


