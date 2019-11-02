import socket
import threading
import sys

'''
@learning: def receive(sock) stays in a sys-call: if it's interrupted and the signal handler does not raise an exception,
the method now retries the system call instead of raising an InterruptedError exception (pep475)
python raises a KeyboardInterrupt exception because of SIGINT when CTRL+c is pressed and many modules don't handle this exception.
fixing in higher-level libs takes to long time. proposal is to handle this in wrapper of stdlib
'''

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# send 'leave' to leave the chat, 'STATE NOTIFY' will change to 'STATE LEAVE'
# this is necessary to stop receive-loop
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
		if STATE == 'LEAVE':
			break
		response = str(sock.recv(1024), 'UTF-8')
		if response != '':
			response = response.split('\r\n')
			if response[0] != 'dslp/2.0\r\n' and response[1] not in message_type:
				print('unkown message type')
			elif response[1] == 'user text notify':
				print_message(response)
			elif response[1] == 'error':
				print_error(response)

'''
this method takes the number of lines of the incoming message written in the dslp-header. 
multiplied with -1 it can be used by the range()-function to print all the lines that contain the message
'''
def print_message(response):
	honeyname = response[2]
	loveletterlines = int(response[4])
	line_number = loveletterlines * (-1)
	for line in range(line_number, -1):
		print('(' + honeyname + ') ' + response[line])

def print_error(response):
	loveletterlines = int(response[4])
	num_lines = loveletterlines * (-1)
	for line in range(num_lines, -1):
		print('ERROR ' + response[line])


def user_join(sock):
	join = ['dslp/2.0\r\n', 'user join\r\n', username+'\r\n', 'dslp/body\r\n']
	print('Joining with username ' + username)
	for line in join:
		sock.send(bytearray(line, "UTF-8"))


def send_text(sock):
	global STATE
	while True:
		message = input()
		if message == 'leave':
			user_leave(sock)
			break
		if message == '':
			STATE = 'LEAVE'
			break
		try:
			receivername = message.split(':')[0]
			message = message.split(':')[1]
			text_notify = ['dslp/2.0\r\n', 'user text notify\r\n', username+'\r\n', receivername+'\r\n', '1\r\n', 'dslp/body\r\n', message+'\r\n']
			for line in text_notify:
				sock.send(bytearray(line, "UTF-8"))
		except Exception:
			print("Wrong format. Use: 'Username: Text'")


def user_leave(sock):
	leave = ['dslp/2.0\r\n', 'user leave\r\n', username+'\r\n', 'dslp/body\r\n']
	for line in leave:
		sock.send(bytearray(line, "UTF-8"))


if __name__ == "__main__":
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True)
	thread.start()
	user_join(sock)
	send_text(sock)
	user_leave(sock)
	sock.close()

