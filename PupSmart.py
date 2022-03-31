from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
from Camera.CameraModule import CameraModule
import time

def collect_data(data_module, x_gyro_list, y_gyro_list, z_gyro_list, x_accel_list, y_accel_list, z_accel_list, x_mag_list, y_mag_list, z_mag_list):
    tail_data_module.poll_imu_data()
    timestamp = tail_data_module.get_timestamp()
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
    return x_gyro_list, y_gyro_list, z_gyro_list, x_accel_list, y_accel_list, z_accel_list, x_mag_list, y_mag_list, z_mag_list

def send_data_to_firebase(x_gyro_list, y_gyro_list, z_gyro_list, x_accel_list, y_accel_list, z_accel_list, x_mag_list, y_mag_list, z_mag_list, trial_name, sensor_name):
    rpi_2_firebase.send_timeseries_to_firebase(x_accel_list, trial_name + "_" + sensor_name, "X", "accel", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_accel_list, trial_name + "_" + sensor_name, "Y", "accel", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_accel_list, trial_name + "_" + sensor_name, "Z", "accel", "2")

    rpi_2_firebase.send_timeseries_to_firebase(x_gyro_list, trial_name + "_" + sensor_name, "X", "gyro", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_gyro_list, trial_name + "_" + sensor_name, "Y", "gyro", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_gyro_list, trial_name + "_" + sensor_name, "Z", "gyro", "2")

    rpi_2_firebase.send_timeseries_to_firebase(x_mag_list, trial_name + "_" + sensor_name, "X", "mag", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_mag_list, trial_name + "_" + sensor_name, "Y", "mag", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_mag_list, trial_name + "_" + sensor_name, "Z", "mag", "2")

tail_data_module = IMUDataModule(address = 104)
body_data_module = IMUDataModule(address = 105)

rpi_2_firebase = RPi2Firebase()
# camera_module = CameraModule()

trial_name = input("Trial run Name: ")
duration = 0.0
try:
    duration = int(input("Trial Duration (seconds): "))
except ValueError:
    print("Duration must be a number")
    duration = int(input("Trial Duration (seconds): "))

input("Press Enter to continue...")

tail_x_gyro_list = []
tail_y_gyro_list = []
tail_z_gyro_list = []

tail_x_accel_list = []
tail_y_accel_list = []
tail_z_accel_list = []

tail_x_mag_list = []
tail_y_mag_list = []
tail_z_mag_list = []

body_x_gyro_list = []
body_y_gyro_list = []
body_z_gyro_list = []

body_x_accel_list = []
body_y_accel_list = []
body_z_accel_list = []

body_x_mag_list = []
body_y_mag_list = []
body_z_mag_list = []

sample_time = 0.05;

time_start = time.time()

while time.time() < time_start + duration:
    time_iter = time.time()
    print(time_iter - time_start)
    tail_x_gyro_list, tail_y_gyro_list, tail_z_gyro_list, tail_x_accel_list, tail_y_accel_list, tail_z_accel_list, tail_x_mag_list, tail_y_mag_list, tail_z_mag_list = collect_data(tail_data_module, tail_x_gyro_list, tail_y_gyro_list, tail_z_gyro_list, tail_x_accel_list, tail_y_accel_list, tail_z_accel_list, tail_x_mag_list, tail_y_mag_list, tail_z_mag_list)
    body_x_gyro_list, body_y_gyro_list, body_z_gyro_list, body_x_accel_list, body_y_accel_list, body_z_accel_list, body_x_mag_list, body_y_mag_list, body_z_mag_list = collect_data(body_data_module, body_x_gyro_list, body_y_gyro_list, body_z_gyro_list, body_x_accel_list, body_y_accel_list, body_z_accel_list, body_x_mag_list, body_y_mag_list, body_z_mag_list)

    current_time = time.time()
    time_left = sample_time - (current_time - time_iter) #
    if time_left <= 0:
        continue
    time.sleep(sample_time - (current_time - time_iter))

print(trial_name + "trial complete after" + str(time.time() - time_start) + "seconds")
send_data_to_firebase(tail_x_gyro_list, tail_y_gyro_list, tail_z_gyro_list, tail_x_accel_list, tail_y_accel_list, tail_z_accel_list, tail_x_mag_list, tail_y_mag_list, tail_z_mag_list, trial_name, "Tail")
send_data_to_firebase(body_x_gyro_list, body_y_gyro_list, body_z_gyro_list, body_x_accel_list, body_y_accel_list, body_z_accel_list, body_x_mag_list, body_y_mag_list, body_z_mag_list, trial_name, "Body")
#     path =  camera_module.take_picture()
#     rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = tail_data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")

print("Pushing " +trial_name+ " trial to Firebase complete")

