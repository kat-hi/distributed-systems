import re
import socket

''' fetching networking traffic, extracting IPs and dslp-USERNAMES since dslp is not encrypted it is possible to extract
names and ips of all users joining the dslp-server
@ note: there are different packet-contents comparing packets fetched  working at RIS and working at home..kinda messed up now
@ TODO text_notify_extractor still needs a regex for extracting sender-ip, so that remove_lost_connection() works properly '''

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
print('start sniffing...')
USERNAMES = []


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
	except socket.error:
		print("Something went wrong. Connection failed.")


def update_current_user_list():
	global USERNAMES
	print('_________________________')
	print('updated list of registered users:')
	for user in USERNAMES:
		print('-- ', user)
	print('listend')


def user_join_extractor(message):
	global USERNAMES
	try:
		# this string only appears sometimes. I don't get it...
		regex_user_ip = "User [\w][\w]* on connection (\d)*\.(\d)*\.(\d)*\.(\d)*:(\d)* joins the server."
		''' @username_from_join: extract sentence "User x on connection x joins the server" from the whole tcp-paket
		and .split() sentence based on contained whitespaces and take the second word (which is the username) '''
		username_from_join = re.search(regex_user_ip, message).group().split()[1]
		ip_from_join = re.search(regex_user_ip, message).group().split()[4].split(':')[0]  # extract ip without port

		USERNAMES.append((username_from_join, ip_from_join))
		update_current_user_list()
	except AttributeError:
		pass


def text_notify_extractor(message):
	global USERNAMES
	try:
		# "notification from jsonLover1000 to jsonLover99", "timestamp": "1572864370.3324468", "dslp-ip": "xxx.xx.xxx.xx"}]'
		regex_usernames = "Sending user text notification from [\w][\w]* to [\w][\w]*\""
		usernames_from_text_notify = re.search(regex_usernames, message).group().split(
			'"')  # ['notification from jsonLover1000 to jsonLover99', '']

		sender = usernames_from_text_notify[0].split()[5]
		receiver = usernames_from_text_notify[0].split()[7]

		USERNAMES.append((sender, 'unknown'))  # ip-regex is still missing
		update_current_user_list()

		USERNAMES.append((receiver, 'unknown'))  # ip-regex is still missing
		update_current_user_list()
	except AttributeError:
		pass


''' this method checks whether an extracted ip is already contained in USERNAMES.
USERNAMES is a list of tuples (username,ip)
this method returns either the user_tuple to be deleted or "False" if the ip is not listed '''
def is_ip_in_list(ip):
	for user_tuple in USERNAMES:
		if ip == user_tuple[1]:
			return user_tuple
	return False


''' this method is based on the check_value returned by is_ip_in_list() '''
def remove_ip_from_list(check_value):
	if not check_value:
		pass
	else:
		USERNAMES.remove(check_value)
		update_current_user_list()


def loss_due_to_connection_lost(message):
	# {"message": "Connection to xx.xx.xxx.x:xxxxx lost.", "timestamp": "1572879039.475101", "dslp-ip": "xx.xx.xxx.x"}
	try:
		regex = "(\d)*\.(\d)*\.(\d)*\.(\d)*:(\d)* lost"
		lost_ip = re.search(regex, message).group().split(':')[0]  # get rid of the port
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


def loss_due_to_resetting(message):
	# {"message":"Resetting state machine.","timestamp":"1572864370.338236","dslp-ip":"xxx.xx.xxx.xx"}]'
	try:
		regex = "Resetting (.)*(\d)*\.(\d)*\.(\d)*\.(\d)*\"}]?"
		lost_ip = re.search(regex, message).group().split("\"")[8]
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


def loss_due_to_leave(message):
	# Access-Control-Allow-Credentials: true\r\nConnection: close\r\nServer: Werkzeug/0.15.4 Python/3.7.4\r\nDate: Mon, 04 Nov201921:
	# 43:24 GMT\r\n\r\n\x00\x01\x02\x04\xff42 / websock, ["newmessage", {"message": "Line received (\'dslp/2.0\')" timestamp":
	# "1572903804.1877353", "dslp-ip": "xx.xx.xxx.xx"}]'
	try:
		regex = "Access-Control-Allow-Credentials(.)*Connection\: close(.)*(\d)*\.(\d)*\.(\d)*\.(\d)*\"}]?"
		lost_ip = re.search(regex, message).group().split("\"")[13]  # extract ip
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


''' this method is a wrapper for two methods extracting ip and username 
each method is based on a different scenario/use case based on DSLP '''
def sniff_sniff(s, message):
	# extract username and ip from 'user join' message
	user_join_extractor(message)
	# extract usernames from users already joined. (fetch infos with 'user text notify' messages)
	text_notify_extractor(message)


''' this method is a wrapper for two methods checking if an ip can be removed from username-list. 
each method is based on a different scenario/use case based on DSLP '''
def remove_lost_connection(message):
	loss_due_to_resetting(message)
	loss_due_to_connection_lost(message)
	loss_due_to_leave(message)


if __name__ == "__main__":
	connect(s)
	while True:
		msg = str(s.recvfrom(65565)[0])
		# print(msg) # ♥ watch the beauty of network traffic ♥
		sniff_sniff(s, msg)  # contains user_join_extractor() and text_notify_extractor()
		remove_lost_connection(msg)  # contains loss_due_to_resetting() and loss_due_to_connection_lost()
