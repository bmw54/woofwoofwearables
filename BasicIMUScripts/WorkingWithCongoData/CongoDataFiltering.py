import json
import skinematics as skin
import statistics as stat
import numpy as np
from datetime import datetime


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
    corrected_times = np.linspace(times[0], times[-1], numsteps)

    def interpolate_sensor(sensor):
        intps_list = [[interpolate(times, [data[t][sensor][dir] for t in times], ct) for ct in corrected_times] for dir in ['X', 'Y', 'Z']]
        intps_array = np.array(intps_list).transpose()
        return intps_array

    accl_intps = interpolate_sensor('ACCL')
    gyro_intps = interpolate_sensor('GYRO')
    mag_intps = interpolate_sensor('MAG')


    # Apply kalman filter
    qOut = skin.imus.kalman(1.0/timestep, accl_intps, gyro_intps, mag_intps)
    # for i in range(len(qOut)):
    #     print(datetime.fromtimestamp(corrected_times[i]), skin.quat.quat2deg(qOut)[i])
    
    for i in range(len(qOut)):
        print(datetime.fromtimestamp(corrected_times[i]), [round(rads*180.0/np.pi) for rads in skin.quat.calc_angvel(qOut,1.0/timestep)[i]])
    # print("\n\n\n")
    # for i in range(len(qOut)):
    #     print(datetime.fromtimestamp(corrected_times[i]), skin.quat.calc_angvel(qOut,1.0/timestep)[i])


