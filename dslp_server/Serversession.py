
class User():
	active_users = [] # list of user-objects

	def __init__(self, host_ip, port, addr):
		self.host_ip = host_ip
		self.port = port
		self.addr = addr
		self.group = ''
		self.name = ''


class Group():
	active_groups = [] # list of group-objects

	def __init_(self):
		self.name = ''
		self.member = []


def get_addr_by_username(user):
	for active_user in User.active_users:
		if active_user.name == user.name:
			return active_user.addr
	return False # return false if user not exists


def get_group_by_username(user):
	for group in Group.active_groups:
		if user.group == group.name:
			return group
	return False  # return false if group not exists


def get_group_by_name(groupname):
	for group in Group.active_groups:
		if group.name == groupname:
			return group
	return False  # return false if group not exists