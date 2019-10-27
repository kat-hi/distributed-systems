import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

message_type = ['request time', 'response time', 'group join', 'group leave',
                'group notify', 'user join', 'user leave', 'user text notify',
                'user file notify', 'error']


def receive(sock):
	while True:
		response = str(sock.recv(512), 'UTF-8')
		if response != '':
			response = response.split('\r\n')
			if response[1] == 'error':
				check_error(response)
			elif response[1] == 'group notify':
				print(response)
			return response


def group_join(sock):
	join_group = ['dslp/2.0\r\n', 'group join\r\n', 'Übung\r\n', 'dslp/body\r\n']
	try:
		for line in join_group:
			sock.send(bytearray(line, "UTF-8"))
	except socket.error as e:
		print(e)


def group_notify(sock):
	static_message = "<p style='height=400px;color:red'>\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 </p>\r\n"
	notify_group = ['dslp/2.0\r\n', 'group notify\r\n', 'Übung\r\n', '1\r\n', 'dslp/body\r\n', static_message]
	try:
		for line in notify_group:
			sock.send(bytearray(line, 'UTF-8'))
	except socket.error as e:
		print("Sorry this message cannot be send")


def group_leave(sock):
	leave_group = ['dslp/2.0\r\n', 'group leave\r\n', 'Übung\r\n', 'dslp/body\r\n']
	if input() != '':
		try:
			for line in leave_group:
				sock.send(bytearray(line, 'UTF-8'))
		except socket.error as e:
			print("leaving group was not successful")


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
	except socket.error as e:
		print("Something went wrong. Connection failed.")

def check_error(response):
	if response[1] == 'error':
		lines = response[2]
		for line in range(-lines,-1):
			print(line)
		return False
	else:
		return True


if __name__ == "__main__":
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,))
	response = thread.start()
	group_join(sock)
	group_notify(sock)
	group_leave(sock)
