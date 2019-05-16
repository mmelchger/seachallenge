import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.4.1', 9000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Look for the response
    amount_received = 0
    nMessages = 10000;

    while amount_received < nMessages:
        data = sock.recv(1000)
        amount_received += 1
        print(data)

finally:
    print('closing socket')
    sock.close()