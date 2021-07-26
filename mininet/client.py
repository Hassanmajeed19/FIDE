#client program to send data from one mininet host to the other
import serial
import socket

HOST = '10.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
count=0

#establishing connection with the serial port which in this case is "/dev/ttyACM0"
try:
    arduino = serial.Serial("/dev/ttyACM0",timeout=1,baudrate=9600)
except:
    print('Please check the port')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while count<10:
        #arduino data is being received in data variable as bytes which is then sent to server
        s.sendall(arduino.readline())
        count +=1
