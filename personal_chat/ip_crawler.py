import re
import socket

'''  extracting IPs and dslp-usernames '''

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

USERNAMES = []


def connect(sock):
	server_adr = ("dbl41.beuth-hochschule.de", 80)
	print('start sniffing...')
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


def user_join_extractor(message):
	global USERNAMES
	try:
		# this string only appears sometimes in the traffic. I don't get it...
		regex = "User [\w][\w]* on connection (\d)*\.(\d)*\.(\d)*\.(\d)*:(\d)* joins the server."

		''' @username_from_join: 
		-> extract sentence "User x on connection x joins the server" from tcp-paket 
		-> .split() sentence based on contained whitespaces 
		-> take the second word (which is the username) '''
		username_from_join = re.search(regex, message).group().split()[1]
		ip_from_join = re.search(regex, message).group().split()[4].split(':')[0]  # extract ip without port
		#print(username_from_join, ip_from_join)
		USERNAMES.append((username_from_join, ip_from_join))
		update_current_user_list()
	except AttributeError:
		pass


def text_notify_extractor(message):
	global USERNAMES
	try:
		# "notification from jsonLover1000 to jsonLover99", "timestamp": "1572864370.3324468", "dslp-ip": "xxx.xx.xxx.xx"}]'
		regex = "Sending user text notification from [\w][\w]* to [\w][\w]*\""
		usernames_from_text_notify = re.search(regex, message).group().split('"')  # ['notification from jsonLover1000 to jsonLover99', '']

		sender = usernames_from_text_notify[0].split()[5]
		receiver = usernames_from_text_notify[0].split()[7]
		print('Someone that\'s sending: " + sender')
		print('Someone that\'s receiving: " + receiver')
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
	global USERNAMES
	for user_tuple in USERNAMES:
		if ip == user_tuple[1]:
			return user_tuple
	return False


''' this method is based on the check_value returned by is_ip_in_list() '''
def remove_ip_from_list(check_value):
	global USERNAMES
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
		print('lost ip: lost ', lost_ip)
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


def loss_due_to_resetting(message):
	# {"message":"Resetting state machine.","timestamp":"1572864370.338236","dslp-ip":"xxx.xx.xxx.xx"}]'
	try:
		regex = "Resetting (.)*(\d)*\.(\d)*\.(\d)*\.(\d)*\"}]?"
		lost_ip = re.search(regex, message).group().split("\"")[8]
		print('lost ip: reset ', lost_ip)
		#remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


def loss_due_to_leave(message):
	# Access-Control-Allow-Credentials: true\r\nConnection: close\r\nServer: Werkzeug/0.15.4 Python/3.7.4\r\nDate: Mon, 04 Nov201921:
	# 43:24 GMT\r\n\r\n\x00\x01\x02\x04\xff42 / websock, ["newmessage", {"message": "Line received (\'dslp/2.0\')" timestamp":
	# "1572903804.1877353", "dslp-ip": "xx.xx.xxx.xx"}]'
	try:
		regex = "Access-Control-Allow-Credentials(.)*Connection\: close(.)*(\d)*\.(\d)*\.(\d)*\.(\d)*\"}]?"
		lost_ip = re.search(regex, message).group().split("\"")[13]  # extract ip
		print('lost ip: leave ', lost_ip)
		#remove_ip_from_list(is_ip_in_list(lost_ip))
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
	#loss_due_to_resetting(message)
	loss_due_to_connection_lost(message)
	# loss_due_to_leave(message)


if __name__ == "__main__":
	connect(s)
	while True:
		msg = s.recvfrom(65565)[0]
		print(msg) # ♥ watch the beauty of network traffic ♥
		sniff_sniff(s, msg)  # contains user_join_extractor() and text_notify_extractor()
		remove_lost_connection(msg)  # contains loss_due_to_resetting(), loss_due_to_connection_lost(), loss_due_to_leave()
