import random
import TwoIMUs
from CalculationHandler import Calculation_Module
import json


def get_mood(frequency, amplitude, pitches, angles, side_bias):
    moods = ['excited','happy', 'angry', 'idle', 'alert']
    return random.choice(moods)



if __name__ == "__main__":
    cm = Calculation_Module()

    tail_file = "twoSensorsRun-Tail.json"
    body_file = "twoSensorsRun-Body.json"


    with open(tail_file, "r") as read_file: tail_data = json.load(read_file)
    with open(body_file, "r") as read_file: body_data = json.load(read_file)

    xvecs = TwoIMUs.get_vectors_TEMP(body_data, tail_data)
    
    timesList = []
    # for i in range(len(tail_data)):
    #     tailTimes = tail_data[i][0]
    #     bodyTimes = body_data[i][0]
    #     []
    #     for j in range(len(tailTimes)):
            



    pitches, angles =  cm.get_pitches_angles_from_vectors(xvecs)

    print(len(xvecs))

    frequency = cm.calculate_frequency(angles, timestamps)
    print(frequency)

    amplitude = cm.calculate_average_amplitude(angles)
    print(amplitude)

    side_bias  = cm.calculate_side_bias_from_vectors(angles)
    print(side_bias)