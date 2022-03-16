import pandas as pd
import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

df = pd.DataFrame(columns = ['X_Acceleration','Y_Acceleration', 'Z_Acceleration', 'X_Gyro', 'Y_Gyro','Z_Gyro','X_Magnetometer', 'Y_Magnetometer', 'Z_Magnetometer'])



cycles = 1800
for i in range(1, cycles):
    acceleration = icm.acceleration
    gyro = icm.gyro
    magnetic = icm.magnetic

    print("\n\n\n\nAcceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
    print("")
    df = df.append({'X_Acceleration' : acceleration[0], 'Y_Acceleration' : acceleration[1], 'Z_Acceleration' : acceleration[2], 'X_Gyro' : gyro[0], 'Y_Gyro': gyro[1], 'Z_Gyro' :gyro[2], 'X_Magnetometer': magnetic[0], 'Y_Magnetometer' : magnetic[1], 'Z_Magnetometer' : magnetic[2]}, 
        ignore_index = True)
    time.sleep(.1)

