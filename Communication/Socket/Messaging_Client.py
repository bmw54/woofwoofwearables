import socket

HOST = '172.28.143.162' # Wireless IP Address of PI
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#Lets loop awaiting for your input
while True:
	command = input('Enter your command: ')
	s.send(command.encode())
	reply = s.recv(1024).decode()
	if reply == 'Terminate':
		break
	print(reply)
