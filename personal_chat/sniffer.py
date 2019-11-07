import socket
import struct
import string

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)


class Ethernet():
	def __init__(self, packet):
		eth_length = 14  # 6 Bytes Destination MAC Addr | 6 Bytes Source MAC Addr | 2 Bytes EtherType
		eth_header = packet[:eth_length]
		self.destination, self.source, self.upper_layer_protokoll = struct.unpack('!6s6sH', eth_header)
		self.data = packet[14:]  # get Payload/data

	def print_mac_addr(self):
		dest = map('{:02x}'.format, self.destination) # convert dec into 2-digit-hex values
		src = map('{:02x}'.format, self.source)
		mac_addr_dest = ':'.join(dest).upper() # # convert iterable into string, formatting to mac
		mac_addr_src = ':'.join(src).upper()
		print('Destination: ' + mac_addr_dest + ' | Source: ' + mac_addr_src +
		      ' | upper layer protocol: ' + str(self.upper_layer_protokoll)) # EtherType value of 0x0800 == ipv4


class IPv4:
	def __init__(self, packet):
		self.ttl, self.protokoll, self.source, self.target = struct.unpack('! 8x B B 2x 4s 4s', packet[:20])
		self.data = packet[20:]

	def print_ip_header(self):
		src = map('{:01d}'.format, self.source) # convert into 1-digit-dec value
		src_ip = '.'.join(src) # convert iterable into string
		target = map('{:01d}'.format, self.target)
		target_ip = '.'.join(target)
		print('TTL: ' + str(self.ttl) + ' | Source_IP: ' + src_ip + ' | Target_IP: ' + target_ip)

	def ipv4(self, addr):
		return '.'.join(map(str, addr))


def extract_ethernet_frame(packet):
	eth = Ethernet(packet)
	eth.print_mac_addr()
	return eth


def extract_ipv4_packet(packet, addr):
	ipv4 = IPv4(packet)
	ipv4.print_ip_header()
	ipv4.ipv4(addr)


def fetch_and_convert_data(packet):
	printables = string.ascii_letters + ' ' + string.digits + string.punctuation
	convertables = []
	for bit in packet:
		if chr(bit) in printables:
			convertables.append(chr(bit))
		else:
			convertables.append('.')
	print(''.join(convertables))


if __name__ == "__main__":
	while True:
		packet, addr = s.recvfrom(65535)
		# print(packet) # ♥ watch the beauty of network traffic
		eth = extract_ethernet_frame(packet)
		extract_ipv4_packet(eth.data, addr)
		# fetch_and_convert_data(packet) # convert data into printable values
		print('__________________________________')
