# just a short script to make it easy for me to test my changes in IMUDataProcessing.py
import IMUDataProcessing
import json


JSONpath = '../SavedJSONs/'

file_version1 = "woof-woof-wearables-rtdb-michelle.json"
file_version2 = "twoSensorsRun-Body.json"
file_version3 = "Congo_4_12_22_idle2-body-cleaned.json"

with open(JSONpath + file_version3, "r") as read_file: read_data = json.load(read_file)

version = IMUDataProcessing.dataVersion(read_data)
T, labels = IMUDataProcessing.getTimeSeries(read_data)

print("Length of timeseries list (number of windows):", len(T))
print("Length of first timeseries (number of sensors, should be 9):", len(T[0]))
print("Length of list of accel X timestamps from first timeseries:", len(T[0][0]))
print("accel X timestamps sorted?:", sorted(T[0][0]) == T[0][0])

print("Number of samples in each window:")
for i in range(len(T)):
    print("\t", len(T[i][0]))

times = [t for sublist in T for t in sublist[0]]
print("All windows and timestamps sorted in order?:", times == sorted(times))
print("Total number of samples in all windows:", len(times))

print()
Out = IMUDataProcessing.reorganizeData(read_data)
print(len(Out))
for d in Out:
    timeLength = len(d['time'])
    print(timeLength)

interpOut = IMUDataProcessing.readAndInterpolateData(read_data)
print(len(interpOut))
for l in interpOut:
    print(len(l[0]), len(l[1]), len(l[2]), len(l[3]))

Out = IMUDataProcessing.filterReadData(read_data)
print(len(Out))
for l in Out:
    print(len(l))
    print(len(l[0]), len(l[1]))

timeSeriesLists, labels = IMUDataProcessing.getTimeSeries(read_data)
for series in timeSeriesLists:
    IMUDataProcessing.checkTimeSeries(series, labels)


filteredOutput = IMUDataProcessing.filterReadData(read_data)
for [times, qOut] in filteredOutput:
    IMUDataProcessing.plotFilterOutput(times, qOut)

