from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
from Camera.CameraModule import CameraModule
import time

data_module = IMUDataModule()
rpi_2_firebase = RPi2Firebase()
camera_module = CameraModule()

while True:
    data_module.poll_imu_data()
    current_data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(current_data, "CurrentIMUData")
    path =  camera_module.take_picture()
    print(path)
    rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")
    time.sleep(2)
