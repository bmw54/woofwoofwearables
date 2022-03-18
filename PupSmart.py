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

    x_gyro = data_module.get_X_gyro()
    y_gyro = data_module.get_Y_gyro()
    z_gyro = data_module.get_Z_gyro()

    x_mag = data_module.get_X_magnetic()
    y_mag = data_module.get_Y_magnetic()
    z_mag = data_module.get_Z_magnetic()

    x_accel_data = {"Time" : timestamp, "Value": x_acceleration}
    y_accel_data = {"Time" : timestamp, "Value": y_acceleration}
    z_accel_data = {"Time" : timestamp, "Value": z_acceleration}

    x_gyro_data = {"Time" : timestamp, "Value": x_gyro}
    y_gyro_data = {"Time" : timestamp, "Value": y_gyro}
    z_gyro_data = {"Time" : timestamp, "Value": z_gyro}

    x_mag_data = {"Time" : timestamp, "Value": x_mag}
    y_mag_data = {"Time" : timestamp, "Value": y_mag}
    z_mag_data = {"Time" : timestamp, "Value": z_mag}

    rpi_2_firebase.send_timeseries_to_firebase(x_accel_data, "FridayPuppyRun", "X", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(y_accel_data, "FridayPuppyRun", "Y", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(z_accel_data, "FridayPuppyRun", "Z", "accel")

    rpi_2_firebase.send_timeseries_to_firebase(x_gyro_data, "FridayPuppyRun", "X", "gyro")
    rpi_2_firebase.send_timeseries_to_firebase(y_gyro_data, "FridayPuppyRun", "Y", "gyro")
    rpi_2_firebase.send_timeseries_to_firebase(z_gyro_data, "FridayPuppyRun", "Z", "gyro")

    rpi_2_firebase.send_timeseries_to_firebase(x_mag_data, "FridayPuppyRun", "X", "mag")
    rpi_2_firebase.send_timeseries_to_firebase(y_mag_data, "FridayPuppyRun", "Y", "mag")
    rpi_2_firebase.send_timeseries_to_firebase(z_mag_data, "FridayPuppyRun", "Z", "mag")


    current_data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(current_data, "CurrentIMUData")
#     path =  camera_module.take_picture()
#     rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")
    time.sleep(.1)
