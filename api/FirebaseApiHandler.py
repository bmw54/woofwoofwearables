from flask_restful import Api, Resource, reqparse
from flask import jsonify
import numpy as np
from CalculationHandler import Calculation_Module
import pyrebase
import TwoIMUs
import MoodClassifier
import random


class FirebaseConfig:
  config = {

  "apiKey": "M3daySH0pEM5DcBgLbw8LVYJakBh2M8anFkDXq0I",

  "authDomain": "woof-woof-wearables.firebaseapp.com",

  "databaseURL": "https://woof-woof-wearables-default-rtdb.firebaseio.com",

  "storageBucket": "woof-woof-wearables.appspot.com"

  }
  firebase = pyrebase.initialize_app(config)
  db = firebase.database()
  storage = firebase.storage()

  def get_tail_and_body_data_from_firebase(folder_name, data_name, direction, version_number = 3):
    body_folder_name = "{FolderName}-body".format(folder_name)
    tail_folder_name = "{FolderName}-tail".format(folder_name)
    body_data = list(FirebaseConfig.db.child(body_folder_name).child("2-push").child(version_number).child(data_name).child(direction).get().val().values())
    tail_data = list(FirebaseConfig.db.child(tail_folder_name).child("2-push").child(version_number).child(data_name).child(direction).get().val().values())
    print(tail_data)
    print(type(tail_data))
    return tail_data, body_data


class TimeSeriesApiHandler(Resource):
  def get(self, folder_name, data_name, direction):
    tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    response_dict = {"Tail": tail_data, "Body" : body_data}
    response = jsonify(response_dict)
    response.status_code = 200 # or 400 or whatever
    return response


class AnglesHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    print(vectors)
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    response = jsonify(angles)
    response.status_code = 200 # or 400 or whatever
    return response

class PitchesHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    print(vectors)
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    response = jsonify(pitches)
    response.status_code = 200 # or 400 or whatever
    return response
  
class FrequencyHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    frequency = calculation_module.calculate_frequency(angles, timestamps)
    response = jsonify(frequency)
    response.status_code = 200 # or 400 or whatever
    return response

class AmplitudeHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    print(vectors)
    amplitude = calculation_module.calculate_average_amplitude(angles)
    response = jsonify(amplitude)
    response.status_code = 200 # or 400 or whatever
    return response
    
class SideBiasHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    side_bias = calculation_module.calculate_side_bias_from_vectors(vectors)
    print(vectors)
    response = jsonify(side_bias)
    response.status_code = 200 # or 400 or whatever
    return response

class MoodHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    side_bias = calculation_module.calculate_side_bias_from_vectors(vectors)
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    frequency = calculation_module.calculate_frequency(angles, timestamps)
    amplitude = calculation_module.calculate_average_amplitude(angles)
    mood = MoodClassifier.get_mood(frequency, amplitude, pitches, angles, side_bias)
    response = jsonify(mood)
    response.status_code = 200 # or 400 or whatever
    return response

class HappyPhotoHandler(Resource):
  def get(self, folder_name, window_num):
    window_num_list = [0,1,2,3,4,5]
    window_num = random.choice(window_num_list)
    image_url = list(FirebaseConfig.db.child("harnessrunzero-images").child("2-push").get().val().values())[window_num]['url']
    print(image_url)
    response = jsonify(image_url)
    response.status_code = 200 # or 400 or whatever
    return response

class ImageApiHandler(Resource):
  def get(self):
    data = FirebaseConfig.db.child("images").child("1-set").get().val()
    response = jsonify(data)
    response.status_code = 200 # or 400 or whatever
    return response

class DataApiHandler(Resource):
  def get(self, folder_name, data_num):
    data = FirebaseConfig.db.child(folder_name).child("1-set").child(data_num).get().val()
    response = jsonify(data)
    response.status_code = 200 # or 400 or whatever
    return response



class AveragesHandler(Resource):
  def get(self, folder_name, data_name, direction):
    calculation_module = Calculation_Module()
    data = list(FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val().values())
    averages = calculation_module.get_averages(10, data)
    response = jsonify(averages)
    response.status_code = 200 # or 400 or whatever
    return response

class VelocityHandler(Resource):
  def get(self, folder_name, data_name, direction):
    calculation_module = Calculation_Module()
    data = list(FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val().values())
    velocities = calculation_module.get_velocity_from_acceleration(data)
    averages = calculation_module.get_averages(10, velocities)
    response = jsonify(averages)
    response.status_code = 200 # or 400 or whatever
    return response

class PositionHandler(Resource):
  def get(self, folder_name, data_name, direction):
    calculation_module = Calculation_Module()
    data = list(FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val().values())
    positions = calculation_module.get_position_from_acceleration(data)
    response = jsonify(positions)
    response.status_code = 200 # or 400 or whatever
    return response


class FourierTransformHandler(Resource):
  def get(self, folder_name, window_num):
    calculation_module = Calculation_Module()
    #tail_data, body_data = FirebaseConfig.get_tail_and_body_data_from_firebase(folder_name, data_name, direction)
    vectors, timestamps = TwoIMUs.get_vectors_from_JSON()
    pitches, angles = calculation_module.get_pitches_angles_from_vectors(vectors)
    #print(vectors)
    calculation_module.calculate_ft(angles, timestamps)
    response = jsonify(0)
    response.status_code = 200 # or 400 or whatever
    return response

