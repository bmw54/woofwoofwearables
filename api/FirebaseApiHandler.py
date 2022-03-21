from re import A
from flask_restful import Api, Resource, reqparse
from flask import jsonify
from numpy import average
from Calculation_Handler import Averages_Module, Velocity_Module
import pyrebase

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



class TimeSeriesApiHandler(Resource):
  def get(self, folder_name, data_name, direction):
    data = FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val()
    print(type(data))
    response = jsonify(list(data.values()))
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
    average_module = Averages_Module()
    data = list(FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val().values())
    averages = average_module.get_averages(10, data)
    response = jsonify(averages)
    response.status_code = 200 # or 400 or whatever
    return response

class VelocityHandler(Resource):
  def get(self, folder_name, data_name, direction):
    velocity_module = Velocity_Module()
    average_module = Averages_Module()
    data = list(FirebaseConfig.db.child(folder_name).child("2-push").child(data_name).child(direction).get().val().values())
    velocities = velocity_module.get_velocity_from_acceleration(data)
    averages = average_module.get_averages(10, velocities)
    response = jsonify(averages)
    response.status_code = 200 # or 400 or whatever
    return response

