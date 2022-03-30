from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
from Camera.CameraModule import CameraModule
import time

data_module = IMUDataModule()
rpi_2_firebase = RPi2Firebase()
# camera_module = CameraModule()

trial_name = input("Trial run Name: ")
duration = 0.0
try:
    duration = int(input("Trial Duration (seconds): "))
except ValueError:
    print("Duration must be a number")
    duration = int(input("Trial Duration (seconds): "))


x_gyro_list = []
y_gyro_list = []
z_gyro_list = []

x_accel_list = []
y_accel_list = []
z_accel_list = []

x_mag_list = []
y_mag_list = []
z_mag_list = []

time_start = time.time()

while time.time() < time_start + duration:
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

    x_accel_list.append({"Time" : timestamp, "Value": x_acceleration}) 
    y_accel_list.append( {"Time" : timestamp, "Value": y_acceleration})
    z_accel_list.append({"Time" : timestamp, "Value": z_acceleration})

    x_gyro_list.append({"Time" : timestamp, "Value": x_gyro})
    y_gyro_list.append({"Time" : timestamp, "Value": y_gyro})
    z_gyro_list.append({"Time" : timestamp, "Value": z_gyro})

    x_mag_list.append({"Time" : timestamp, "Value": x_mag})
    y_mag_list.append({"Time" : timestamp, "Value": y_mag})
    z_mag_list.append({"Time" : timestamp, "Value": z_mag})
    time.sleep(.01)

print(trial_name + "trial complete after" + str(time.time() - time_start) + "seconds")

for i in range(0, len(x_accel_list)):
    rpi_2_firebase.send_timeseries_to_firebase(x_accel_list[i], trial_name, "X", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(y_accel_list[i], trial_name, "Y", "accel")
    rpi_2_firebase.send_timeseries_to_firebase(z_accel_list[i], trial_name, "Z", "accel")

    rpi_2_firebase.send_timeseries_to_firebase(x_gyro_list[i], trial_name, "X", "gyro")
    rpi_2_firebase.send_timeseries_to_firebase(y_gyro_list[i], trial_name, "Y", "gyro")
    rpi_2_firebase.send_timeseries_to_firebase(z_gyro_list[i], trial_name, "Z", "gyro")

    rpi_2_firebase.send_timeseries_to_firebase(x_mag_list[i], trial_name, "X", "mag")
    rpi_2_firebase.send_timeseries_to_firebase(y_mag_list[i], trial_name, "Y", "mag")
    rpi_2_firebase.send_timeseries_to_firebase(z_mag_list[i], trial_name, "Z", "mag")
    current_data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(current_data, "CurrentIMUData")
#     path =  camera_module.take_picture()
#     rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")

print("Pushing " +trial_name+ "trial to Firebase complete")

