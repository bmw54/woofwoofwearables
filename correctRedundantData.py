import json


"""
There was an error with some of our data collection. When saving data in a version 3 structure,
a sample window's data would be repeated in all following windows. This program goes through
and corrects this problem. This program doesn't do a ton of error checking, so before you run it,
please make sure the data is in the correct format and that it does have this redundancy issue.
"""


JSONpath = './SavedJSONs/'
file_name = "Congo_4_12_22_idle2-body"
file_extension = ".json"

with open(JSONpath + file_name + file_extension, "r") as read_file: read_data = json.load(read_file)

for sensor in ['accel', 'mag', 'gyro']:
    for d in ['X', 'Y', 'Z']:
        sensorDict = read_data['3'][sensor][d]

        # go in order from shortest window to longest
        windowNames = list(sensorDict)
        windowLengths = [len(sensorDict[wn]) for wn in windowNames]
        sortedWindowLenInds = [windowLengths.index(wl) for wl in sorted(windowLengths)]
        sortedWindowNames = [windowNames[wli] for wli in sortedWindowLenInds]

        seenSamples = []
        for windowName in sortedWindowNames:
            for ss in seenSamples:
                if ss not in sensorDict[windowName]:
                    print("error: seenSamples not subset")
                    quit()
            
            sensorDict[windowName] = [dataDict for dataDict in sensorDict[windowName] if dataDict not in seenSamples]
            seenSamples += sensorDict[windowName]


string = input("write data to file %s? [y/n]" % (JSONpath + file_name + "-cleaned" + file_extension))

if string == "y":
    print("writing")
    with open(JSONpath + file_name + "-cleaned" + file_extension, "w") as fp: json.dump(read_data,fp, indent=2) 
else:
    print("not writing")