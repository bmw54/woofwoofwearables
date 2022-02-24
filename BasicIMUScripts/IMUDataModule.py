import board
import adafruit_icm20x
import numpy as np

class IMUDataModule:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.icm = adafruit_icm20x.ICM20948(i2c)
        self.acceleration = (0.0, 0.0,0.0)
        self.gyro = (0.0, 0.0,0.0)
        self.magnetic = (0.0, 0.0,0.0)
        self.angle = (0.0, 0.0,0.0)
        self.average_acceleration = (0.0, 0.0,0.0)
        self.average_gyro = (0.0, 0.0,0.0)
        self.average_magnetic = (0.0, 0.0,0.0)
        self.average_angle = (0.0, 0.0,0.0)
        self.length = 0

    def poll_imu_data(self):
        (x,y,z) = self.icm.magnetic
        (x,y,z) = (max(x, 0.001), max(y, 0.001), max(z, 0.001))
        angle = (np.arctan(z/y), np.arctan(x/z), np.arctan(y/x))  
        acceleration = self.icm.acceleration
        gyro = self.icm.gyro
        magnetic = self.icm.magnetic

        total_acceleration =  tuple(map(sum,zip(acceleration, self.average_acceleration * self.length)))
        self.average_acceleration = tuple(val/self.length + 1 for val in total_acceleration)

        total_gyro =  tuple(map(sum,zip(gyro, self.average_gyro * self.length)))
        self.average_gyro = tuple(val/self.length + 1 for val in total_gyro)

        total_magnetic =  tuple(map(sum,zip(magnetic, self.average_magnetic * self.length)))
        self.average_magnetic = tuple(val/self.length + 1 for val in total_magnetic)

        total_angle =  tuple(map(sum,zip(angle, self.average_angle * self.length)))
        self.average_angle = tuple(val/self.length + 1 for val in total_angle)

        self.length += 1

        self.acceleration = acceleration
        self.gyro = gyro
        self.magnetic = magnetic
        self.angle = angle
        

    def get_imu_data(self):
        self.poll_imu_data()
        return [self.acceleration, self.gyro, self.magnetic, self.angle]
    
    def get_average_imu_data(self):
        self.poll_imu_data()
        return [self.average_acceleration, self.average_gyro, self.average_magnetic, self.average_magnetic, self.length]
     


    
    
  

      
