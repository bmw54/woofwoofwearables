import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
bodyIcm = adafruit_icm20x.ICM20948(i2c, address = 105) 
tailIcm = adafruit_icm20x.ICM20948(i2c, address = 104) #tail has solder jumper changing its address from 105 to 104 (0x69 to 0x68)

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

while True:
    bodyMVec = bodyIcm.magnetic
    tailMVec = tailIcm.magnetic
    print("\n\n")
    print("Body Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (bodyMVec))
    print("Tail Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (tailMVec))
    
    #calculate the angle between the two IMUs
    vb = unit_vector(bodyMVec)
    vt = unit_vector(tailMVec)
    
    angleRad = np.arccos(np.clip(np.dot(vb,vt), -1, 1))
    
    angleDeg = angleRad * 180/np.pi
    
    
    print("Angle Difference: %.2f degrees" % (angleDeg))
    time.sleep(0.1)