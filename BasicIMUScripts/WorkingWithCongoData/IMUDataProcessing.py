import json
import skinematics as skin
import statistics as stat
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from ModifiedKalman import modifiedKalman

def checkTimeSeries(timeSeries, labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]):
    if not (len(labels) == len(timeSeries) == 9):
        print("invalid input length")
        return
    
    allTimes = combineTimeSeries(timeSeries)

    timeDiffs = [allTimes[i+1] - allTimes[i] for i in range(len(allTimes)-1)]
    timestep = stat.median(timeDiffs)

    print("Number of samples:", len(allTimes))
    print("Median time between samples: %.2f seconds" % (timestep))

    print("Gaps in the recording:")
    gapInds = [i for i in range(len(timeDiffs)) if round(timeDiffs[i]/timestep) > 1]
    for gi in gapInds:
        diff = timeDiffs[gi]
        print("\tBreak of %.2f seconds (~%0.2f samples) at index %d (timestamp %.2f)" % (diff, (diff/timestep)-1, gi, allTimes[gi]))
    
    allString = ""
    for i in range(len(allTimes)):
        allString += "-"
        if gapInds.count(i):
            skippedSamples = round(timeDiffs[i]/timestep)-1
            if skippedSamples >= 5:
                breakString = "[~~"+ str(skippedSamples) + "~~]"
            else:
                breakString = "[" + ("~"*max(skippedSamples-2, 0)) + ("]"*np.clip(skippedSamples-1, 0, 1))
            allString += breakString
    
    print("All:\t%s" % (allString))
    
    for i in range(len(labels)):
        newList = timeSeries[i]
        string = allString
        missingMeasurementIndices = [j for j in range(len(allTimes)) if not newList.count(allTimes[j])]
        for j in range(len(allTimes)):
            if missingMeasurementIndices.count(j):
                string = string.replace("-", "o", 1)
            else:
                string = string.replace("-", "x", 1)
        string = string.replace("x", "-")
        print("%s:\t%s" % (labels[i], string))
    return

def combineTimeSeries(timeSeries):
    # given several time series lists, combine them into one sorted list with no repeats
    allTimes = [item for sublist in timeSeries for item in sublist]
    allTimes = list(set(allTimes))
    allTimes.sort()
    return allTimes

def timeSeriesIntersection(timeSeries):
    timeIntersection = timeSeries[0]
    for series in timeSeries[1:]:
        for time in timeIntersection:
            if not series.count(time):
                timeIntersection.remove(time)
    return timeIntersection

def getTimeSeries(read_data):
    timeSeries = []
    for sensor in ['accel', 'mag', 'gyro']:
        for d in ['X', 'Y', 'Z']:
            newTimeSeries = [read_data[sensor][d][entry]["Time"] for entry in read_data[sensor][d]]
            newTimeSeries.sort()
            timeSeries += [newTimeSeries]
    
    labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]
    return timeSeries, labels

def reorganizeData(read_data, start=0, stop=-1):
    timeSeries = getTimeSeries(read_data)[0]
    timeCombined = combineTimeSeries(timeSeries)
    startTime = timeCombined[start]
    stopTime = timeCombined[stop]
    croppedTimeSeries = [[time for time in series if startTime <= time <= stopTime] for series in timeSeries]
    # get list of timestamps measured by all sensors
    timeIntersection = timeSeriesIntersection(croppedTimeSeries)
    data = {}
    data['time'] = timeIntersection
    for sensor in ['accel', 'mag', 'gyro']:
        for d in ['X', 'Y', 'Z']:
            values = [read_data[sensor][d][entry]["Value"] for entry in read_data[sensor][d]]
            times = [read_data[sensor][d][entry]["Time"] for entry in read_data[sensor][d]]
            data[sensor+d] = []
            for t in timeIntersection:
                data[sensor+d].append(values[times.index(t)])
    return data

def readAndInterpolateData(read_data, start=0, stop=-1):
    data = reorganizeData(read_data, start, stop)
    times = data['time']
    timeDiffs = [times[i+1] - times[i] for i in range(len(times)-1)]
    numsteps = round((times[-1] - times[0])/stat.median(timeDiffs))
    corrected_times = np.linspace(times[0], times[-1], numsteps)

    def interpolate_sensor(sensor):
        funcs = {}
        for d in ['X', 'Y', 'Z']:
            funcs[d] = interp1d(times, data[sensor+d])
        intps_list = [[funcs[d](ct) for ct in corrected_times] for d in ['X', 'Y', 'Z']]
        intps_array = np.array(intps_list).transpose()
        return intps_array

    accl_intps = interpolate_sensor('accel')
    gyro_intps = interpolate_sensor('gyro')
    mag_intps = interpolate_sensor('mag')
    return corrected_times, accl_intps, gyro_intps, mag_intps

def filterReadData(read_data, start=0, stop=-1):
    corrected_times, accl_intps, gyro_intps, mag_intps = readAndInterpolateData(read_data, start, stop)
    qOut = modifiedKalman(1.0/(corrected_times[1]-corrected_times[0]), accl_intps, gyro_intps, mag_intps)
    return corrected_times, qOut

def filterFile(file_name, start=0, stop=-1):
    with open(file_name, "r") as read_file: read_data = json.load(read_file)
    return filterReadData(read_data, start, stop)

def plotFilterOutput(times, qOut):
    timeStep = times[1]-times[0]
    degs = skin.quat.quat2deg(qOut)
    angvel = skin.quat.calc_angvel(qOut, 1.0/timeStep)

    # plot degree rotation
    fig = plt.figure()
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('Degree Rotation')
    plt.xlabel('Timestamp')
    plt.plot([datetime.fromtimestamp(ct) for ct in times], degs)
    plt.legend(['X', 'Y', 'Z'], loc='best')
    plt.grid(True)

    # plot angular velocity
    fig = plt.figure()
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('Angular Velocity')
    plt.xlabel('Timestamp')
    plt.plot([datetime.fromtimestamp(ct) for ct in times], angvel)
    plt.legend(['X', 'Y', 'Z'], loc='best')
    plt.grid(True)



    rotmats = [skin.quat.convert(q) for q in qOut]

    fig = plt.figure(figsize=plt.figaspect(2))
    ax = fig.add_subplot(311, projection='3d')
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    colors = ['r','b','g']

    def plotOrientation(i=int):
        sampleNum = i%len(times)
        # Vecs = (rotmats[sampleNum]@np.diag([1.5,0.5,0.5])).transpose()
        Vecs = (rotmats[sampleNum]@np.diag([1,1,1])).transpose()
        origin = np.zeros_like(Vecs) # origin point
        ax.clear()
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.quiver(*origin, Vecs[:,0], Vecs[:,1], Vecs[:,2], color = ['r','b','g','r','r','b','b','g','g'])
        ax.set_box_aspect((1, 1, 1))  # aspect ratio is 1:1:1 in data space
        ax.set_xlabel('X') # X-axis seems to be North
        ax.set_ylabel('Y') # Y-axis seems to be cross_product(Up, North)
        ax.set_zlabel('Z') # Z-axis seems to be Up


        ax2.clear()
        plt.sca(ax2)
        p = plt.plot([ct-times[0] for ct in times], degs)
        plt.axvline(times[sampleNum]-times[0], color='orange')
        for j in range(3): p[j].set_color(colors[j])
        plt.legend(['X', 'Y', 'Z'], loc='best')
        plt.yticks(rotation=90) #rotate the y-axis values
        plt.ylabel('Degree Rotation')
        plt.xlabel('Seconds')
        ax2.set_ylim([-180, 180])
        ax2.grid(True)

        ax3.clear()
        plt.sca(ax3)
        p = plt.plot([ct-times[0] for ct in times], angvel)
        plt.axvline(times[sampleNum]-times[0], color='orange')
        for j in range(3): p[j].set_color(colors[j])
        plt.legend(['X', 'Y', 'Z'], loc='best')
        plt.yticks(rotation=90) #rotate the y-axis values
        plt.ylabel('Angular Velocity')
        plt.xlabel('Seconds')
        ax3.grid(True)

    animator = ani.FuncAnimation(fig, plotOrientation, interval = timeStep*1000)

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # file_name = "woof-woof-wearables-default-rtdb-2-push-export.json"
    # file_name = "woof-woof-wearables-rtdb-michelle.json"
    # file_name = "Doherty-Hand.json"
    file_name = "Doherty-Hand0330.json"
    
    # vvv Uncomment to check data for missing entries and determine start and stop indices vvv
    # with open(file_name, "r") as read_file: read_data = json.load(read_file)
    # lists, labels = getTimeSeries(read_data)
    # checkTimeSeries(lists, labels)

    startIndex = 0
    stopIndex = -1

    times, qOut = filterFile(file_name, startIndex, stopIndex)
    plotFilterOutput(times, qOut)