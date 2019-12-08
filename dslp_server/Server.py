from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from Serversession import Group, User
from Serverhandler import STATE
import Serverhandler

MESSAGE_TYPES = ['request time', 'group join', 'group leave', 'group notify', 'user join',
                 'user leave', 'user text notify', 'user file notify', 'error']


class Dslp(LineReceiver):
	def __init__(self, user):
		Serverhandler.change_states('NOT_CONNECTED', 'CONNECTED')
		self.message_type = ''
		self.user = user # host, port, addr
		self.receiver = ''
		self.temp_group_name = ''


	def lineReceived(self, line):
		# these variables are kind of temporary because dslp has to be checked first before any functions are executed

		line = str(line, 'UTF-8')
		if STATE['CONNECTED']:
			if line == 'dslp/2.0':
				print('Line received(' + line + ')')
				Serverhandler.change_states('CONNECTED', 'EXPECT_MSG_TYPE')

		elif STATE['EXPECT_MSG_TYPE']:
			if line in MESSAGE_TYPES:
				print('Line received(' + line + ')')
				self.message_type = line
				Serverhandler.change_states('EXPECT_MSG_TYPE', 'EXPECT_LINE_3')
			else:
				Serverhandler.error('Unexpected type of message', self)

		elif STATE['EXPECT_LINE_3']:
			print('Line received(' + line + ')')
			if self.message_type == 'request time':
				if line == 'dslp/body':
					Serverhandler.response_time(self)
				else:
					Serverhandler.error('Didn\'t receive dslp', self)
			elif self.message_type == 'group join' or 'group leave' or 'group notify':
				self.temp_group_name = line
			elif self.message_type == 'user join' or 'user leave' or 'user text notify':
				self.user.name = line

			if self.message_type == 'request time':
				Serverhandler.change_states('EXPECT_LINE_3', 'RESETTING_STATE_MACHINE')
			elif self.message_type in MESSAGE_TYPES:
				Serverhandler.change_states('EXPECT_LINE_3', 'EXPECT_LINE_4')

		elif STATE['EXPECT_LINE_4']:
			print('Line received(' + line + ')')
			if self.message_type == 'group join':
				if line == 'dslp/body':  # if the last line from dslp is correct, create the new group:
					Serverhandler.group_join(self.user, self.temp_group_name)
					Serverhandler.change_states('EXPECT_LINE_4', 'RESETTING_STATE_MACHINE')
				else:
					Serverhandler.error('Didn\'t receive dslp', self)
			elif self.message_type == 'group leave':
				if line == 'dslp/body':
					Serverhandler.group_leave(self.user)
					Serverhandler.change_states('EXPECT_LINE_4', 'RESETTING_STATE_MACHINE')
				else:
					Serverhandler.error('Didn\'t receive dslp', self)
			elif self.message_type == 'group notify':
				expected_lines = line
				print('Expecting' + expected_lines + 'text line(s) in body.')
				line_number = int(line)
			elif self.message_type == 'user join':
				if line != 'dslp/body':
					Serverhandler.error('Didn\'t receive dslp', self)
				else:
					Serverhandler.user_join(self.user)
			elif self.message_type == 'user leave':
				Serverhandler.user_leave(self.user)
			elif self.message_type == 'user text notify':
				self.receiver = line

			if self.message_type == 'user text notify' or self.message_type == 'group notify':
				Serverhandler.change_states('EXPECT_LINE_4', 'EXPECT_LINE_5')
			elif self.message_type in MESSAGE_TYPES:
				Serverhandler.change_states('EXPECT_LINE_4', 'RESETTING_STATE_MACHINE')

		if STATE['EXPECT_LINE_5']:
			print('Line received(' + line + ')')
			if self.message_type == 'user text notify':
				Serverhandler.user_text_notify(line, self.user, self.receiver)
			elif self.message_type == 'group notify':
				pass
			Serverhandler.change_states('EXPECT_LINE_5', 'EXPECT_LINE_6')

		if STATE['EXPECT_FURTHER_DATA']:
			print('Line received(' + line + ')')
			Serverhandler.change_states('EXPECT_LINE_6', 'EXPECT_FURTHER_DATA')


class DslpFactory(Factory):
	def buildProtocol(self, addr):
		user = User(addr.host, addr.port, addr)
		print('Connection established')
		return Dslp(user)


endpoint = TCP4ServerEndpoint(reactor, 7000)
endpoint.listen(DslpFactory())
reactor.run()
