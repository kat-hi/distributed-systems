import socket
import threading
import sys
import mimetypes

USERNAME = sys.argv[1]
# bytes() method returns a immutable bytes object initialized with the given size and data.
# bytearray() is the mutable version of this

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

message_type = ['request time', 'response time', 'group join', 'group leave',
                'group notify', 'user join', 'user leave', 'user text notify',
                'user file notify', 'error']


def receive(sock):
	response = str(sock.recv(64000), 'UTF-8')
	response = response.split('\r\n')
	if response[0] != 'dslp/2.0':
		print('Unexpected type of message')
	elif response[1] == 'error':
		print('something went wrong.')
	elif response[1] != 'user file notify':
		print('Unexpected type of message: notify')
	elif response[1] not in message_type:
		print('Unknown type of message')
	else:
		FILE = response[4]
		MIMETYPE = response[5]
		DATA = response[8]
		if MIMETYPE == "text/plain":
			with open(FILE, 'w', encoding="utf-8") as file:
				file.write(DATA)
			file.close()
		elif MIMETYPE == "image/jpeg" or MIMETYPE == "image/png":
			with open(FILE, 'wb') as file:
				DATA = bytes(DATA, 'UTF-8')
				for data in DATA:
					file.write(bytes(data))
			file.close()
		elif MIMETYPE == "application/pdf":
			with open(FILE, 'wb') as file:
				DATA = bytes(DATA, 'UTF-8')
				for data in DATA:
					file.write(bytes(data))
			file.close()
		else:
			print("Unknown MIME-Type: " + MIMETYPE)
	return


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 44444)
	try:
		sock.connect(server_adr)
	except socket.error as e:
		print("Something went wrong. Connection failed.")


def user_join(sock):
	join = ['dslp/2.0\r\n', 'user join\r\n', USERNAME + '\r\n', 'dslp/body\r\n']
	print('Joining with username ' + USERNAME)
	for line in join:
		sock.send(bytearray(line, "UTF-8"))


if __name__ == "__main__":
	connect(sock)
	user_join(sock)
	receive(sock)
