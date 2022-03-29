import json
import skinematics as skin
import statistics as stat
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
import matplotlib.animation as ani
import matplotlib.pyplot as plt


def checkTimeSeries(lables, dataLists):
    if not (len(lables) == len(dataLists) == 9):
        print("invalid input length")
        return
    
    allTimes = [item for sublist in dataLists for item in sublist]
    allTimes = list(set(allTimes))
    allTimes.sort()

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
        newList = dataLists[i]
        string = allString
        missingMeasurementIndeces = [j for j in range(len(allTimes)) if not newList.count(allTimes[j])]
        for j in range(len(allTimes)):
            if missingMeasurementIndeces.count(j):
                string = string.replace("-", "o", 1)
            else:
                string = string.replace("-", "x", 1)
        string = string.replace("x", "-")
        print("%s:\t%s" % (labels[i], string))
    return


file_name = "woof-woof-wearables-default-rtdb-2-push-export.json"
# file_name = "woof-woof-wearables-rtdb-michelle.json"

with open(file_name, "r") as read_file:
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

mag = read_data['mag']
magx = mag['X']
magy = mag['Y']
magz = mag['Z']

magtx = [magx[entry]["Time"] for entry in magx]
magty = [magy[entry]["Time"] for entry in magy]
magtz = [magz[entry]["Time"] for entry in magz]

gyro = read_data['gyro']
gyrox = gyro['X']
gyroy = gyro['Y']
gyroz = gyro['Z']

gyrotx = [gyrox[entry]["Time"] for entry in gyrox]
gyroty = [gyroy[entry]["Time"] for entry in gyroy]
gyrotz = [gyroz[entry]["Time"] for entry in gyroz]

lists = [accltx, acclty, accltz, magtx, magty, magtz, gyrotx, gyroty, gyrotz]
startIndex = 12
stopIndex = 59

labels = ["AcclX", "AcclY", "AcclZ", "MagnX", "MagnY", "MagnZ", "GyroX", "GyroY", "GyroZ"]
checkTimeSeries(labels, lists)


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



