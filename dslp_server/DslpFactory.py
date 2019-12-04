from twisted.internet.protocol import Factory
from Serversession import User

class DslpFactory(Factory):
	def __init__(self):
		self.users = []

	def buildProtocol(self, addr):
		user = User(addr.host, addr.port)
		self.users.append(user)
		print('Connection established')
		from Server import Dslp
		return Dslp(user)
