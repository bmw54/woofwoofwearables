from Communication.Firebase import RPi2Firebase
from BasicIMUScripts import IMUDataModule
import time

data_module = IMUDataModule()
rpi_2_firebase = RPi2Firebase()

while True:
    data = data_module.get_imu_data()
    rpi_2_firebase.send_data_to_firebase(data)
    time.sleep(2)
