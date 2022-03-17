import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
tailIcm = adafruit_icm20x.ICM20948(i2c, address = 104) #tail has solder jumper changing its address from 105 to 104 (0x69 to 0x68)

xangle = 0;
yangle = 0;
zangle = 0;
tlast = time.time()
t = 0;
while True:
    print("\n\n")
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (tailIcm.gyro))
    t = time.time()
    xangle += tailIcm.gyro[0]*(t-tlast)*180/np.pi
    yangle += tailIcm.gyro[1]*(t-tlast)*180/np.pi
    zangle += tailIcm.gyro[2]*(t-tlast)*180/np.pi
    tlast = t
    print("Angle X:%.2f, Y: %.2f, Z: %.2f degrees" % (xangle,yangle,zangle))
    time.sleep(0.1)
