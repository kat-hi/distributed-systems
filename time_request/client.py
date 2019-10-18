import socket
from datetime import datetime
import re

# using measure_process_time() requires the following packages:
# from time import process_time
# from numpy import *

server_adr = ("dbl44.beuth-hochschule.de", 21)

'''
@learning: TCP_NODELAY disables nagle's algorithm and ensures data is written immediately. 
note: This increases overhead in all packets but since this client-server example does not require much throughput it's okay, 
it works anyway since in python there is no need to flush. 
There wasn't any significant difference in process time between enabled and disabled algorithm using this small kind of data
'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

header = ['dslp/2.0\r\n', 'request time\r\n', 'dslp/body\r\n']

message_type = ['request time', 'response time', 'group join', 'group leave',
                'group notify', 'user join', 'user leave', 'user text notify',
                'user file notify', 'error']


def check_dslp_header(response):
	'''
	@ response: list of strings. each string is one line of the server's response
	@ check_message_type: to pass the dslp-header-check "check_message_type" is expected to be 1. It returns 1 if
		the response message type fits to an acceptable type in message_type list.
	@ response[0] and response[2]: the first and third line in the header which are simply compared to the string
		expected from DSLP
	'''
	check_message_type = 0
	if response[0] != 'dslp/2.0':
		return False
	for type in message_type:
		if response[1] == type:
			check_message_type += 1
	if check_message_type == 0:
		return False
	if response[2] != 'dslp/body':
		return False
	return True


def catch_error_message(response):
	# @response: list of strings. each string is one line of the server's response
	if response[0] != 'dslp/2.0\r\n':
		return False
	if response[1] != 'error\r\n':
		return False
	if response[2] != 'dslp/body\r\n':
		return False
	# extract text lines from the third line of the server-response-message for enclosing the range of the error message
	range_end = int(response[2]) + 3
	for line in range(4, range_end + 1):
		print(response[line])
	return True


def send_header(header):
	for message in header:
		sock.send(bytearray(message, "UTF-8"))


def receive():
	response = str(sock.recv(1024), 'UTF-8')
	response = response.split('\r\n')
	if check_dslp_header(response):
		# 2019-10-18T15:31:56+00:00
		server_date = response[3].split('T')[0]  # '2019-10-18'
		server_time = response[3].split('T')[1].split('+')[0]  # '15:31:56'
		server_timezone = re.search('\+\d\d:\d\d', response[3]).group() # not used
		sever_date_time = server_date + ' ' + server_time
		sever_date_time = datetime.strptime(sever_date_time, '%Y-%m-%d %H:%M:%S')
		print('Current time on the server:', datetime.strftime(sever_date_time, '%c CEST'))
	elif catch_error_message(response) != True:
		print('processing dslp failed.')


def get_server_infos():
	peer = sock.getpeername()
	print("Connection established:", socket.getfqdn(str(peer[0])) + '/' + str(peer[0]) + ":" + str(peer[1]))


'''
this function writes a txt-file with a list of process times, the mean value of time and standard deviation
it can be used to compare different socket configurations such as SOCK_STREAM, NODELAY ..etc..
note: actually the data that is used for this socket-connection is not suitable for getting considerable results. 
better test with large streaming data
'''
'''
def measure_process_time():
	t = 0
	requests = 500
	stats_values = []
	with open('process-time-checklist.txt', 'w') as ptc:
		for i in range(1, requests):
			start = process_time()
			send_header(header)
			receive()
			end = process_time()
			diff = end - start
			ptc.write(str(diff) + 's\n')
			t = t + diff
			stats_values.append(diff)
		ptc.write('t mean = ' + str(t/requests) + 's\n')
		ptc.write('t stddev = ' + str(array(stats_values).std()) + 's')
		ptc.close()
'''

if __name__ == "__main__":
	sock.connect(server_adr)
	get_server_infos()
	# measure_process_time() # uncomment sendHeader(header) and receive() and run measure_process_time() instead
	send_header(header)
	receive()
	sock.close()
