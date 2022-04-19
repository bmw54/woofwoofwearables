import csv
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../api')
import CalculationHandler
import TwoIMUs
import IMUDataProcessing
import MoodClassifier


JSON_PATH = "../SavedJSONs/"
CSV_PATH = "./"
tail_file_name = "butterbean_4_16_alert-tail.json"
body_file_name = "butterbean_4_16_alert-body.json"
write_file_name = "butterbean_4_16_alert.csv"

tailFilteredData = IMUDataProcessing.filterFile(JSON_PATH + tail_file_name)
bodyFilteredData = IMUDataProcessing.filterFile(JSON_PATH + body_file_name)

quatsList, timesList = TwoIMUs.get_quats_from_filtered_data(tailFilteredData, bodyFilteredData)
xVecsList = TwoIMUs.quats_to_vectors(quatsList)


calculation_module = CalculationHandler.Calculation_Module()


# open the file in the write mode
with open(CSV_PATH + write_file_name, 'w') as f:
    # create the csv writer
    writer = csv.writer(f)
    labelrow = ["Frequency","Amplitude","Pitches","Angles","Side Bias","Mood","Image Url","Timestamps"]
    # write a row to the csv file
    writer.writerow(labelrow)

    for i in range(len(xVecsList)):
        # window i
        # row i+1
        pitches, angles = calculation_module.get_pitches_angles_from_vectors(xVecsList[i])
        frequency = calculation_module.calculate_frequency(angles, timesList[i])
        amplitude = calculation_module.calculate_average_amplitude(angles)
        side_bias  = calculation_module.calculate_side_bias_from_vectors(xVecsList[i])
        mood = MoodClassifier.get_mood(frequency, amplitude, pitches, angles, side_bias)
        image_url = ""
        row = [frequency, amplitude, pitches, angles, side_bias, mood, image_url, list(timesList[i])]
        # write a row to the csv file
        writer.writerow(row)

