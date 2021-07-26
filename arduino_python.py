#program to check if the data of sensors can be made available in python
#library for communicating with arduino
import serial
#establishing connection with the serial port which in this case is "/dev/ttyACM0"
try:
    arduino = serial.Serial("/dev/ttyACM0", timeout=1 ,baudrate=9600)
except:
    print("Please check the port")

for i in range(20):
    #arduino data is being received in data variable as bytes 
    data=arduino.readline()
    #converting bytes into string
    data=data.decode()
    if data:
        print(data)
