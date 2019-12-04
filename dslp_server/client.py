import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(sock):
	server_adr = ("127.0.0.1", 8000)
	try:
		sock.connect(server_adr)
		print('connected')
	except socket.error as e:
		print("Something went wrong. Connection failed.")


def send(sock):
	while True:
		message = input()
		sock.send(bytearray(message, "UTF-8"))


if __name__ == "__main__":
	connect(sock)
	send(sock)