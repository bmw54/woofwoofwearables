import board
import adafruit_icm20x
import numpy as np

class IMUDataModule:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.icm = adafruit_icm20x.ICM20948(i2c)

    def get_imu_data(self):
        (x,y,z) = self.icm.magnetic
        (x,y,z) = (max(x, 0.001), max(y, 0.001), max(z, 0.001))
        angle = (np.arctan(z/y), np.arctan(x/z), np.arctan(y/x))  
        return [self.icm.acceleration, self.icm.gyro, self.icm.magnetic, angle]

  

      
