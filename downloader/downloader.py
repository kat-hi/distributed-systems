import socket
import sys
import requests
import re

URI = sys.argv[1]
PORT = 80
PROTOCOL = URI.split('://')[0]
DNS = (URI.split('//')[1]).split('/', 1)[0]
RESSOURCE = (URI.split('//')[1]).split('/', 1)[1]
FILETYPE = (URI.split('//')[1]).split('.', 2)[2]

server_adr = (DNS, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def it_could_have_been_so_simple():
	r = requests.get(URI, allow_redirects=True)
	open('media.' + FILETYPE, 'wb').write(r.content)

def check_tls():
	if PROTOCOL == 'https':
		print('It won\'t work. TLS or SSL is used')
		return False
	return True

def connect():
	try:
		sock.connect(server_adr)
		print('Connection established')
	except socket.error:
		print("Something went wrong. Connection failed")


def send_request():
	request = "GET /%s HTTP/1.1\r\nHost: %s\r\nAccept:  */*\r\n\r\n" % (RESSOURCE, DNS)
	sock.send(request.encode())


def receive():
	content = b''
	while True:
		response = sock.recv(64000)
		if not response:
			break
		content = content + response
	return content


def content_length_extractor(content):
	regex_content_length = 'Content-Length: [\d]*'
	content_length = int(re.search(regex_content_length, str(content)).group().split(' ')[1]) * (-1)
	return content_length


# etag is used to define the filename in save_file()
def etag_extractor(content):
	regex_etag = 'ETag: \"((\w)*(-)*)*\"'
	etag = re.search(regex_etag, str(content)).group().split("\"")
	etag = etag[1] + "." # preparation for save_file() when etag and filetype will be concatenated to a new filename
	return etag


def save_file(etag, content_length, content):
	content = content[content_length:-1]
	open(etag + FILETYPE, 'wb').write(content)


if __name__ == '__main__':
	# it_could_have_been_so_simple()
	if check_tls():
		connect()
		send_request()
		content = receive()
		content_length = content_length_extractor(content)
		etag = etag_extractor(content)
		save_file(etag, content_length, content)
