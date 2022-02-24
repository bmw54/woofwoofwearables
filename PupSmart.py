from Communication.Firebase.RPi2Firebase import RPi2Firebase
from BasicIMUScripts.IMUDataModule import IMUDataModule
import time

data_module = IMUDataModule()
rpi_2_firebase = RPi2Firebase()

while True:
    data_module.poll_imu_data()
    current_data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(current_data, "CurrentIMUData")
    # average_data = data_module.get_average_imu_data()
    # rpi_2_firebase.send_data_to_firebase(average_data, "AverageIMUData")
    time.sleep(2)
