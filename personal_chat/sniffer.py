import re
import socket
# this script fetches all ip adressess in current network traffic
#
# the plan: ssh portforwarding: compute.beuth -> dbl44
# execute this script and watch the traffic. do regex and filter usernames?
# I wasn't allowed to watch network traffic on compute@beuth-hochschule.de
#
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

while True:
	response = str(s.recvfrom(65565))
	try:
		regex = '([0-9][0-9]*.[0-9][0-9]*.[0-9][0-9]*.[0-9][0-9]*,*)'
		print(re.search(regex, response).group())
	except AttributeError:
		continue
