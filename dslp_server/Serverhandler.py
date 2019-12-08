import datetime
from Serversession import Group, User

STATE = {'NOT_CONNECTED': False, 'CONNECTED': False, 'EXPECT_MSG_TYPE': False, 'EXPECT_LINE_3': False,
         'EXPECT_LINE_4': False, 'EXPECT_LINE_5': False, 'EXPECT_FURTHER_DATA': False}


def response_time(addr):
	date = str(datetime.datetime.now())
	response_time_msg = ['dslp/2.0\r\n', 'response time\r\n', 'dslp/body\r\n', date + '\r\n']
	for line in response_time_msg:
		addr.sendLine(bytearray(line, 'utf-8'))


def group_join(user, group_name):
	if group_name not in Group.active_groups.name:
		new_group = Group()
		new_group.name = group_name
		new_group.member.append(user)
		Group.active_groups.append(new_group)
		user.group = group_name
	else:
		user.group = group_name
		group = Group.get_group_by_name(group_name)
		group.member.append(user)
	print(user.ip + ':' + user.port + 'joins group ' + group_name)


def group_leave(user):
	User.active_users.remove(user)
	group = Group.get_group_by_name(user)
	group.member.remove(user)
	Group.active_groups.remove(user)
	print(user.ip + ':' + user.port + 'leaves group ' + user.group)


def group_notify(line, user, receiver):
	response_msg = ['dslp/2.0\r\n', 'user text notify\r\n', user.name+'\r\n', receiver+'\r\n', 'dslp/body\r\n', line+'\r\n']
	group = Group.get_group_by_name(user)
	for member in group.member:
		for line in response_msg:
			member.addr.sendLine(bytearray(line, 'utf-8'))


def user_join(user):
	User.active_users.append(user)


def user_leave(user):
	User.active_users.remove(user)


def user_text_notify(line, user, receiver):
	response_msg = ['dslp/2.0\r\n', 'user text notify\r\n', user.name+'\r\n', receiver+'\r\n', 'dslp/body\r\n', line+'\r\n']
	group = Group.get_group_by_name(user)
	for member in group.member:
		for line in response_msg:
			member.addr.sendLine(bytearray(line, 'utf-8'))


def error(message, addr):
	countlines = 0
	for line in message:
		countlines += 1
	error_msg = ['dslp/2.0\r\n', 'error\r\n', 'countlines\r\n', 'dslp/body\r\n', 'message\r\n']
	for line in error_msg:
		addr.sendLine(bytearray(line, 'utf8'))


def change_states(current_state, new_state):
	if new_state == 'RESETTING_STATE_MACHINE':
		STATE[current_state] = False
		print(new_state)
	else:
		STATE[current_state] = False
		STATE[new_state] = True
		print('Changing State ' + current_state + ' >> ' + new_state)
