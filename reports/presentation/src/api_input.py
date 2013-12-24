def get_user_info(self, user_id):
	return self.vk.users.get(uid = user_id)[0]
