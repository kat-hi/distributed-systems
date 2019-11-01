import socket
import threading
import sys
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# send 'end' to leave the chat, 'STATE NOTIFY' will change to 'STATE LEAVE'
STATE = 'NOTIFY'
message_type = ['request time', 'response time', 'group join', 'group leave',
                'group notify', 'user join', 'user leave', 'user text notify',
                'user file notify', 'error']
username = sys.argv[1]

def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
	except socket.error as e:
		print("Something went wrong. Connection failed.")


def receive(sock):
	while True:
		print('inside receive')
		print(STATE)
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
	print('inside send_text')
	print(response[6])

	'''
	num_lines = int(response[3]) * (-1)
	for line in range(num_lines, -1):
		print('(' + response[2] + ') ' + response[line])
	'''

def print_error(response):
	print(response[4])
	'''
	num_lines = int(response[3]) *(-1)
	for line in range(num_lines,-1):
		print(response[line])
	'''

def user_join(sock):
	join = ['dslp/2.0', 'user join', username, 'dslp/body']
	print('Joining with username ' + username)
	for line in join:
		sock.send(bytearray(line, "UTF-8"))


def send_text(sock):
	print('inside send_text')
	global STATE
	while True:
		message = input()
		if message == '':
			STATE = 'LEAVE'
			break
		else:
			receivername = message.split(':')[0]
			message = message.split(':')[1]
		text_notify = ['dslp/2.0', 'user', 'text notify', username, receivername, '1', 'dslp/body', message]
		for line in text_notify:
			sock.send(bytearray(line, "UTF-8"))


def user_leave(sock):
	print('inside user_leave')
	leave = ['dslp/2.0', 'user leave', username, 'dslp/body']
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
