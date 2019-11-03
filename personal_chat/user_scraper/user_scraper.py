import string
import itertools
import socket
import threading
import sys
import mmap
'''
ideas on how to get all registered users
#1 this script: it is highly uneffective! process is always killed. WIP: trying memory mapped files
#2 udp/connectionless recv: but how do I get dslp-responses containing the usernames?
#3 listen like a server... but cannot bind to the same address... / port forwarding.. (sshtunnel.py)
#4 fetch user names from server-log (webscraping.py)
#5 serverlog: "Performing group membership cleanup ... " maybe fetching users via "group membership"?

'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#charset = str(string.ascii_letters)
#charset = str(string.ascii_lowercase)
charset = 'abcdefghijklmnoprstu'

username = ''
userlist = []

wordlength = sys.argv[1]


def get_permutations(wordlength):
	def convertTuple(tup):
		str = ''.join(tup)
		return str

	# run this with wordlength 3-7 if possible, so you get all char combinations with wordlength 3-7
	with open('file.txt', 'r') as file:
		with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE) as buffer:
			names = itertools.permutations(charset,wordlength)
			for name in names:
				stri = convertTuple(name)
				buffer.writelines(stri+'\r\n')
			buffer.close()
			file.close()


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
	global username
	with open("file.txt", "r") as file:
		with mmap.mmap(file.fileno(), 0) as buffer:
			for user in buffer:
				username = user
				text_notify = ['dslp/2.0\r\n', 'user text notify\r\n', 'anonymous\r\n',
			                   str(user) + '\r\n', '1\r\n', 'dslp/body\r\n', 'gotcha\r\n']
				for line in text_notify:
					sock.send(bytearray(line, "UTF-8"))

def printlist():
	global userlist
	with open('usernames.txt', 'w') as file:
		with mmap.mmap(file.fileno(), 0) as buffer:
			for name in userlist:
				file.write(name)
				print(name)

if __name__ == "__main__":
	get_permutations(wordlength) # write all possible combinations in file.txt
	connect(sock)
	thread = threading.Thread(target=receive, args=(sock,), daemon=True) # checks if received message is an error message
	# if not -> user exists and userlist.append(user)
	thread.start()
	test(sock)
	printlist()
	sock.close()
	print('socket closed')
