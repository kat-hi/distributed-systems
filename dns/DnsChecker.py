import sys, dns
import dns.resolver

zone = sys.argv[1]

def get_mailserver(zone):
	print('Mailserver:')
	try:
		mailserverlist = dns.resolver.query(zone,'MX')
		for mailserver in mailserverlist:
			print(mailserver.exchange)
	except:
		print('dns resolver failed')
	print('')

def get_dnsserver(zone):
	print("DNS-Server:")
	try:
		dnsserverlist = dns.resolver.query(zone,'NS')
		for dnsserver in dnsserverlist:
			print(dnsserver)
	except:
		print('dns resolver failed')
	print('')

def get_ip_from_www_server(zone):
	print("www-Server:")
	url = "www." + zone
	try:
		www_server_ipv4 = dns.resolver.query(url,'A')
		for server in www_server_ipv4:
			print('IPv4: ' + str(server))
	except dns.resolver.NoAnswer:
		print('IPv4: ---')
	except Exception:
		print('IPv4: ---')

	try:
		www_server_ipv6 = dns.resolver.query(url, "AAAA")
		for server in www_server_ipv6:
			print('IPv6: ' + str(server))
	except dns.resolver.NoAnswer:
		print('IPv6: ---')
	except Exception:
		print('IPv6: ---')



if __name__ == '__main__':
	get_mailserver(zone)
	get_dnsserver(zone)
	get_ip_from_www_server(zone)
