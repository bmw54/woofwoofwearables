import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../api')
import IMUDataProcessing
import json




def printData(read_data):
    start_time = 1650138015
    print("FILE: tail")
    version = IMUDataProcessing.dataVersion(read_data)
    # use the accelerometer X sensor as a reference to determnie the number of windows
    numberOfWindows = len(read_data[str(version)]['accel']['X'])
    print("num windows:", numberOfWindows)
    timeSeriesList = []
    for windowNum in range(numberOfWindows):
        newTimeSeries = []
        for sensor in ['accel', 'mag', 'gyro']:
            for d in ['X', 'Y', 'Z']:
                sensorDict = read_data[str(version)][sensor][d]
                if windowNum >= len(sensorDict): continue
                windowName = list(sensorDict)[windowNum]
                windowData = sensorDict[windowName]
                newTimeList = [wd['Time'] for wd in windowData]
                newTimeList.sort()
                newTimeSeries += [newTimeList]
                print("Sensor %s%s window %d starts at time: %d" %(sensor, d, windowNum, newTimeList[0]-start_time))
        timeSeriesList += [newTimeSeries]
    timeSeriesList.sort()




JSON_PATH = "../SavedJSONs/"
tail_file_name = "butterbean_4_16_excited-tail.json"
write_file_name = "butterbean_4_16_excited-tail-corrected.json"


with open(JSON_PATH + tail_file_name, "r") as read_file: read_data = json.load(read_file)

version = IMUDataProcessing.dataVersion(read_data)

new_data = {}
new_data[str(version)] = {}

# use the accelerometer X sensor as a reference to determnie the number of windows
numberOfWindows = len(read_data[str(version)]['mag']['X'])
for sensor in ['accel', 'mag', 'gyro']:
    new_data[str(version)][sensor] = {}
    for d in ['X', 'Y', 'Z']:
        new_data[str(version)][sensor][d] = {}
        for windowNum in range(numberOfWindows):
            windowNameNum = windowNum
            if sensor == 'accel' and windowNum >= 1: windowNameNum += 1
            windowName = list(read_data[str(version)][sensor][d])[windowNameNum]
            new_data[str(version)][sensor][d][windowName] = read_data[str(version)][sensor][d][windowName]

printData(read_data)
printData(new_data)


string = input("write data to file %s? [y/n]" % (JSON_PATH + write_file_name))

if string == "y":
    print("writing")
    with open(JSON_PATH + write_file_name, "w") as fp: json.dump(new_data,fp, indent=2) 
else:
    print("not writing")
