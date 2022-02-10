import socket
import time
import board
import adafruit_icm20x


HOST = '172.28.143.162' # Wireless IP Address of PI
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#managing error exception
try:
    s.bind((HOST, PORT))
except socket.error:
    print('Bind failed ')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()

print('Connected')

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

# awaiting for message
while True:
    message = "\n\n\n\nAcceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2 \nGyro X:%.2f, Y: %.2f, Z: %.2f rads/s \nMagnetometer X:%.2f, Y: %.2f, Z: %.2f uT\n" % (icm.acceleration + icm.gyro + icm.magnetic)
    print(message)
    time.sleep(2)

    # Sending message
    conn.send(message.encode())
conn.close() # Close connections
