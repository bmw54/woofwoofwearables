import json

from numpy import size

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
    # MAKE SURE PYTHON VERSION IS 3.6 OR LATER SO THAT DICTIONARIES MAINTAIN ORDER
    # Note: using the acceleration x value timestamps for everything

    data = {}
    for i in range(17,len(accltx)):
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

    # print(list(data.values())[0])
    print(data)

