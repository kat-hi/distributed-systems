from twisted.internet import reactor, protocol


class Echo(protocol.Protocol):

	def dataReceived(self, data):
		self.transport.write(data)


def main():
	factory = protocol.ServerFactory()
	factory.protocol = Echo
	reactor.listenTCP(8000, factory)
	reactor.run()


if __name__ == '__main__':
	main()