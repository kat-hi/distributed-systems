import socket
import threading
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# send 'end' to leave the chat, 'STATE NOTIFY' will change to 'STATE LEAVE'
STATE = 'NOTIFY'
message_type = ['request time', 'response time', 'group join', 'group leave',
                'group notify', 'user join', 'user leave', 'user text notify',
                'user file notify', 'error']


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
	except socket.error as e:
		print("Something went wrong. Connection failed.")


def receive(sock):
	while True:
		if STATE == 'LEAVE':
			break
		response = str(sock.recv(512), 'UTF-8')
		if response != '':
			response = response.split('\r\n')
			if response[0] != 'dslp/2.0' and response[1] not in message_type:
				print('unkown message type')
			elif response[1] == 'user text notify':
				print_message(response)
			elif response[1] == 'error':
				print_error(response)


def print_message(response):
	num_lines = int(response[3]) * (-1)
	for line in range(num_lines, -1):
		print('(' + response[2] + ') ' + response[line])


def print_error(response):
	if response[1] == 'error':
		num_lines = int(response[3]) *(-1)
		for line in range(num_lines,-1):
			print(response[line])
		return False
	else:
		return True


def user_join(sock):
	join = ['dslp/2.0', 'user join', str(sys.argv[1]), 'dslp/body']
	for line in join:
		sock.send(bytearray(line, "UTF-8"))


def send_text(sock):
	global STATE
	while True:
		message = input()
		if message == '':
			STATE = 'LEAVE'
			break

		sock.send(bytearray(message, "UTF-8"))

def user_text_notify():
	text_notify = ['dslp/2.0', 'user', 'text notify', 'Heinz', 'Gregor', '2', 'dslp/body']


def user_leave(sock):
	leave = ['dslp/2.0', 'user leave', 'Heinz', 'dslp/body']
	for line in leave:
		sock.send(bytearray(line, "UTF-8"))


if __name__ == "__main__":
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True)
	thread.start()
	user_join(sock)
	send_text(sock)
	user_leave(sock)
	thread.join()
	sock.close()