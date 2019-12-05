from twisted.internet import reactor, protocol, endpoints
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ServerEndpoint
from Serverhandler import STATE
import Serversession
import Serverhandler

MESSAGE_TYPES = ['request time', 'group join', 'group leave', 'group notify', 'user join',
                 'user leave', 'user text notify', 'user file notify', 'error']



class Dslp(LineReceiver):
	group_name = ''
	username = ''

	def __init__(self, user):
		Serverhandler.change_states('NOT_CONNECTED', 'CONNECTED')
		self.message_type = ''
		self.user = user

	def lineReceived(self, line):
		# these variables are kind of temporary because dslp has to be checked first before any functions are executed
		temp_group_name = ''
		temp_user_name = ''
		temp_text = ''

		line = str(line, 'UTF-8')

		if STATE['CONNECTED']:
			if line == 'dslp/2.0':
				print('Line received(' + line + ')')
				Serverhandler.change_states('CONNECTED', 'EXPECT_MSG_TYPE')

		elif STATE['EXPECT_MSG_TYPE']:
			if line in MESSAGE_TYPES:
				self.message_type = line
				print('Line received(' + line + ')')
				Serverhandler.change_states('EXPECT_MSG_TYPE', 'EXPECT_LINE_3')
			else:
				self.error('Unexpected type of message')

		elif STATE['EXPECT_LINE_3']:
			print('Line received(' + line + ')')
			if self.message_type == 'request time':
				if line == 'dslp/body':
					self.response_time()
			elif self.message_type == 'group join':
				temp_group_name = line
			elif self.message_type == 'group leave':
				temp_group_name = line
			elif self.message_type == 'group notify':
				pass
			elif self.message_type == 'user join':
				temp_user_name = line
			elif self.message_type == 'user leave':
				Serversession.User.delete_user(self.user)
			elif self.message_type == 'user text notify':
				pass
			Serverhandler.change_states('EXPECT_LINE_3', 'EXPECT_LINE_4')

		elif STATE['EXPECT_LINE_4']:
			print('Line received(' + line + ')')
			if self.message_type == 'group join':
				if line == 'dslp/body':  # if the last line from dslp is correct, create the new group:
					self.group_join(temp_group_name)
				else:
					self.error('Didn\'t receive dslp')
			elif self.message_type == 'group leave':
				if line == 'dslp/body':
					Serverhandler.group_leave()
				else:
					self.error('Didn\'t receive dslp')
			elif self.message_type == 'group notify':
				expected_lines = line
				print('Expecting' + expected_lines + 'text line(s) in body.')
				line = int(line)
				if line > 1:
					Serverhandler.change_states('EXPECT_LINE_4', 'EXPECT_LINE_5')
			elif self.message_type == 'user join':
				print('Line received(' + line + ')')
			elif self.message_type == 'user leave':
				Serversession.active_users.remove(self.user)
			elif self.message_type == 'user text notify':
				Serverhandler.change_states('EXPECT_LINE_4', 'EXPECT_LINE_5')

		if STATE['EXPECT_LINE_5']:
			pass



from DslpFactory import DslpFactory

endpoint = TCP4ServerEndpoint(reactor, 8000)
endpoint.listen(DslpFactory())
reactor.run()
