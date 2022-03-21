# - Gyro gives you angular rates (angular velocity) which you have to integrate to get angular position. This introduces drift which you need to correct using the accelerometer and magnetometer.
# - Filter the clean but drifting gyro angular position with a noisy but stable angular position built form raw acceleration and magnetometer vector using a kalman or complimentary filter. You should have stable and clean(ish) angular position. Any noise in the magnetometer or linear acceleration will appear as angular position noise.
# - Since now you know which way is up (from the stable rotation calculated above), you can remove the gravity acceleration from raw accelerometer data. Any error in the rotation will result in the gravity acceleration polluting the linear acceleration (the system will appear to accelerate in random directions)
# - Integrate linear acceleration twice. This results in massive drift due to the accumulated errors above. Depending on your algorithm, calibration method, sensor quality, local magnetic distortion, how close you are to the poles etc - you'll have a stable position for seconds or tens of seconds. For more stability you can filter this position with some absolute value coming from a GPS for example.

from time import time
import scipy.integrate


class Amplitude_Module:


    def __init__(self):
        self.ang_position = []

    def calc_angular_position(self, gyro_timeseries):
        timestamps = gyro_timeseries.keys()
        ang_velo = gyro_timeseries.values()
        self.ang_position = scipy.integrate(ang_velo, x =timestamps )
        return self.ang_position





    
    
  

      
