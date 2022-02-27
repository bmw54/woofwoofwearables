"""
Tutorial: Send Data to Firebase Using Raspberry Pi
Hardware:
– Raspberry Pi 3 Model B
References:
– https://circuitpython.readthedocs.io/projects/mlx90614/en/latest/
– https://github.com/thisbejim/Pyrebase
"""

import time
import board
import busio as io
import adafruit_icm20x
import pyrebase


i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

config = {
  "apiKey": "M3daySH0pEM5DcBgLbw8LVYJakBh2M8anFkDXq0I",
  "authDomain": "woof-woof-wearables.firebaseapp.com",
  "databaseURL": "https://woof-woof-wearables-default-rtdb.firebaseio.com",
  "storageBucket": "woof-woof-wearables.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print("Send Data to Firebase Using Raspberry Pi")
print("—————————————-")
print()

while True:
  

  data = {
    "Acceleration": icm.acceleration,
    "Gyro": icm.gyro, 
    "Magnetometer": icm.magnetic,
  }
  db.child("icm20x").child("1-set").set(data)
  db.child("icm20x").child("2-push").push(data)

  time.sleep(2)