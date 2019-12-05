import datetime
import Serversession

STATE = {'NOT_CONNECTED': False, 'CONNECTED': False, 'EXPECT_MSG_TYPE': False, 'EXPECT_LINE_3': False,
         'EXPECT_LINE_4': False, 'EXPECT_LINE_5': False}

def response_time(self):
	date = str(datetime.datetime.now())
	response_time_msg = ['dslp/2.0\r\n', 'response time\r\n', 'dslp/body\r\n', date + '\r\n']
	for line in response_time_msg:
		self.sendLine(bytearray(line, 'utf-8'))


def group_join(self, group_name):
	group = Serversession.Group()
	if group_name not in Serversession.active_groups:
		group.create_group(group_name)
	group.add_user(self.user)
	print(self.user.ip + ':' + self.user.port + 'joins group ' + group_name)


def group_leave(self):
	Serversession.active_groups.remove(self.user.group)
	print(self.user.ip + ':' + self.user.port + 'leaves group ' + self.user.group)


def group_notify():
	pass


def user_join():
	pass


def user_leave():
	pass


def user_text_notify():
	pass


def error(message):
	countlines = 0
	for line in message:
		countlines += 1
	error_msg = ['dslp/2.0\r\n', 'error\r\n', 'countlines\r\n', 'dslp/body\r\n', 'message\r\n']
	for line in error_msg:
		self.sendLine(bytearray(line, 'utf8'))


def change_states(current_state, new_state):
	STATE[current_state] = False
	STATE[new_state] = True
	print('Changing State ' + current_state + ' >> ' + new_state)