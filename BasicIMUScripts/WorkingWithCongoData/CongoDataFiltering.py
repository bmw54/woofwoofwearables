import json
import skinematics as skin
import statistics as stat
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
import matplotlib.animation as ani
import matplotlib.pyplot as plt


# def interpolate(xlist, ylist, xval):
#     if xval != np.clip(xval, min(xlist), max(xlist)):
#         print("X value", xval, "out of range")
#         xval = np.clip(xval, min(xlist), max(xlist))
#         print("Rounding X value to:", xval)
    
#     if xlist.count(xval): return ylist[xlist.index(xval)]

#     x1_ind = [i for i in range(len(xlist)) if xlist[i]<xval][-1]
#     x1 = xlist[x1_ind]
#     x2 = xlist[x1_ind+1]
#     y1 = ylist[x1_ind]
#     y2 = ylist[x1_ind+1]
#     yval = ((y2-y1)*1.0/(x2-x1)) * (xval-x1) + y1
#     return yval

# def checkData(name, xlist, ylist, zlist):
#     if not (xlist == ylist == zlist):
#         print(name, "X time length:", len(xlist))
#         print(name, "Y time length:", len(ylist))
#         print(name, "Z time length:", len(zlist))
#         print("")

#         if(xlist != ylist):
#             print(name, "x and y times not equal")
#         if(xlist != zlist):
#             print(name, "x and z times not equal")
#         if(ylist != zlist):
#             print(name, "y and z times not equal")

#         print("")
        
#         listLengths = [len(xlist), len(ylist), len(zlist)]
#         largestList = [xlist, ylist, zlist][listLengths.index(max(listLengths))]
#         for time in largestList:
#             if not xlist.count(time):
#                 print(name, "X time list doesn't include time", time, "(index", largestList.index(time), "of largest list)")
#             if not ylist.count(time):
#                 print(name, "Y time list doesn't include time", time, "(index", largestList.index(time), "of largest list)")
#             if not zlist.count(time):
#                 print(name, "Z time list doesn't include time", time, "(index", largestList.index(time), "of largest list)")
#     else:
#         print(name, "time length:", len(xlist))
    
#     print("")

def checkTimeSeries(lables, dataLists):
    if not (len(lables) == len(dataLists) == 9):
        print("invalid input")
        return
    allTimes = list()
    for newList in dataLists:
        allTimes += newList
    
    allTimes = list(set(allTimes))
    allTimes.sort()
    print("Number of samples:", len(allTimes))

    timeDiffs = [allTimes[i+1] - allTimes[i] for i in range(len(allTimes)-1)]
    timestep = stat.median(timeDiffs)
    print("Median time between samples: %.2f seconds" % (timestep))
    timeBreakIndeces = [i for i in range(len(timeDiffs)) if round(timeDiffs[i]/timestep) > 1]
    print("Gaps in the recording:")
    for tbi in timeBreakIndeces:
        diff = timeDiffs[tbi]
        print("\tBreak of %.2f seconds (~%0.2f samples) at index %d (timestamp %.2f)" % (diff, (diff/timestep)-1, tbi, allTimes[tbi]))
    
    allTimeString = ""
    for i in range(len(allTimes)):
        allTimeString += "-"
        if timeBreakIndeces.count(i):
            skippedSamples = round(timeDiffs[i]/timestep)-1
            if skippedSamples >= 5:
                breakString = "[~~"+ str(skippedSamples) + "~~]"
            else:
                breakString = "[" + ("~"*max(skippedSamples-2, 0)) + ("]"*np.clip(skippedSamples-1, 0, 1))
            allTimeString += breakString
    
    print("All:\t%s" % (allTimeString))
    
    for i in range(len(labels)):
        newList = dataLists[i]
        string = allTimeString
        missingMeasurementIndeces = [j for j in range(len(allTimes)) if not newList.count(allTimes[j])]
        for j in range(len(allTimes)):
            if missingMeasurementIndeces.count(j):
                string = string.replace("-", "o", 1)
            else:
                string = string.replace("-", "x", 1)
        string = string.replace("x", "-")
        print("%s:\t%s" % (labels[i], string))
    return



with open("woof-woof-wearables-rtdb-michelle.json", "r") as read_file:
    # load json file
    read_data = json.load(read_file)

    # check the data for missing entries and inconsistencies
    accl = read_data['accel']
    acclx = accl['X']
    accly = accl['Y']
    acclz = accl['Z']

    accltx = [acclx[entry]["Time"] for entry in acclx]
    acclty = [accly[entry]["Time"] for entry in accly]
    accltz = [acclz[entry]["Time"] for entry in acclz]

    # checkData("Acceleration", accltx, acclty, accltz)

    mag = read_data['mag']
    magx = mag['X']
    magy = mag['Y']
    magz = mag['Z']

    magtx = [magx[entry]["Time"] for entry in magx]
    magty = [magy[entry]["Time"] for entry in magy]
    magtz = [magz[entry]["Time"] for entry in magz]

    # checkData("Magnetometer", magtx, magty, magtz)

    gyro = read_data['gyro']
    gyrox = gyro['X']
    gyroy = gyro['Y']
    gyroz = gyro['Z']

    gyrotx = [gyrox[entry]["Time"] for entry in gyrox]
    gyroty = [gyroy[entry]["Time"] for entry in gyroy]
    gyrotz = [gyroz[entry]["Time"] for entry in gyroz]

    # checkData("Gyroscope", gyrotx, gyroty, gyrotz)
    
    # maxTimeDiff = 0
    # maxTimeDiffStartIndex = None
    lists = [accltx, acclty, accltz, magtx, magty, magtz, gyrotx, gyroty, gyrotz]
    # maxList = None
    startIndex = 12
    stopIndex = 59
    # for i in range(9):
    #     newList = lists[i]
    #     timeDiffs = [newList[j+1] - newList[j] for j in range(12, stopIndex-1)]
    #     newMax = max(timeDiffs)
    #     if newMax > maxTimeDiff:
    #         maxTimeDiff = newMax
    #         maxTimeDiffStartIndex = timeDiffs.index(newMax)
    #         maxList = i
    
    # print("Maximum time jump is", maxTimeDiff, "seconds and occurs at index", maxTimeDiffStartIndex, "of time list", maxList)

    labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]
    checkTimeSeries(labels, lists)
    quit()


    # Construct some dictionaries
    # because magnetometer is missing values at index 6 and 16, we'll start after those indeces
    # edit: actually there seems to be a large break in the values for about a little over a minute,
    # so we'll start after that (for i in range(35,len(accltx)))
    # MAKE SURE PYTHON VERSION IS 3.6 OR LATER SO THAT DICTIONARIES MAINTAIN ORDER
    # Note: using the acceleration x value timestamps for everything

    data = {}
    for i in range(startIndex,stopIndex-1):
        new_accl = {'X': acclx[list(acclx.keys())[i]]["Value"],
                    'Y': accly[list(accly.keys())[i]]["Value"],
                    'Z': acclz[list(acclz.keys())[i]]["Value"]}

        new_gyro = {'X': gyrox[list(gyrox.keys())[i]]["Value"],
                    'Y': gyroy[list(gyroy.keys())[i]]["Value"],
                    'Z': gyroz[list(gyroz.keys())[i]]["Value"]}

        new_mag =  {'X': magx[list(magx.keys())[i]]["Value"],
                    'Y': magy[list(magy.keys())[i]]["Value"],
                    'Z': magz[list(magz.keys())[i]]["Value"]}
        
        data[accltx[i]] = {'ACCL': new_accl, 'GYRO': new_gyro, 'MAG': new_mag}

    # Correct for skipped measurements and imprecise sampling with interpolation
    times = list(data)
    timeDiffs = [times[i+1] - times[i] for i in range(len(times)-1)]
    numsteps = round((times[-1] - times[0])/stat.median(timeDiffs))
    timestep = (times[-1] - times[0])/numsteps
    corrected_times = np.linspace(times[0], times[-1], numsteps)


    def interpolate_sensor(sensor):
        funcs = {}
        for d in ['X', 'Y', 'Z']:
            funcs[d] = interp1d(times, [data[t][sensor][d] for t in times])
        intps_list = [[funcs[d](ct) for ct in corrected_times] for d in ['X', 'Y', 'Z']]
        intps_array = np.array(intps_list).transpose()
        return intps_array

    accl_intps = interpolate_sensor('ACCL')
    gyro_intps = interpolate_sensor('GYRO')
    mag_intps = interpolate_sensor('MAG')


    # Apply kalman filter
    qOut = skin.imus.kalman(1.0/timestep, accl_intps, gyro_intps, mag_intps)
    # filterResults = skin.quat.quat2deg(qOut)
    filterResults = skin.quat.calc_angvel(qOut, 1.0/timestep)

    fig = plt.figure(1)
    plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
    plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
    plt.ylabel('Degree Rotation')
    plt.xlabel('Timestamp')
    plt.plot([datetime.fromtimestamp(ct) for ct in corrected_times], filterResults)
    plt.legend(['X', 'Y', 'Z'], loc='best')
    
    print(datetime.fromtimestamp(corrected_times[0]))

    rotmats = [skin.quat.convert(q) for q in qOut]

    fig = plt.figure(3, figsize=plt.figaspect(1.5))
    ax = fig.add_subplot(211, projection='3d')
    ax2 = fig.add_subplot(212)

    colors = ['r','b','g']

    def plotOrientation(i=int):
        sampleNum = i%len(corrected_times)
        Vecs = (rotmats[sampleNum]@np.diag([1.5,0.5,0.5])).transpose()
        origin = np.zeros_like(Vecs) # origin point
        ax.clear()
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.quiver(*origin, Vecs[:,0], Vecs[:,1], Vecs[:,2], color = ['r','b','g','r','r','b','b','g','g'])

        ax2.clear()
        p = plt.plot([ct-corrected_times[0] for ct in corrected_times], filterResults)
        plt.axvline(corrected_times[sampleNum]-corrected_times[0], color='orange')
        for j in range(3): p[j].set_color(colors[j])
        plt.legend(['X', 'Y', 'Z'], loc='best')
        plt.yticks(rotation=90) #rotate the y-axis values
        plt.ylabel('Degree Rotation')
        plt.xlabel('Seconds')
        # ax2.set_ylim([-180, 180])
        ax2.grid(True)








    animator = ani.FuncAnimation(fig, plotOrientation, interval = timestep*1000)



    plt.tight_layout()
    plt.show()



