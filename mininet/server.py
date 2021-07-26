#server program to receive data from one mininet host to the other
import socket

HOST = '10.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

#creating socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    #establishing connection
    conn, addr = s.accept()
    with conn:
        for i in range(10):
            #receiving data from client
            data = conn.recv(1024)
            #converting data from byte to string
            data = data.decode()
            if data:
                print('Received', data)
