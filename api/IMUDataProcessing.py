import json
import skinematics as skin
import statistics as stat
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from ModifiedKalman import modifiedKalman

def dataVersion(read_data):
    """
    Takes the data from a measurement trial and returns an integer corresponding
    to the version number of that data. If version isn't recognized, raises an
    error.
    """
    if (len(read_data) == 3) and ('accel' in read_data) and ('mag' in read_data) and ('gyro' in read_data): return 1
    if len(read_data) == 1: return int(list(read_data)[0])
    raise ValueError("Error reading data version number. Data doesn't seem to have the right format")

def checkTimeSeries(timeSeries, labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]):
    """
    Input: timeSeries - a list of 9 sublists, each of which contain the time series data
    stored for a particular sensor (AccelerometerX, MagnetometerY, GyroscopeZ, etc.).
        labels - the names corresponding to each of these sublists
    
    This function prints out visual representations of the timeseries and its holes to make
    it easier to spot holes and errors. This function also calculates and prints helpful 
    information about the time series data.

    This function operates on a single sample window, not a whole data collection trial.
    """
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
    """
    Input: timeSeries - a list of 9 sublists, each of which contain the time series data
    stored for a particular sensor (AccelerometerX, MagnetometerY, GyroscopeZ, etc.).
    
    Output: the union of these lists sorted in order. This is a list of all timestamps 
    at which we've recorded any data for a given sample window. This list contains no 
    repeats and is sorted.

    This function operates on a single sample window, not a whole data collection trial.
    """
    allTimes = [item for sublist in timeSeries for item in sublist]
    allTimes = list(set(allTimes))
    allTimes.sort()
    return allTimes

def timeSeriesIntersection(timeSeries):
    """
    Input: timeSeries - a list of 9 sublists, each of which contain the time series data
    stored for a particular sensor (AccelerometerX, MagnetometerY, GyroscopeZ, etc.).
    
    Output: the intesection of these lists sorted in order. This is a list of all the 
    timestamps for which all of the sensors have data recorded. This list contains no
    repeats and is sorted.

    This function operates on a single sample window, not a whole data collection trial.
    """
    timeIntersection = timeSeries[0]
    for series in timeSeries[1:]:
        for time in timeIntersection:
            if not series.count(time):
                timeIntersection.remove(time)
    return timeIntersection

def getTimeSeries(read_data):
    """
    *deep breath* ... *deep exhale*
    
    Ok so
    
    This function takes the data from a measurement trial as input
    
    A measuement trial is split up into one or more measurement windows, periods
    of time during the trial during which the pi is recording data
    
    This function returns a two lists. One is a list of labels, the other is a 
    list where each item is a "time series object" and corresponds to a single
    measurement window. This list of time series objects are sorted in the order
    in which the measurement windows were recorded.
    
    A "time series object" means a list of nine lists, one list for each of the
    nine sensors (AccelerometerX, MagnetometerY, GyroscopeZ, etc.). Each sublist
    contains the timestamps recorded by that sensor. These timestamps are sorted
    in chronological order.

    The returned list of labels shows how the sensor data is ordered within each
    timeseries object. The first list in a timeseries object corresponds to the
    first label in the list of labels.
    """

    version = dataVersion(read_data)
    labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]

    if version == 1:
        # version 1 only has one long window
        timeSeries = []
        for sensor in ['accel', 'mag', 'gyro']:
            for d in ['X', 'Y', 'Z']:
                newTimeList = [read_data[sensor][d][key]["Time"] for key in read_data[sensor][d]]
                newTimeList.sort()
                timeSeries += [newTimeList]
        return [timeSeries], labels
    

    if version == 2:
        # version 2 only has one long window
        timeSeries = []
        for sensor in ['accel', 'mag', 'gyro']:
            for d in ['X', 'Y', 'Z']:
                sensorDict = read_data[str(version)][sensor][d]
                if len(sensorDict) != 1:
                    raise ValueError("""Error reading data from datafile. Dictionary for %s %s has more than one entry.
                                        Data doesn't seem to have the right format""" % (sensor, d))
                dataDictList = list(sensorDict.values())[0]
                newTimeList = [dict["Time"] for dict in dataDictList]
                newTimeList.sort()
                timeSeries += [newTimeList]
        return [timeSeries], labels


    if version == 3:
        # use the accelerometer X sensor as a reference to determnie the number of windows
        numberOfWindows = len(read_data[str(version)]['accel']['X'])
        timeSeriesList = []
        for windowNum in range(numberOfWindows):
            newTimeSeries = []
            for sensor in ['accel', 'mag', 'gyro']:
                for d in ['X', 'Y', 'Z']:
                    sensorDict = read_data[str(version)][sensor][d]
                    if len(sensorDict) != numberOfWindows:
                        raise ValueError("""Error reading data from datafile. Sensors have an inconsistent number of 
                                            windows. accel X has %d sample windows while %s %s has %d sample windows""" 
                                            % (numberOfWindows, sensor, d, len(sensorDict)))
                    windowName = list(sensorDict)[windowNum]
                    windowData = sensorDict[windowName]
                    newTimeList = [wd['Time'] for wd in windowData]
                    newTimeList.sort()
                    newTimeSeries += [newTimeList]
            timeSeriesList += [newTimeSeries]
        timeSeriesList.sort()
        return timeSeriesList, labels


    raise ValueError("Error reading timeseries. getTimeSeries doesn't recognize the given version:", version)

def reorganizeData(read_data):
    """
    Input: read_data - the data read from firebase in dictionary form

    Output: The same data but sorted into a list of dictionaries.
    These dictionaries are organized in a slightly more intuitive way and remove
    the autogenerated keys which are stored in the firebase dataset. Each of the
    dictionaries corresponds to the data from a single sample window and they're
    sorted in chronological order.

    The dictionaries have the following structure:
    data = {"time" : [list of timestamps at which all the sensors have data],
            "accelX" : [list of values corresponding to those timestamps]
            "accelY" : [ " ]
               etc...
            }
    """
    version = dataVersion(read_data)
    timeSeriesList, labels = getTimeSeries(read_data)
    dataDictList = []
    for timeSeries in timeSeriesList:
        # get list of timestamps measured by all sensors
        timeIntersection = timeSeriesIntersection(timeSeries)
        data = {}
        data['time'] = timeIntersection
        for sensor in ['accel', 'mag', 'gyro']:
            for d in ['X', 'Y', 'Z']:
                if version == 1:
                    values = [read_data[sensor][d][entry]["Value"] for entry in read_data[sensor][d]]
                    times = [read_data[sensor][d][entry]["Time"] for entry in read_data[sensor][d]]
                elif version == 2:
                    dictList = list(read_data[str(version)][sensor][d].values())[0]
                    values = [dict["Value"] for dict in dictList]
                    times = [dict["Time"] for dict in dictList]
                elif version == 3:
                    # get list of all times and values in the trial
                    dictList = [dict for sublist in list(read_data[str(version)][sensor][d].values()) for dict in sublist]
                    values = [dict["Value"] for dict in dictList]
                    times = [dict["Time"] for dict in dictList]

                data[sensor+d] = []
                for t in timeIntersection:
                    data[sensor+d].append(values[times.index(t)])
        dataDictList.append(data)
    return dataDictList

def readAndInterpolateData(read_data):
    """
    Input: read_data - the data read from firebase in dictionary form

    Output: The result from interpolating that data. For each sensor, this function
    finds the median difference between samples in the data and predicts what the 
    value of the data would be if sampled at exactly that rate. This is output in
    a format that is intended to be easy to plug directly into our kalman filter
    function.

    The output is a list in which each item corresponds to a sample window.
    Each item in the output is a 4 item list of the form:

        [corrected_times, accl_intps, gyro_intps, mag_intps]
    
    The last three items in this list (accl_intps, gyro_intps, mag_intps) are all
    3xN arrays where N is the number of interpolated samples. They correspond to the
    accelerometer, gyroscope, and magnetometer. Each row of these arrays corresponds
    to the interpolated x, y, and z values for the given sensor at the cooresponding 
    timestamp in corrected_times.

    The output is sorted in the order in which the sample windows were recorded
    """
    dataDicts = reorganizeData(read_data)
    interpolatedData = []
    for data in dataDicts:
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
        interpolatedData.append([corrected_times, accl_intps, gyro_intps, mag_intps])
    return interpolatedData

def filterReadData(read_data):
    interpolatedData = readAndInterpolateData(read_data)
    filteredData = []
    for data in interpolatedData:
        # apply the kalman filter to the data from each window
        [corrected_times, accl_intps, gyro_intps, mag_intps] = data
        qOut = modifiedKalman(1.0/(corrected_times[1]-corrected_times[0]), accl_intps, gyro_intps, mag_intps)
        filteredData.append([corrected_times, qOut])
    return filteredData

def filterFile(file_name):
    with open(file_name, "r") as read_file: read_data = json.load(read_file)
    return filterReadData(read_data)

def plotFilterOutput(times, qOut):
    """
    This function takes the timestamps and quaternions from a single sample window
    and plots them with detailed and animated graphs.

    This function operates on a single sample window, not a whole data collection trial.
    """
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
        Vecs = (rotmats[sampleNum]@np.diag([1.5,0.5,0.5])).transpose()
        # Vecs = (rotmats[sampleNum]@np.diag([1,1,1])).transpose()
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
    JSONpath = '../SavedJSONs/'
    # file_name = "woof-woof-wearables-default-rtdb-2-push-export.json"
    # file_name = "woof-woof-wearables-rtdb-michelle.json"
    # file_name = "Doherty-Hand.json"
    # file_name = "Doherty-Hand0330.json"
    file_name = "twoSensorsRun-Tail.json"
    file_name = "Congo_4_12_22_idle2-body-cleaned.json"
    
    # vvv Uncomment to check data for missing entries and determine start and stop indices vvv
    # with open(JSONpath + file_name, "r") as read_file: read_data = json.load(read_file)
    # timeSeriesLists, labels = getTimeSeries(read_data)
    # for series in timeSeriesLists:
    #     checkTimeSeries(series, labels)

    filteredOutput = filterFile(JSONpath + file_name)
    for [times, qOut] in filteredOutput:
        plotFilterOutput(times, qOut)