import numpy as np
import skinematics as skin
import skinematics.quat as sq
# importing IMUDataProcessing.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../api')

import IMUDataProcessing

def quats_to_vectors(quatsList):
    xVecsList = []
    for i in range(len(quatsList)):
        quatDiffs = quatsList[i]

        # The following matrix is a rotation we need to apply to our results to get it into the basis we need.
        # The bodyIMU is oriented with its X vector pointing towards the dog's head, the Y vector pointing to the dog's right,
        # and the Z vector pointing downwards. To do our calculations, we'd like the results from this function to be in a basis 
        # in which the X vector is the dog's left, the Y vector is pointed backwards, and the Z vector is pointed upwards.
        # This matrix corresponds to that transformation.
        SensorCorrection = np.array([[0,-1,0],
                                    [-1,0,0],
                                    [0,0,-1]])
        
        rotMats = [SensorCorrection @ sq.convert(q) for q in quatDiffs]
        xVecs = [rm[:,0] for rm in rotMats] # multiplying an x vector by a matrix is the same as just reading the first column of that matrix
        xVecsList.append(xVecs)
    return xVecsList

def get_quats_from_filtered_data(tailFilteredData, bodyFilteredData):
    if len(tailFilteredData) != len(bodyFilteredData): 
        raise ValueError("""Body and tail have different number of windows
                            Body: %d windows
                            Tail: %d windows""" % (len(bodyFilteredData), len(tailFilteredData)))
    numWindows = len(tailFilteredData)

    quatsList = []
    timesList = []

    # Note: body and tail measurements aren't taken at the exact same time.
    # I'm choosing to ignore this for now.
    for i in range(len(tailFilteredData)):
        tailTimes, tailQuats = tailFilteredData[i]
        bodyTimes, bodyQuats = bodyFilteredData[i]

        if len(tailTimes) != len(bodyTimes): raise ValueError("""Window %d (out of %d) for Body and tail have different number of timestamps
                                                                Body: %d timestamps
                                                                Tail: %d timestamps""" % (i, numWindows, len(bodyTimes), len(tailTimes)))
        
        quatDiffs = sq.q_mult(sq.q_inv(bodyQuats), tailQuats)
        # Matrix math to translate a vector reletive to the tail IMU into the basis of the body:
        #           v2 = np.linalg.inv(B)@T@v
        # T is the rotation matrix of the tail IMU (aka the change of basis matrix from the tail basis to the environment basis)
        # B is the rotation matrix of the body IMU (aka the change of basis matrix from the body basis to the environment basis)
        # This operation takes the vector, translates it into the environment basis, then into the body basis. The quaterion 
        # operations are basically doing the same thing

        quatsList.append(quatDiffs)
        timesList.append(tailTimes) #Note: we just use tailtimes
    
    return quatsList, timesList

def get_quats(body_data, tail_data):
    tailFilteredData = IMUDataProcessing.filterReadData(tail_data)
    bodyFilteredData = IMUDataProcessing.filterReadData(body_data)
    return get_quats_from_filtered_data(tailFilteredData, bodyFilteredData)

def get_vectors(body_data, tail_data):
    quatsList, timesList = get_quats(body_data, tail_data)
    xVecsList = quats_to_vectors(quatsList)
    return xVecsList, timesList


def get_quats_from_JSON(tail_file, body_file):
    tailFilteredData = IMUDataProcessing.filterFile(tail_file)
    bodyFilteredData = IMUDataProcessing.filterFile(body_file)
    return get_quats_from_filtered_data(tailFilteredData, bodyFilteredData)

def get_vectors_from_JSON(tail_file, body_file):
    quatsList, timesList = get_quats_from_JSON(tail_file, body_file)
    xVecsList = quats_to_vectors(quatsList)
    return xVecsList, timesList
