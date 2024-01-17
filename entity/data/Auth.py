"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
# external
from smileerror.ErrorBase import ErrorBase


class Auth:
	"""

	"""
	class Constant:
		"""

		"""
		AUTH    = 'auth'
		PASSWORD= 'password'
		ROLE    = 'role'
		USERNAME= 'username'

	class AuthList:
		"""

		"""
		def __init__(self, username: str, password: str, role: str):
			"""

			:param username:
			:param password:
			:param role:
			"""
			# public
			self.password   = password
			self.role       = role
			self.username   = username

	def __init__(self, data: dict):
		"""

		"""
		# private
		self.__data         = data
		self.__error        = ErrorBase()
		self.__list         = []
		# lazy loading
		self.__load()

	def __load(self) -> None:
		"""

		:return:
		"""
		for i in range(len(self.__data)):
			self.__list.append(self.__data[i])

	def get(self, index: int) -> AuthList | None:
		"""

		:param index:
		:return:
		"""
		try:
			return self.AuthList(
					username    = self.__list[index].get(Auth.Constant.USERNAME)
					, password  = self.__list[index].get(Auth.Constant.PASSWORD)
					, role      = self.__list[index].get(Auth.Constant.ROLE) if self.__list[index].get(Auth.Constant.ROLE) else None
			) if self.__list[index] else None

		except Exception as e:
			self.__error.setTrue(code= 301, message= str(e))
			return None

	def findUsernamePassword(self, username: str, password: str) -> bool:
		"""

		:param username:
		:param password:
		:return:
		"""
		for d in self.__data:
			if d.get(Auth.Constant.USERNAME) == username and d.get(Auth.Constant.PASSWORD) == password:
				return True
		#
		return False

	def length(self) -> int:
		"""

		:return:
		"""
		return len(self.__data)
