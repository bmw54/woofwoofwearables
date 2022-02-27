from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.capture('/home/pi/woofwoofwearables/CameraScripts/testimg.jpg')
camera.stop_preview()

# camera.start_preview()
# camera.start_recording('/home/pi/woofwoofwearables/CameraScripts/testvideo.h264')
# sleep(5)
# camera.stop_recording()
# camera.stop_preview()