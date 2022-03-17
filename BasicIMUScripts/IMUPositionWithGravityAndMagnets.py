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
    Nt = unit_vector(tailIcm.magnetic)
    Gt = unit_vector(tailIcm.acceleration)
    Ot = unit_vector(np.cross(Nt, Gt))
    
    Nb = unit_vector(bodyIcm.magnetic)
    Gb = unit_vector(bodyIcm.acceleration)
    Ob = unit_vector(np.cross(Nb, Gb))
    
    M = np.array([Nt,Gt,Ot]).transpose()   #matrix to change from magnetic/gravity basis into tail basis
    Minv = np.linalg.inv(M)                #matrix to change from tail basis into magnetic/gravity basis
    
    B = np.array([Nb,Gb,Ob]).transpose()   #matrix to change from magnetic/gravity basis into body basis
    
    tailVectors = B.dot(Minv)
    vx = unit_vector(tailVectors.transpose()[0])
    
    
    print("\n\n")
    print("Orientation X:%.2f, Y: %.2f, Z: %.2f" % (vx[0], vx[1], vx[2]))
#     
#     print("\n\n")
#     print("Body Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (bodyMVec))
#     print("Tail Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (tailMVec))
    