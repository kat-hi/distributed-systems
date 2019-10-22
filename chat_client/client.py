import socket

server_adr = ("dbl44.beuth-hochschule.de", 21)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_adr)

if __name__ == "__main__":
	print("Hello")