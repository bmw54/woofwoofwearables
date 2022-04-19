import random
import numpy as np
import csv
import matplotlib.pyplot as plt


def get_mood(frequency, amplitude, pitches, angles, side_bias):
    moods = ['excited','happy', 'angry', 'idle', 'alert']
    if amplitude > 20: return 'excited'
    if side_bias > 0.9: return 'alert'
    avgPitch = np.mean(pitches)
    if avgPitch > 0.325: return 'idle'
    return 'happy'
    



if __name__ == "__main__":
    CSV_PATH = "../CSVs/"
    file_names = ["butterbean_4_16_alert.csv",
                "butterbean_4_16_excited.csv",
                "butterbean_4_16_happy.csv",
                "butterbean_4_16_idle.csv"]
    labels = ["alert",
            "excited",
            "happy",
            "idle"]
    colors = ['k','r','y','p']

    data = []
    data.append(["freq", "ampl", "avgPitch", "sideBias", "label"])
    for i in range(len(file_names)):
        file = file_names[i]
        with open(CSV_PATH + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_list = list(csv_reader)[1:]
        for row in csv_list:
            # Frequency,Amplitude,Pitches,Angles,Side Bias,Mood,Image Url,Timestamps
            freq = float(row[0])
            ampl = float(row[1])
            pitches = list(map(float,row[2][1:-1].split(", ")))
            avgPitch = np.mean(pitches)
            angles = list(map(float,row[3][1:-1].split(", ")))
            sideBias = float(row[4])
            # print("%s: \tFreq:%g, \tAmpl:%g, \tAvgPitch:%g, \tSide Bias:%g" % (labels[i], freq, ampl, avgPitch, sideBias))
            data.append([freq, ampl, avgPitch, sideBias, labels[i]])
    
    for col in range(len(data[0])-1):
        plt.figure()
        feature = data[0][col]
        plt.title(feature)
        for mood in labels:
            x = [data[row][col] for row in range(len(data[1:])) if data[row][-1] == mood]
            y = np.zeros_like(x)+labels.index(mood)
            plt.plot(x, y, "o", lw=5)
            xmin = min(x)
            xmax = max(x)
            print("%s %s Range: \t[%g, %g]" % (mood, feature, xmin, xmax))
            xavg = np.mean(x)
            print("%s %s Mean: \t%g" % (mood, feature, xavg))
        plt.legend(labels)
    
    plt.show()