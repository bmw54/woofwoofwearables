from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
from Camera.CameraModule import CameraModule
import time

def collect_data(tail_data_module, body_data_module):
    tail_data_module.poll_imu_data()
    body_data_module.poll_imu_data()

    timestamp = tail_data_module.get_timestamp()
    x_acceleration = tail_data_module.get_X_acceleration()
    y_acceleration = tail_data_module.get_Y_acceleration()
    z_acceleration = tail_data_module.get_Z_acceleration()

    x_gyro = tail_data_module.get_X_gyro()
    y_gyro = tail_data_module.get_Y_gyro()
    z_gyro = tail_data_module.get_Z_gyro()

    x_mag = tail_data_module.get_X_magnetic()
    y_mag = tail_data_module.get_Y_magnetic()
    z_mag = tail_data_module.get_Z_magnetic()

    x_acceleration = {"Time" : timestamp, "Value": x_acceleration}
    y_acceleration =  {"Time" : timestamp, "Value": y_acceleration}
    z_acceleration = {"Time" : timestamp, "Value": z_acceleration}

    x_gyro = {"Time" : timestamp, "Value": x_gyro}
    y_gyro = {"Time" : timestamp, "Value": y_gyro}
    z_gyro = {"Time" : timestamp, "Value": z_gyro}

    x_mag = {"Time" : timestamp, "Value": x_mag}
    y_mag = {"Time" : timestamp, "Value": y_mag}
    z_mag =  {"Time" : timestamp, "Value": z_mag}

    body_timestamp = body_data_module.get_timestamp()
    body_x_acceleration = tail_data_module.get_X_acceleration()
    body_y_acceleration = tail_data_module.get_Y_acceleration()
    body_z_acceleration = tail_data_module.get_Z_acceleration()

    body_x_gyro = tail_data_module.get_X_gyro()
    body_y_gyro = tail_data_module.get_Y_gyro()
    body_z_gyro = tail_data_module.get_Z_gyro()

    body_x_mag = tail_data_module.get_X_magnetic()
    body_y_mag = tail_data_module.get_Y_magnetic()
    body_z_mag = tail_data_module.get_Z_magnetic()

    body_x_acceleration = {"Time" : timestamp, "Value": body_x_acceleration}
    body_y_acceleration =  {"Time" : timestamp, "Value": body_y_acceleration}
    body_z_acceleration = {"Time" : timestamp, "Value": body_z_acceleration}

    body_x_gyro = {"Time" : timestamp, "Value": body_x_gyro}
    body_y_gyro = {"Time" : timestamp, "Value": body_y_gyro}
    body_z_gyro = {"Time" : timestamp, "Value": body_z_gyro}

    body_x_mag = {"Time" : timestamp, "Value": body_x_mag}
    body_y_mag = {"Time" : timestamp, "Value": body_y_mag}
    body_z_mag =  {"Time" : timestamp, "Value": body_z_mag}
    
    return  x_acceleration, y_acceleration, z_acceleration, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag, body_x_acceleration, body_y_acceleration, body_z_acceleration, body_x_gyro, body_y_gyro, body_z_gyro, body_x_mag, body_y_mag, body_z_mag

def send_data_to_firebase(x_gyro_list, y_gyro_list, z_gyro_list, x_accel_list, y_accel_list, z_accel_list, x_mag_list, y_mag_list, z_mag_list, trial_name):
    rpi_2_firebase.send_timeseries_to_firebase(x_accel_list, trial_name, "X", "accel", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_accel_list, trial_name, "Y", "accel", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_accel_list, trial_name, "Z", "accel", "2")

    rpi_2_firebase.send_timeseries_to_firebase(x_gyro_list, trial_name, "X", "gyro", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_gyro_list, trial_name, "Y", "gyro", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_gyro_list, trial_name, "Z", "gyro", "2")

    rpi_2_firebase.send_timeseries_to_firebase(x_mag_list, trial_name, "X", "mag", "2")
    rpi_2_firebase.send_timeseries_to_firebase(y_mag_list, trial_name, "Y", "mag", "2")
    rpi_2_firebase.send_timeseries_to_firebase(z_mag_list, trial_name, "Z", "mag", "2")

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
    x_acceleration, y_acceleration, z_acceleration, x_gyro, y_gyro, z_gyro, x_mag, y_mag, z_mag, body_x_acceleration, body_y_acceleration, body_z_acceleration, body_x_gyro, body_y_gyro, body_z_gyro, body_x_mag, body_y_mag, body_z_mag = collect_data(tail_data_module, body_data_module)
    tail_x_accel_list.append(x_acceleration)
    tail_y_accel_list.append(y_acceleration)
    tail_z_accel_list.append(z_acceleration)
    tail_x_gyro_list.append(x_gyro)
    tail_y_gyro_list.append(y_gyro)
    tail_z_gyro_list.append(z_gyro)
    tail_x_mag_list.append(x_mag)
    tail_y_mag_list.append(y_mag)
    tail_z_mag_list.append(z_mag)

    body_x_accel_list.append(body_x_acceleration)
    body_y_accel_list.append(body_y_acceleration)
    body_z_accel_list.append(body_z_acceleration)
    body_x_gyro_list.append(body_x_gyro)
    body_y_gyro_list.append(body_y_gyro)
    body_z_gyro_list.append(body_z_gyro)
    body_x_mag_list.append(body_x_mag)
    body_y_mag_list.append(body_y_mag)
    body_z_mag_list.append(body_z_mag)

    current_time = time.time()
    time_left = sample_time - (current_time - time_iter) #
    if time_left <= 0:
        continue
    time.sleep(sample_time - (current_time - time_iter))

print(trial_name + "trial complete after" + str(time.time() - time_start) + "seconds")
send_data_to_firebase(tail_x_gyro_list, tail_y_gyro_list, tail_z_gyro_list, tail_x_accel_list, tail_y_accel_list, tail_z_accel_list, tail_x_mag_list, tail_y_mag_list, tail_z_mag_list, trial_name)
send_data_to_firebase(body_x_gyro_list, body_y_gyro_list, body_z_gyro_list, body_x_accel_list, body_y_accel_list, body_z_accel_list, body_x_mag_list, body_y_mag_list, body_z_mag_list, trial_name)
#     path =  camera_module.take_picture()
#     rpi_2_firebase.send_image_to_firebase(path, "testimg.jpg")
    # average_data = tail_data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")

print("Pushing " +trial_name+ " trial to Firebase complete")

