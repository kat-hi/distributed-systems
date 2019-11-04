import re
import socket

# fetching networking traffic,extracting IPs and dslp-usernames
# since dslp is not encrypted it is possible to extract names of all users joining the dslp-server
#

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
print('start sniffing...')
usernames = []


def connect(sock):
	server_adr = ("dbl44.beuth-hochschule.de", 21)
	try:
		sock.connect(server_adr)
	except socket.error:
		print("Something went wrong. Connection failed.")

# it works
def user_join_extractor(response):
	global usernames
	try:
		regex_user_ip = "User [\w][\w]* on connection (\d)*.(\d)*.(\d)*.(\d)*:(\d)* joins the server."
		username_from_join = re.search(regex_user_ip, response).group().split()[1]
		ip_from_join = re.search(regex_user_ip, response).group().split()[4].split(':')[0]  # extract ip without port

		# if username_from_join not in usernames:
		usernames.append(username_from_join)
		print(username_from_join + ' ' + ip_from_join)
	except AttributeError:
		pass

# it works
def text_notify_extractor(response):
	global usernames
	try:
		# "Sending user text notification from json1000 to json", "timestamp": "1572864370.3324468", "dslp-ip": "141.64.203.45"}]'
		# yet_another_regex = "Line received(.)*\, \"timestamp\"\: \"(\d)*\.(\d)*(.)* \"dslp-ip\"\: \"(\d)*\.(\d)*\.(\d)*\.(\d)*\""
		# regex_sender_ip = "Sending user text notification from [\w][\w]* to [\w][\w]*\"(.)* \"dslp-ip\"\: \"(\d)*\.(\d)*\.(\d)*\.(\d)*\""

		regex_usernames = "Sending user text notification from [\w][\w]* to [\w][\w]*\""
		usernames_from_text_notify = re.search(regex_usernames, response).group().split('"')
		sender = usernames_from_text_notify[0].split()[5]
		receiver = usernames_from_text_notify[0].split()[7]

		if sender not in usernames:
			usernames.append((sender,))
			print(sender)
			# if receiver not in usernames:
			usernames.append((receiver,))
			print(receiver)
	except AttributeError:
		pass


def sniff_sniff(s):
	while True:
		response = str(s.recvfrom(65565)[0])
		#print(response) # watch network traffic

		# first try: extracting username and ip from 'user join' message
		user_join_extractor(response)

		# second try: getting username from users already joined. (fetch infos with user text notify messages)
		# (1) fetching sender and receiver name from 'user text notify' (usernames_from_text_notify)
		# (2) fetching any ip from user text notify (yet_another_regex)
		text_notify_extractor(response)

		# third try: get users removed from server for updating current user list
		remove_lost_connection(response)


def check_ip_in_list(ip):
	for info_tuple in usernames:
		if ip == info_tuple(1):
			return info_tuple
	return False


def remove_lost_connection(response):
	#\"dslp-ip\"(.)* (\d)*.(\d)*.(\d)*.(\d)*\"\}]?
	try:
		ip = "\"dslp-ip\"(.)* (\d)*.(\d)*.(\d)*.(\d)*\"\}]?"
		ip_from_sender = re.search(ip, response).group()
		print('RESETTING', ip_from_sender.split())

		return_value = check_ip_in_list(ip_from_sender)
		if return_value == False:
			pass
		else:
			usernames.remove(return_value)
	except AttributeError:
		pass

#["newmessage",{"message":"User jsonLover0123 removed from server due to disconnect.","timestamp":"1572879039.5032785","dslp-ip":"95.91.247.8"}]
# essage":"Connection to 10.128.0.1:52887 lost.
#,["newmessage",{"message":"Resetting state machine.","timestamp":"1572879071.8838224","dslp-ip":"10.128.0.1"}]'
def update_current_user_list():
	global usernames
	print('_________________________')
	print('new list:')
	for user in usernames:
		print('-- ', user)


if __name__ == "__main__":
	connect(s)
	sniff_sniff(s)