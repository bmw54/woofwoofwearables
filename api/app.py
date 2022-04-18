from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
# from FirebaseApiHandler import *
from SpreadsheetApiHandler import *
#MAKE SURE ONLY ONE ApiHandler is uncommented

app = Flask(__name__, static_url_path='', static_folder='frontend/build') # should i change this?
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

"""
FirebaseApiHandler Urls
"""
# api.add_resource(TimeSeriesApiHandler, '/firebase/<string:folder_name>/<string:data_name>/<string:direction>')
# api.add_resource(ImageApiHandler, '/firebase/images')
# api.add_resource(DataApiHandler, '/firebase/<string:folder_name>/<int:data_num>')
# api.add_resource(AveragesHandler, '/firebase/averages/<string:folder_name>/<string:data_name>/<string:direction>')
# api.add_resource(VelocityHandler, '/firebase/velocity/<string:folder_name>/<string:data_name>/<string:direction>')
# api.add_resource(PositionHandler, '/firebase/position/<string:folder_name>/<string:data_name>/<string:direction>')
# api.add_resource(FourierTransformHandler, '/firebase/fouriertransform/<string:folder_name>/<int:window_num>')

# api.add_resource(PitchesHandler, '/firebase/pitches/<string:folder_name>/<int:window_num>')
# api.add_resource(AnglesHandler, '/firebase/angles/<string:folder_name>/<int:window_num>')
# api.add_resource(FrequencyHandler, '/firebase/frequency/<string:folder_name>/<int:window_num>')
# api.add_resource(AmplitudeHandler, '/firebase/amplitude/<string:folder_name>/<int:window_num>')
# api.add_resource(SideBiasHandler, '/firebase/sidebias/<string:folder_name>/<int:window_num>')
# api.add_resource(MoodHandler, '/firebase/mood/<string:folder_name>/<int:window_num>')
# api.add_resource(HappyPhotoHandler, '/firebase/happyphoto/<string:folder_name>/<int:window_num>')
# api.add_resource(SpreadsheetHandler, '/firebase/spreedsheet/<int:window_num>')

"""
SpreedSheetApiHandler Urls
"""
api.add_resource(PitchesHandler, '/spreadsheet/pitches/<int:window_num>')
api.add_resource(AnglesHandler, '/spreadsheet/angles/<int:window_num>')
api.add_resource(FrequencyHandler, '/spreadsheet/frequency/<int:window_num>')
api.add_resource(AmplitudeHandler, '/spreadsheet/amplitude/<int:window_num>')
api.add_resource(SideBiasHandler, '/spreadsheet/sidebias/<int:window_num>')
api.add_resource(MoodHandler, '/spreadsheet/mood/<int:window_num>')
api.add_resource(HappyPhotoHandler, '/spreadsheet/happyphoto/<int:window_num>')
