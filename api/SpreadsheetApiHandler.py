from tkinter import W
from flask_restful import Api, Resource, reqparse
from flask import jsonify
from datetime import datetime
import csv


"""
Spreadsheet - reach row is a different window
row[0] = frequency
row[1] = amplitude
row[2] = pitches
row[3] = angles
row[4] = side_bias
row[5] = mood
row[6] = image_url
row[7] = timestamps
"""

data_col_list = ["frequency", "amplitude", "pitches", "angles", "side-bias", "mood", "image-url", "timestamps"]
spreedsheet_path = "../CSVs/butterbean_4_16_happy.csv"

class SpreadSheetReader:
    def get_data(data_name, window_num):
        with open(spreedsheet_path) as file_obj:
            reader_obj = csv.reader(file_obj)
            reader_list = list(reader_obj)
            if window_num >= len(reader_list) - 1:
                window_num = len(reader_list) -2
            row = reader_list[window_num + 1]
            data = row[data_col_list.index(data_name)]
            return data
 

class AnglesHandler(Resource):
    def get(self, window_num):
        angles = SpreadSheetReader.get_data('angles', window_num)
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        angles = list(map(float, angles[1:-1].split(", ")))
        ret = []
        first_time = time_stamps[0]
        for i in range(len(time_stamps)):
            seconds = time_stamps[i] - first_time
            a_dict = {"Time": round(seconds,1), "Value": angles[i]}
            ret.append(a_dict)
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response

class PitchesHandler(Resource):
    def get(self, window_num):
        pitches = SpreadSheetReader.get_data('pitches', window_num)
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        pitches = list(map(float, pitches[1:-1].split(", ")))
        ret = []
        first_time = time_stamps[0]
        for i in range(len(time_stamps)):
            seconds = time_stamps[i] - first_time
            a_dict = {"Time": round(seconds,1), "Value": pitches[i]}
            ret.append(a_dict)
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response
  
class FrequencyHandler(Resource):
    def get(self, window_num):
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        datetime_obj = datetime.fromtimestamp(int(time_stamps[0])).time()
        a_dict = {"Time": str(datetime_obj), "Value": float(SpreadSheetReader.get_data('frequency', window_num))}
        ret = [a_dict]
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response

class AmplitudeHandler(Resource):
    def get(self, window_num):
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        datetime_obj = datetime.fromtimestamp(int(time_stamps[0])).time()
        a_dict = {"Time": str(datetime_obj), "Value": float(SpreadSheetReader.get_data('amplitude', window_num))}
        ret = [a_dict]
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response

    
class SideBiasHandler(Resource):
    def get(self, window_num):
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        datetime_obj = datetime.fromtimestamp(int(time_stamps[0])).time()
        a_dict = {"Time": str(datetime_obj), "Value": float(SpreadSheetReader.get_data('side-bias', window_num))}
        ret = [a_dict]
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response

class MoodHandler(Resource):
    def get(self, window_num):
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        datetime_obj = datetime.fromtimestamp(int(time_stamps[0])).time()
        a_dict = {"Time": str(datetime_obj), "Value": SpreadSheetReader.get_data('mood', window_num)}
        ret = [a_dict]
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response

class HappyPhotoHandler(Resource):
    def get(self, window_num):
        time_stamps = SpreadSheetReader.get_data('timestamps', window_num)
        time_stamps_list = time_stamps[1:-1].split(", ")
        time_stamps = list(map(float,time_stamps_list ))
        datetime_obj = datetime.fromtimestamp(int(time_stamps[0])).time()
        a_dict = {"Time": str(datetime_obj), "Value": SpreadSheetReader.get_data('image-url', window_num)}
        ret = [a_dict]
        response = jsonify(ret)
        response.status_code = 200 # or 400 or whatever
        return response
