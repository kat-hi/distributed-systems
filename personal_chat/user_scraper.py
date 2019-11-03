import string
import itertools
import socket
import threading
import sys

'''
ideas on how to get all registered users
#1 this script is highly uneffective
#2 udp? /broadcast
#3 listen like a server
#4 webscraping

'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
possible_namelist = []


#charset = str(string.ascii_lowercase)
charset = 'abcdefghijklmnoprstu'
print(charset)
def convertTuple(tup):
	str = ''.join(tup)
	return str

with open('file.txt', 'w') as file:
		names = itertools.permutations(charset,3)
		for name in names:
			stri = convertTuple(name)
			file.writelines(stri+'\r\n')
			possible_namelist.append(str)
file.close()

username = ''
userlist = []


def connect(sock):
	print('connect ...')
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
		print('connected')
	except socket.error as e:
		print("Something went wrong. Connection failed.")

def receive(sock):
	global userlist
	global username
	while True:
		response = str(sock.recv(2048), 'UTF-8')
		if response != '':
			if response[1] == 'error':
				continue
			else:
				userlist.append(username)

def test(sock):
	print('teststart')
	global username
	for user in possible_namelist:
		username = user
		text_notify = ['dslp/2.0\r\n', 'user text notify\r\n', 'anonymous\r\n',
	                   str(user) + '\r\n', '1\r\n', 'dslp/body\r\n', 'gotcha\r\n']
		for line in text_notify:
			sock.send(bytearray(line, "UTF-8"))

def printlist():
	print('start print')
	global userlist
	with open('usernames.txt', 'w') as file:
		for name in userlist:
			file.write(name)
			print(name)

if __name__ == "__main__":
	print('start')
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True)
	thread.start()
	test(sock)
	printlist()
	sock.close()
	print('socket closed')
