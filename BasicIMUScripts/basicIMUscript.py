import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)


while True:
    print("\n\n\n\nAcceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))
    (x,y,z) = icm.magnetic
    (x,y,z) = (max(x, 0.001), max(y, 0.001), max(z, 0.001))
    angle = (np.arctan(z/y), np.arctan(x/z), np.arctan(y/x))
    print("Angle X:%.2f, Y: %.2f, Z: %.2f uT" % (angle))
    print("")
    time.sleep(0.1)
