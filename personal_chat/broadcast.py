import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('dbl44.beuth-hochschule.de', 21)
message = 'This is the message.  It will be repeated.'

try:
    # Send data
    sent = sock.sendto(b"test", server_address)
    # Receive response
    data, server = sock.recvfrom(4096)
    print(data,server)
finally:
    sock.close()