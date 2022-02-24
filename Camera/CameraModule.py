from picamera import PiCamera
from time import sleep

class CameraModule:

    def __init__(self):
        self.camera = PiCamera()
    
    def take_picture(self):
        self.camera.capture("/home/pi/firebaseenv/woofwoofwearables/Camera/testimg.jpg")
        return "/home/pi/firebaseenv/woofwoofwearables/Camera/testimg.jpg"


