import socket
import threading
import sys

'''
@learning1: def receive(sock) stays in a sys-call: if it's interrupted and the signal handler does not raise an exception,
the method now retries the system call instead of raising an InterruptedError exception (pep475) but many modules don't 
handle this exception. fixing this in higher-level libs takes to long time. proposal is to handle this in wrapper of stdlib
long story short: that's why in python there is no exception handling needed with ending this recv-syscall
'''

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

''' 
send 'leave' to leave the chat and'STATE NOTIFY' will change to 'STATE LEAVE'
this is necessary to stop receive-loop that's kinda daemon - for real, with respect to @learning1
'''
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
		if check_STATE():
			response = str(sock.recv(2048), 'UTF-8')
			if response != '':
				response = response.split('\r\n')
				if response[0] != 'dslp/2.0\r\n' and response[1] not in message_type:
					print('unkown message type')
				elif response[1] == 'user text notify':
					print_message(response)
				elif response[1] == 'error':
					print_error(response)
		else:
			break


'''
this method takes the number of lines of the incoming message written in the dslp-header. 
multiplied with -1 it can be used by the range()-function to print all the lines that contain the message
[ but it does not work and I could not figure it out why.. so it's now a static line-reading solution ]
'''

def print_message(response):
	print('(' + response[2] + ')' + response[6])
	'''loveletterlines = int(response[4]) * (-1)
	for line in range(loveletterlines, -0):
		print(response[line])
	'''

def print_error(response):
	print('ERROR: ' + response[4])
	'''
	loveletterlines = int(response[2]) * (-1)
	for line in range(loveletterlines, -0):
		print('ERROR ', str(response[line]))
	'''

def user_join(sock):
	join = ['dslp/2.0\r\n', 'user join\r\n', username + '\r\n', 'dslp/body\r\n']
	print('Joining with username ' + username)
	for line in join:
		sock.send(bytearray(line, "UTF-8"))

'''
this method checks and sends input. 
first: there is a check for keywords, that would end the session.
second: the required input (with respect to our task it has to be 'receivername: textmessage') is split into name and message
'''
def send_text(sock):
	while True:
		message = input()
		if check_ending_keywords(message):
			receivername = message.split(':')[0]
			if receivername.__contains__('dslp/2.0'):
				print("invalid name")
				continue
			else:
				message = message.split(':')[1]
				text_notify = ['dslp/2.0\r\n', 'user text notify\r\n', username + '\r\n',
				               receivername + '\r\n', '1\r\n', 'dslp/body\r\n', message + '\r\n']
				for line in text_notify:
					sock.send(bytearray(line, "UTF-8"))
		else:
			break


def check_ending_keywords(message):
	global STATE
	if message == 'leave':
		STATE = 'LEAVE'
		user_leave(sock)
		return False
	elif message == '':
		STATE = 'LEAVE'
		return False
	else:
		return True


def user_leave(sock):
	leave = ['dslp/2.0\r\n', 'user leave\r\n', username + '\r\n', 'dslp/body\r\n']
	for line in leave:
		sock.send(bytearray(line, "UTF-8"))


def check_STATE():
	global STATE
	if STATE == "NOTIFY":
		return True
	else:
		return False


if __name__ == "__main__":
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True)
	thread.start()
	user_join(sock)
	send_text(sock)
	user_leave(sock)
	sock.close()
