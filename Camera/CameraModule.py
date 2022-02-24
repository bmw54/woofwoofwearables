from picamera import PiCamera
from time import sleep

class CameraModule:

    def __init__(self):
      self.camera = PiCamera()
    
    def take_picture(self):
        self.camera.capture("ADD URL HERE")

    

    







