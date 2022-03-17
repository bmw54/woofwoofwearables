from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
from Camera.CameraModule import CameraModule
import time

data_module = IMUDataModule()
rpi_2_firebase = RPi2Firebase()
# camera_module = CameraModule()

while True:
    data_module.poll_imu_data()
    timestamp = data_module.get_timestamp()
    x_acceleration = data_module.get_X_acceleration()
    y_acceleration = data_module.get_Y_acceleration()
    z_acceleration = data_module.get_Z_acceleration()

    x_accel_data = {"Time" : timestamp, "Value": x_acceleration}
    y_accel_data = {"Time" : timestamp, "Value": y_acceleration}
    z_accel_data = {"Time" : timestamp, "Value": z_acceleration}
    rpi_2_firebase.send_timeseries_to_firebase(x_accel_data, "CurrentIMUData", "X", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(y_accel_data, "CurrentIMUData", "Y", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(z_accel_data, "CurrentIMUData", "Z", "accel")


    current_data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(current_data, "CurrentIMUData")
#     path =  camera_module.take_picture()
#     rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")
    time.sleep(2)
