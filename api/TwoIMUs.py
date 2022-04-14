import numpy as np
import skinematics as skin
import skinematics.quat as sq
# importing IMUDataProcessing.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../api')

import IMUDataProcessing

def get_vectors(body_data, tail_data):

    PLOT = False
    tailTimes, tailQuats = IMUDataProcessing.filterReadData(tail_data)
    bodyTimes, bodyQuats = IMUDataProcessing.filterFile(body_data)

    if(PLOT): IMUDataProcessing.plotFilterOutput(tailTimes, tailQuats)
    if(PLOT): IMUDataProcessing.plotFilterOutput(bodyTimes, bodyQuats)

    # Note: body and tail measurements aren't taken at the exact same time, and through the interpolation process, 
    # they are slightly different lengths. I'm choosing to ignore this for now, but it should be addressed. The two
    # series also don't seem to start at the same time. When the sample period is about 0.08 seconds, the body seems
    # to start recording about 0.04 seconds before the tail

    numPoints = min(len(tailTimes), len(bodyTimes))
    quatDiffs = sq.q_mult(sq.q_inv(bodyQuats[:numPoints]), tailQuats[:numPoints])
    if(PLOT): IMUDataProcessing.plotFilterOutput(tailTimes[:numPoints], quatDiffs)

    # Matrix math to translate a vector reletive to the tail IMU into the basis of the body:
    #           v2 = np.linalg.inv(B)@T@v
    # T is the rotation matrix of the tail IMU (aka the change of basis matrix from the tail basis to the environment basis)
    # B is the rotation matrix of the body IMU (aka the change of basis matrix from the body basis to the environment basis)
    # This operation takes the vector, translates it into the environment basis, then into the body basis. The quaterion 
    # operations are basically doing the same thing

    rotMats = [sq.convert(q) for q in quatDiffs]
    xVecs = [rm[:,0] for rm in rotMats] # multiplying an x vector by a matrix is the same as just reading the first column of that matrix
    return xVecs

def get_vectors_TEMP(body_data, tail_data):
    # Temporary replacement to the above function so I can make it work with the new IMUDataProcessing.py
    # The idea is to replace the code in get_vectors() with something more like this when our team can meet
    # This function also does some error checking on certain assumptions about the output data

    tailFilteredData = IMUDataProcessing.filterReadData(tail_data)
    bodyFilteredData = IMUDataProcessing.filterFile(body_data)

    if len(tailFilteredData) != len(bodyFilteredData): 
        raise ValueError("""Body and tail have different number of windows
                            Body: %d windows
                            Tail: %d windows""" % (len(bodyFilteredData), len(tailFilteredData)))

    numWindows = len(tailFilteredData)

    xVecsList = []
    for i in range(len(tailFilteredData)):
        tailTimes, tailQuats = tailFilteredData[i]
        bodyTimes, bodyQuats = bodyFilteredData[i]

        if len(tailTimes) != len(bodyTimes): raise ValueError("""Window %d (out of %d) for Body and tail have different number of timestamps
                                                                Body: %d timestamps
                                                                Tail: %d timestamps""" % (i, numWindows, len(bodyTimes), len(tailTimes)))
        numTimes = len(bodyTimes)

        for j in range(len(tailTimes)):
            if tailTimes[j] != bodyTimes[j]: 
                raise ValueError("""Window %d (out of %d), timestamp %d (out of %d) for Body and tail are different
                                    Body: %d timestamps
                                    Tail: %d timestamps""" % (i, numWindows, j, numTimes, bodyTimes[j], tailTimes[j]))
        
        quatDiffs = sq.q_mult(sq.q_inv(bodyQuats), tailQuats)

        rotMats = [sq.convert(q) for q in quatDiffs]
        xVecs = [rm[:,0] for rm in rotMats] # multiplying an x vector by a matrix is the same as just reading the first column of that matrix
        xVecsList.append(xVecs)
    
    return xVecsList

def get_vectors_from_JSON():
    JSONpath = '../SavedJSONs/'
    tail_file = "Congo_4_12_22_idle2-tail-cleaned.json"
    body_file = "Congo_4_12_22_idle2-body-cleaned.json"

    # tailTimes, tailQuats = IMUDataProcessing.filterFile(tail_file)
    # bodyTimes, bodyQuats = IMUDataProcessing.filterFile(body_file)

    tailFilteredData = IMUDataProcessing.filterFile(JSONpath + tail_file)
    bodyFilteredData = IMUDataProcessing.filterFile(JSONpath + body_file)

    # Note: body and tail measurements aren't taken at the exact same time, and through the interpolation process, 
    # they are slightly different lengths. I'm choosing to ignore this for now, but it should be addressed. The two
    # series also don't seem to start at the same time. When the sample period is about 0.08 seconds, the body seems
    # to start recording about 0.04 seconds before the tail

    if len(tailFilteredData) != len(bodyFilteredData): 
        raise ValueError("""Body and tail have different number of windows
                            Body: %d windows
                            Tail: %d windows""" % (len(bodyFilteredData), len(tailFilteredData)))

    numWindows = len(tailFilteredData)

    xVecsList = []
    timesList = []

    for i in range(len(tailFilteredData)):
        tailTimes, tailQuats = tailFilteredData[i]
        bodyTimes, bodyQuats = bodyFilteredData[i]

        if len(tailTimes) != len(bodyTimes): raise ValueError("""Window %d (out of %d) for Body and tail have different number of timestamps
                                                                Body: %d timestamps
                                                                Tail: %d timestamps""" % (i, numWindows, len(bodyTimes), len(tailTimes)))
        
        numTimes = len(bodyTimes)

        for j in range(numTimes):
            if tailTimes[j] != bodyTimes[j]: 
                raise ValueError("""Window %d (out of %d), timestamp %d (out of %d) for Body and tail are different
                                    Body: %d timestamps
                                    Tail: %d timestamps""" % (i, numWindows, j, numTimes, bodyTimes[j], tailTimes[j]))
        
        quatDiffs = sq.q_mult(sq.q_inv(bodyQuats), tailQuats)

        # Matrix math to translate a vector reletive to the tail IMU into the basis of the body:
        #           v2 = np.linalg.inv(B)@T@v
        # T is the rotation matrix of the tail IMU (aka the change of basis matrix from the tail basis to the environment basis)
        # B is the rotation matrix of the body IMU (aka the change of basis matrix from the body basis to the environment basis)
        # This operation takes the vector, translates it into the environment basis, then into the body basis. The quaterion 
        # operations are basically doing the same thing

        rotMats = [sq.convert(q) for q in quatDiffs]
        xVecs = [rm[:,0] for rm in rotMats] # multiplying an x vector by a matrix is the same as just reading the first column of that matrix
        xVecsList.append(xVecs)
        timesList.append(tailTimes)
        # print(len(xVecs), len(timestamps))
    return xVecsList, timesList