from twisted.internet.protocol import Factory
from Serversession import User

class DslpFactory(Factory):
	def buildProtocol(self, addr):
		user = User(addr.host, addr.port)
		print('Connection established')
		from Server import Dslp
		return Dslp(user)
