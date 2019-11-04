# getting closer
import socket
import threading
import requests
import sshtunnel
from getpass import getpass

ssh_host = 'compute.beuth-hochschule.de'
ssh_port = 3333
ssh_user = 's77518'

REMOTE_HOST = 'dbl44.beuth-hochschule.de'
REMOTE_PORT = 21

from sshtunnel import SSHTunnelForwarder
ssh_password = getpass('Enter YOUR_SSH_PASSWORD: ')
print('start connecting')

server = SSHTunnelForwarder(
    ssh_address=(ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=(REMOTE_HOST, REMOTE_PORT))

server.start()
print('started')
print('Connect the remote service via local port: %s'  %server.local_bind_port)
print(server.local_bind_port)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting user user request.\n")
    server.stop()
