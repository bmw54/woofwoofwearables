import numpy as np
import skinematics as skin
import skinematics.quat as sq
# importing IMUDataProcessing.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../api')

import IMUDataProcessing

"""
This file isn't a part of the project as a whole, just a place
where we've done some playing with the data
"""

PLOT = True

JSONpath = '../../SavedJSONs'

# tail_file = JSONpath + "/" + "twoSensorsRun-Tail.json"
# body_file = JSONpath + "/" + "twoSensorsRun-Body.json"
tail_file = JSONpath + "/" + "Congo_4_12_22_idle2-tail-cleaned.json"
body_file = JSONpath + "/" + "Congo_4_12_22_idle2-body-cleaned.json"

tailTimes, tailQuats = IMUDataProcessing.filterFile(tail_file)[0] # just look at the first one window
bodyTimes, bodyQuats = IMUDataProcessing.filterFile(body_file)[0]

# if(PLOT): IMUDataProcessing.plotFilterOutput(tailTimes, tailQuats)
if(PLOT): IMUDataProcessing.plotFilterOutput(bodyTimes, bodyQuats)

# Note: body and tail measurements aren't taken at the exact same time, and through the interpolation process, 
# they are slightly different lengths. I'm choosing to ignore this for now, but it should be addressed. The two
# series also don't seem to start at the same time. When the sample period is about 0.08 seconds, the body seems
# to start recording about 0.04 seconds before the tail

numPoints = min(len(tailTimes), len(bodyTimes))
quatDiffs = sq.q_mult(sq.q_inv(bodyQuats[:numPoints]), tailQuats[:numPoints])
# if(PLOT): IMUDataProcessing.plotFilterOutput(tailTimes[:numPoints], quatDiffs)

# Matrix math to translate a vector reletive to the tail IMU into the basis of the body:
#           v2 = np.linalg.inv(B)@T@v
# T is the rotation matrix of the tail IMU (aka the change of basis matrix from the tail basis to the environment basis)
# B is the rotation matrix of the body IMU (aka the change of basis matrix from the body basis to the environment basis)
# This operation takes the vector, translates it into the environment basis, then into the body basis. The quaterion 
# operations are basically doing the same thing

print(bodyQuats[0])

rotMats = [sq.convert(q) for q in quatDiffs]
xVecs = [rm[:,0] for rm in rotMats] # multiplying an x vector by a matrix is the same as just reading the first column of that matrix
