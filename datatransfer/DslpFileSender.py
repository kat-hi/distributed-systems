import socket
import sys
import mimetypes

USERNAME = sys.argv[1]
RECEIVER = sys.argv[2]
FILE = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send_file(sock):
	mime = mimetypes.guess_type(FILE)[0]
	with open(FILE, 'rb') as file:
		bytes = str(file.read())
		size = len(bytes)
		dslp_file = ['dslp/2.0\r\n', 'user file notify\r\n', USERNAME + '\r\n', RECEIVER + '\r\n',
		             FILE + '\r\n', mime + '\r\n', str(size) + '\r\n', 'dslp/body\r\n', bytes]
		line_counter = 0
		for line in dslp_file:
			sock.sendall(bytearray(line, "UTF-8"))
			line_counter += 1


def user_join(sock):
	join = ['dslp/2.0\r\n', 'user join\r\n', USERNAME + '\r\n', 'dslp/body\r\n']
	print('Joining with username ' + USERNAME)
	for line in join:
		sock.send(bytearray(line, "UTF-8"))


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 44444)
	try:
		sock.connect(server_adr)
	except socket.error as e:
		print("Something went wrong. Connection failed.")


if __name__ == "__main__":
	connect(sock)
	user_join(sock)
	send_file(sock)
