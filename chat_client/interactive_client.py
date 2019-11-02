import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# send 'end' to leave the chat, 'STATE NOTIFY' will change to 'STATE LEAVE'
STATE = 'NOTIFY'


def receive(sock):
	while True:
		if STATE == 'LEAVE':
			return
		response = str(sock.recv(512), 'UTF-8')
		if response != '':
			response = response.split('\r\n')
			if response[1] == 'error':
				print_error(response)
			elif response[1] == 'group notify':
				print(response[-2])


def group_join(sock):
	join_group = ['dslp/2.0\r\n', 'group join\r\n', 'Übung\r\n', 'dslp/body\r\n']
	try:
		for line in join_group:
			sock.send(bytearray(line, "UTF-8"))
	except socket.error as e:
		print(e)


def group_notify(sock):
	global STATE
	if STATE == 'LEAVE':
		return
	message = input()
	if message == 'end':
		STATE = 'LEAVE'
	notify_group = ['dslp/2.0\r\n', 'group notify\r\n', 'Übung\r\n', '1\r\n', 'dslp/body\r\n', message+'\r\n']
	try:
		for line in notify_group:
			sock.send(bytearray(line, 'UTF-8'))
	except socket.error as e:
		print("Sorry this message cannot be send")


def group_leave(sock):
	leave_group = ['dslp/2.0\r\n', 'group leave\r\n', 'Übung\r\n', 'dslp/body\r\n']
	if STATE == 'LEAVE':
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


def print_error(response):
	if response[1] == 'error':
		num_lines = int(response[3]) *(-1)
		for line in range(num_lines,-1):
			print(response[line])
		return False
	else:
		return True


if __name__ == "__main__":
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True)
	thread.start()
	group_join(sock)
	while True:
		if STATE == 'LEAVE':
			break
		group_notify(sock)
		print(STATE)
	group_leave(sock)
	sock.close()

