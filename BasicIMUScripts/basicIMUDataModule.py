import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

def imu_data:
    (x,y,z) = icm.magnetic
    (x,y,z) = (max(x, 0.001), max(y, 0.001), max(z, 0.001))
    angle = (np.arctan(z/y), np.arctan(x/z), np.arctan(y/x))  
    return [icm.acceleration, icm.gyro, icm.magnetic, angle]

  

      
