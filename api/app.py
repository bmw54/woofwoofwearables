from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from FirebaseApiHandler import *

app = Flask(__name__, static_url_path='', static_folder='frontend/build') # should i change this?
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(TimeSeriesApiHandler, '/firebase/<string:folder_name>/<string:data_name>/<string:direction>')
api.add_resource(ImageApiHandler, '/firebase/images')
api.add_resource(DataApiHandler, '/firebase/<string:folder_name>/<int:data_num>')
api.add_resource(AveragesHandler, '/firebase/averages/<string:folder_name>/<string:data_name>/<string:direction>')
api.add_resource(VelocityHandler, '/firebase/velocity/<string:folder_name>/<string:data_name>/<string:direction>')
api.add_resource(PositionHandler, '/firebase/position/<string:folder_name>/<string:data_name>/<string:direction>')