import socket
import threading
import requests
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketbacklog = 50
userlist = []

def receive(sock):
	global userlist
	while True:
		msg_recv = str(sock.recv(512), "UTF-8")
		if msg_recv != '':
			for line in msg_recv:
				print(line)

def send():
	URL = 'http://dbl44.beuth-hochschule.de'
	r = requests.get(url=URL)
	data= r.json()
	print(data)

def start_server(sock):
	sock.listen(socketbacklog)


if __name__ == "__main__":
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	sock.connect(server_adr)
	#start_server(sock)
	send()
	#con, adr = sock.accept()
	threading.Thread(target=receive(sock), args=(sock,)).start()