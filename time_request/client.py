import socket
import pandas as panda

server_adr = ("dbl44.beuth-hochschule.de", 21)
sock = socket.socket(socket.AF_INET, socket.TCP_NODELAY)

header = ['dslp/2.0\r\n', 'request time\r\n', 'dslp/body\r\n']

message_type = ['request time\n', 'response time\n', 'group join\n', 'group leave\n',
                'group notify\n', 'user join\n', 'user leave\n', 'user text notify\n',
                'user file notify\n', 'error\n']


def check_dslp_header(response):
	'''
		@ response: list of strings. each string is one line of the server's response
		@ check_message_type: to pass the dslp-header-check "check_message_type" is expected to be 1. It returns 1 if
			the response message type fits to an acceptable type in message_type list.
		@ response[0] and response[2]: the first and third line in the header which are simply compared to the string
			expected from DSLP
	'''
	check_message_type = 0
	if response[0] != 'dslp/2.0\n':
		return False
	for type in message_type:
		if response[1] == type:
			check_message_type += 1
	if check_message_type == 0:
		return False
	if response[2] != 'dslp/body\n':
		return False
	return True


def catch_error_message(response):
	# @response: list of strings. each string is one line of the server's response
	if response[0] != 'dslp/2.0\n':
		return False
	if response[1] != 'error\n':
		return False
	if response[2] != 'dslp/body\n':
		return False
	# extract text lines from the third line of the server-response-message for enclosing the range of the error message
	range_end = int(response[2]) + 3
	for line in range(4, range_end+1):
		print(response[line])
	return True


def sendHeader(header):
	for message in header:
		sock.send(bytearray(message, "UTF-8"))


def receive():
	response_file = sock.makefile()
	response = response_file.readlines(50)
	response_file.close()
	if check_dslp_header(response):
		parse = panda.Timestamp(response[3])
		print("Current time on the server:", parse.day_name(), parse.month_name(), parse.time(), "CEST", parse.year)
	elif catch_error_message(response):
		pass


def get_server_infos():
	peer = sock.getpeername()
	print("Connection established:", socket.getfqdn(str(peer[0])) + '/' + str(peer[0]) + ":" + str(peer[1]))


if __name__ == "__main__":
	sock.connect(server_adr)
	get_server_infos()
	sendHeader(header)
	receive()
