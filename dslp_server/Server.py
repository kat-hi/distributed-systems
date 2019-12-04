'''
The loop is a “reactor” because it waits for and then reacts to events. For that reason it is also known as an event loop. 
And since reactive systems are often waiting on I/O, these loops are also sometimes called select loops, 
since the select call is used to wait for I/O
'''
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ServerEndpoint
import datetime
import Serversession
'''
State.NOT_CONNECTED
State.CONNECTED
State.EXPECT_MSG_TYPE
State.EXPECT_Line_??? //depends on the message type

'''
MESSAGE_TYPES = ['request time', 'group join', 'group leave', 'group notify', 'user join',
                 'user leave', 'user text notify', 'user file notify', 'error']

STATE = {'NOT_CONNECTED': False, 'CONNECTED': False, 'EXPECT_MSG_TYPE': False, 'EXPECT_LINE_3': False,
         'EXPECT_LINE_4': False, 'EXPECT_LINE_5': False}


def check_if_user_exists(self, user):
	if user in self.active_users:
		return 'User already exists'
	else:
		return 'Username checked'


def add_user(self, user):
	self.active_users.append(user)


def change_states(current_state, new_state):
	STATE[current_state] = False
	STATE[new_state] = True
	print('Changing States ' + current_state + ' >> ' + new_state)


class Dslp(LineReceiver):
	group_name = ''
	username = ''

	def __init__(self, user):
		change_states('NOT_CONNECTED', 'CONNECTED')
		self.message_type = ''

	def lineReceived(self, line):
		temp_group_name = ''
		line = str(line, 'UTF-8')
		if STATE['CONNECTED']:
			if line == 'dslp/2.0':
				print('Line received(' + line + ')')
				change_states('CONNECTED', 'EXPECT_MSG_TYPE')
		if STATE['EXPECT_MSG_TYPE']:
			if line in MESSAGE_TYPES:
				self.message_type = line
				print('Line received(' + line + ')')
			else:
				self.error('Unexpected type of message')
			'''
			if line == 'request time':
				self.request_time()
			elif line == 'group join':
				self.group_join()
			elif line == 'group leave':
				self.group_leave()
			elif line == 'group notify':
				self.group_notify()
			elif line == 'user join':
				self.user_join()
			elif line == 'user leave':
				self.user_leave()
			elif line == 'user text notify':
				self.user_text_notify()
			else:
				self.error()
				
			'''
		if STATE['EXPECT_LINE_3']:
			if self.message_type == 'request time':
				if line == 'dslp/body':
					print('Line received(' + line + ')')
					self.response_time()
			if self.message_type == 'group join':
			# if 'dslp/' not in line:
				temp_group_name = line
			change_states('EXPECT_LINE_3', 'EXPECT_LINE_4')

		if STATE['EXPECT_LINE_4']:
			if self.message_type == 'group join':
				if line == 'dslp/body':
					group = Serversession.Group
					group.create_group(temp_group_name)
					group.add_user(self. user)

			elif self.message_type == 'group leave':
				pass
			elif self.message_type == 'group notify':
				pass
			elif self.message_type == 'user join':
				pass
			elif self.message_type == 'user leave':
				pass
			elif self.message_type == ' user text notify':
				pass
			else:
				self.error('Unexpected Type of message')

		if STATE['EXPECT_LINE_5']:
			pass

	def response_time(self):
		change_states('EXPECT_MSG_TYPE', 'EXPECT_LINE_3')
		date = str(datetime.datetime.now())
		response_time_msg = ['dslp/2.0\r\n', 'response time\r\n', 'dslp/body\r\n', date + '\r\n']
		for line in response_time_msg:
			self.sendLine(bytearray(line, 'utf-8'))

	def group_join(self, group_name, user):
		group = Serversession.Group()
		group.create_group(group_name)
		group.add_user(user)

	def group_leave(self):
		pass

	def group_notify(self):
		pass

	def user_join(self):
		pass

	def user_leave(self):
		pass

	def user_text_notify(self):
		pass

	def error(self, message):
		countlines = 0
		for line in message:
			countlines += 1
		error_msg = ['dslp/2.0\r\n', 'error\r\n', 'countlines\r\n', 'dslp/body\r\n', 'message\r\n']
		for line in error_msg:
			self.sendLine(bytearray(line, 'utf8'))


from DslpFactory import DslpFactory
endpoint = TCP4ServerEndpoint(reactor, 8000)
endpoint.listen(DslpFactory())
reactor.run()
