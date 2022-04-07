import numpy as np
import skinematics as skin
import IMUDataProcessing

T = skin.rotmat.R('z', 45)@skin.rotmat.R('y', 45) # change of basis from the tail IMU to the world basis
B = skin.rotmat.R('z', 45) # change of basis from the body IMU to the world basis

v = np.array([[1,0,0]]).transpose()

v2 = np.linalg.inv(B)@T@v

print(v2)