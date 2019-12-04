active_groups = []
active_users = []

class User():
	def __init__(self, host_ip, port):
		self.host_ip = host_ip
		self.port = port


class Group():
	def __init_(self):
		self.name = ''
		self.users = []
		return self

	def create_group(self,group_name):
		if group_name not in active_groups:
			self.name = group_name
			active_groups.append(group_name)

	def add_user(self, user):
		if user not in self.users:
			self.users.append(user)
			active_users.append(user)

	def delete_user(self, user):
		self.users.remove(user)
		active_users.remove(user)