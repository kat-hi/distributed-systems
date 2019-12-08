
class User():
	active_users = [] # list of User-objects

	def __init__(self, host_ip, port, addr):
		self.host_ip = host_ip
		self.port = port
		self.addr = addr
		self.group = ''
		self.name = ''


class Group():
	active_groups = [] # list of groups

	def __init_(self):
		self.name = ''
		self.member = []

	def get_group_by_name(self, user):
		for group in self.active_groups:
			if user.group == group.name:
				return group


