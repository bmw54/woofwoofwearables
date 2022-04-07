import numpy as np
import skinematics as skin
import skinematics.quat as sq
import IMUDataProcessing

tail_file = "twoSensorsRun-Tail.json"
body_file = "twoSensorsRun-Body.json"

tailTimes, tailQuats = IMUDataProcessing.filterFile(tail_file)
IMUDataProcessing.plotFilterOutput(tailTimes, tailQuats)
bodyTimes, bodyQuats = IMUDataProcessing.filterFile(body_file)
IMUDataProcessing.plotFilterOutput(bodyTimes, bodyQuats)

# Note: body and tail measurements aren't taken at the exact same time, and through the interpolation process, 
# they are slightly different lengths. I'm choosing to ignore this for now, but it should be addressed. The two
# series also don't seem to start at the same time. When the sample period is about 0.08 seconds, the body seems
# to start recording about 0.04 seconds before the tail

numPoints = min(len(tailTimes), len(bodyTimes))
quatDiffs = sq.q_mult(sq.q_inv(bodyQuats[:numPoints]), tailQuats[:numPoints])
print(quatDiffs.shape)
IMUDataProcessing.plotFilterOutput(tailTimes[:numPoints], quatDiffs)

# Matrix math to translate a vector reletive to the tail IMU into the basis of the body:
#           v2 = np.linalg.inv(B)@T@v
# T is the rotation matrix of the tail IMU (aka the change of basis matrix from the tail basis to the environment basis)
# B is the rotation matrix of the body IMU (aka the change of basis matrix from the body basis to the environment basis)
# This operation takes the vector, translates it into the environment basis, then into the body basis. The quaterion 
# operations are basically doing the same thing

