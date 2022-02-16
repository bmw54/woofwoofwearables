import time
import board
import adafruit_icm20x
import numpy as np

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

starttime = time.time()
measPeriod = 4 # average measurements over 4 seconds
avgAcc = 0.0
numMeas = 0.0
while True:
    newAcc = icm.acceleration
    newAccMag = np.linalg.norm(newAcc)
    avgAcc = (avgAcc * numMeas + newAccMag)/(numMeas + 1)
    numMeas+=1

    currenttime = time.time()
    if currenttime >= (starttime + measPeriod):
        starttime = currenttime
        print("\n\nAverage Acceleration: ", avgAcc)
        avgAcc = 0
        numMeas = 0
    
