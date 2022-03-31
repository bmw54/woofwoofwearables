from scipy.interpolate import interp1d
import numpy as np
import json
import statistics as stat
import matplotlib.pyplot as plt

def interpolate(xlist, ylist, xval):
    if xval != np.clip(xval, min(xlist), max(xlist)):
        print("X value", xval, "out of range")
        xval = np.clip(xval, min(xlist), max(xlist))
        print("Rounding X value to:", xval)
    
    if xlist.count(xval): return ylist[xlist.index(xval)]

    x1_ind = [i for i in range(len(xlist)) if xlist[i]<xval][-1]
    x1 = xlist[x1_ind]
    x2 = xlist[x1_ind+1]
    y1 = ylist[x1_ind]
    y2 = ylist[x1_ind+1]
    yval = ((y2-y1)*1.0/(x2-x1)) * (xval-x1) + y1
    return yval

x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=41, endpoint=True)
plt.plot(x, y, 'o', xnew, [interpolate(list(x), list(y), xn) for xn in xnew], '-', xnew, f2(xnew), '--')
plt.legend(['data', 'mine', 'cubic'], loc='best')



with open("woof-woof-wearables-default-rtdb-2-push-export.json", "r") as read_file:
    read_data = json.load(read_file)

    accl = read_data['accel']
    acclx = accl['X']
    accly = accl['Y']
    acclz = accl['Z']

    accltx = [acclx[entry]["Time"] for entry in acclx]

    mag = read_data['mag']
    magx = mag['X']
    magy = mag['Y']
    magz = mag['Z']

    gyro = read_data['gyro']
    gyrox = gyro['X']
    gyroy = gyro['Y']
    gyroz = gyro['Z']




    # Construct some dictionaries
    # because magnetometer is missing values at index 6 and 16, we'll start after those indeces
    # edit: actually there seems to be a large break in the values for about a little over a minute, so we'll start after that
    # MAKE SURE PYTHON VERSION IS 3.6 OR LATER SO THAT DICTIONARIES MAINTAIN ORDER
    # Note: using the acceleration x value timestamps for everything

    data = {}
    for i in range(35,len(accltx)):
        new_accl = {'X': acclx[list(acclx.keys())[i]]["Value"],
                    'Y': accly[list(accly.keys())[i]]["Value"],
                    'Z': acclz[list(acclz.keys())[i]]["Value"]}

        new_gyro = {'X': gyrox[list(gyrox.keys())[i]]["Value"],
                    'Y': gyroy[list(gyroy.keys())[i]]["Value"],
                    'Z': gyroz[list(gyroz.keys())[i]]["Value"]}

        new_mag =  {'X': magx[list(magx.keys())[i]]["Value"],
                    'Y': magy[list(magy.keys())[i-1]]["Value"],
                    'Z': magz[list(magz.keys())[i-2]]["Value"]}
        
        data[accltx[i]] = {'ACCL': new_accl, 'GYRO': new_gyro, 'MAG': new_mag}

    # Correct for skipped measurements and imprecise sampling with interpolation
    times = list(data)
    timeDiffs = [times[i+1] - times[i] for i in range(len(times)-1)]
    numsteps = round((times[-1] - times[0])/stat.median(timeDiffs))
    timestep = (times[-1] - times[0])/numsteps

    xacc = [data[t]['ACCL']['X'] for t in times]
    corrected_times = np.linspace(times[0], times[-1], numsteps)

    f3 = interp1d(times, xacc, kind='cubic')
    plt.plot(times, xacc, 'o', corrected_times, [interpolate(times, xacc, ct) for ct in corrected_times], '-', corrected_times, f3(corrected_times), '--')
    plt.legend(['data', 'mine', 'cubic'], loc='best')
    plt.show()

    xacc_interpolated = [interpolate(times, [data[t]['ACCL']['X'] for t in times], ct) for ct in corrected_times]


