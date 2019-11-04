import re
import socket

'''
fetching networking traffic, extracting IPs and dslp-USERNAMES
since dslp is not encrypted it is possible to extract names and ips of all users joining the dslp-server
'''
''' 
@TODO text_notify_extractor still needs a regex for extracting sender-ip, so that remove_lost_connection() works properly
'''

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
	print('new list:')
	for user in USERNAMES:
		print('-- ', user)

def user_join_extractor(message):
	global USERNAMES
	try:
		regex_user_ip = "User [\w][\w]* on connection (\d)*\.(\d)*\.(\d)*\.(\d)*:(\d)* joins the server."
		username_from_join = re.search(regex_user_ip, message).group().split()[1]
		ip_from_join = re.search(regex_user_ip, message).group().split()[4].split(':')[0]  # extract ip without port

		if username_from_join not in USERNAMES:
			USERNAMES.append((username_from_join, ip_from_join))
			print('From join_extractor: ' + username_from_join + ' | ' + ip_from_join)
			update_current_user_list()
	except AttributeError:
		pass


def text_notify_extractor(message):
	global USERNAMES
	try:
		# "Sending user text notification from jsonLover1000 to jsonLover99", "timestamp": "1572864370.3324468", "dslp-ip": "xxx.xx.xxx.xx"}]'
		regex_USERNAMES = "Sending user text notification from [\w][\w]* to [\w][\w]*\""
		USERNAMES_from_text_notify = re.search(regex_USERNAMES, message).group().split('"')
		sender = USERNAMES_from_text_notify[0].split()[5]
		receiver = USERNAMES_from_text_notify[0].split()[7]

		if sender not in USERNAMES:
			USERNAMES.append((sender,))
			# print('From notify_extractor: ' + sender)
			update_current_user_list()
		if receiver not in USERNAMES:
			USERNAMES.append((receiver,))
			# print('From notify_extractor: ' + receiver)
			update_current_user_list()
	except AttributeError:
		pass

'''
this method checks whether an extracted ip is already contained in USERNAMES.
USERNAMES is a list of tuples (username,ip)
this method returns either the user_tuple to be deleted or "False" if the ip is not listed
'''
def is_ip_in_list(ip):
	for user_tuple in USERNAMES:
		if ip == user_tuple[1]:
			return user_tuple
	return False

'''
this method is based on the check_value returned by is_ip_in_list()
'''
def remove_ip_from_list(check_value):
	if not check_value:
		pass
	else:
		USERNAMES.remove(check_value)
		update_current_user_list()


def loss_due_to_resetting(message):
	try:
		connection_lost_regex = "(\d)*\.(\d)*\.(\d)*\.(\d)*:(\d)* lost"
		lost_ip = re.search(connection_lost_regex, message).group().split(':')[0]
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


def loss_due_to_connection_lost(message):
	try:
		reset_regex = "Resetting (.)*(\d)*\.(\d)*\.(\d)*\.(\d)*\"}]?"
		lost_ip = re.search(reset_regex, message).group().split("\"")[8]
		remove_ip_from_list(is_ip_in_list(lost_ip))
	except AttributeError:
		pass


'''
this method is a wrapper for two uses cases ex
'''

def sniff_sniff(s, message):
	# extract username and ip from 'user join' message
	user_join_extractor(message)

	# extract USERNAMES from users already joined. (fetch infos with user text notify messages)
	text_notify_extractor(message)


'''
this method is a wrapper for two methods checking if an ip can be removed from username-list. 
each method is based on a different scenario/use case
'''
def remove_lost_connection(message):
	# first use case: {"message":"Resetting state machine.","timestamp":"1572879071.8838224","dslp-ip":"xx.xxx.x.x"}]'
	loss_due_to_resetting(message)

	# second use case: "message":"Connection to xx.xxx.x.x:xxxxx lost.
	loss_due_to_connection_lost(message)


if __name__ == "__main__":
	connect(s)
	while True:
		msg = str(s.recvfrom(65565)[0])
		# print(msg) # ♥ watch the beauty of network traffic ♥
		sniff_sniff(s, msg) # contains user_join_extractor() and text_notify_extractor()
		remove_lost_connection(msg) # contains loss_due_to_resetting() and loss_due_to_connection_lost()
