"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.1
"""
# built-in
from __future__ import annotations
import os
# external
from smileerror.ErrorBase import ErrorBase
# internal
from core.Util import Util


class Auth:
	"""

	"""
	class Constant:
		"""

		"""
		AUTH    = 'auth'
		PASSWORD= 'password'
		ROLE    = 'role'
		# for login session
		TOKEN   = 'token'
		USERNAME= 'username'

	class AuthList:
		"""

		"""
		def __init__(self, username: str, password: str, role: str, token: str= None):
			"""

			:param username:
			:param password:
			:param role:
			:param token:
			"""
			# public
			self.password   = password
			self.role       = role
			# for login session
			self.token      = token
			self.username   = username

	def __init__(self, data: list):
		"""

		:param data:
		"""
		# private
		self.__data         = data
		self.__list         = []
		self.__path         = os.path.join(self.Constant.TOKEN)
		# public
		self.error          = ErrorBase()
		# lazy loading
		self.__load()

	def __generateToken(self, username: str) -> str | None:
		"""

		:param username:
		:return:
		"""
		#
		value = Util.mergeStr(
			value1  = username
			, value2= Util.encrypt()
		)

		#
		try:
			#
			self.error.setFalse()
			print(os.path.join(self.Constant.TOKEN, username))
			print(value)

			#
			with open(f'{os.path.join(self.__path, username)}', 'w') as fo:
				# write to file
				fo.write(value)

		except Exception as e:
			self.error.setTrue(code= 304, message= str(e))
			return None
		#
		return value

	def __getTokenFromFile(self, username: str) -> str | None:
		"""

		:param username:
		:return:
		"""
		# init
		value   = ''

		#
		try:
			self.error.setFalse()

			#
			with open(f'{os.path.join(self.__path, username)}', 'r') as fo:
				# write to file
				value   = (
					''.join(
						fo.readlines()
					)
				).strip()

		except Exception as e:
			self.error.setTrue(code= 303, message= str(e))
			return None
		#
		return value

	def __load(self) -> None:
		"""

		:return:
		"""
		for i in range(len(self.__data)):
			self.__list.append(self.__data[i])

	def findUsername(self, username: str) -> bool:
		"""

		:param username:
		:return:
		"""
		for i in range(self.length()):
			if self.__data[i].get(Auth.Constant.USERNAME) == username:
				return True
		#
		return False

	def findUsernamePassword(self, username: str, password: str) -> bool:
		"""

		:param username:
		:param password:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			for i in range(self.length()):
				if self.__data[i].get(Auth.Constant.USERNAME) == username and self.__data[i].get(Auth.Constant.PASSWORD) == password:
					return True
			#
		except Exception as e:
			self.error.setTrue(code= 302, message= str(e))
		#
		return False

	def findUsernameToken(self, username: str, token: str) -> bool:
		"""

		:param username:
		:param token:
		:return:
		"""
		for d in self.__data:
			if d.get(Auth.Constant.USERNAME) == username:
				print(f'11= {token}')
				print(f'22= {self.__getTokenFromFile(username= username)}')
				return self.__getTokenFromFile(username= username) == token
		#
		return False

	def get(self, data: list) -> Auth:
		"""

		:param data:
		:return:
		"""
		return Auth(data= data)

	def getByIndex(self, index: int) -> AuthList | None:
		"""

		:param index:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			return self.AuthList(
				username=self.__list[index].get(Auth.Constant.USERNAME)
				, password=self.__list[index].get(Auth.Constant.PASSWORD)
				,
				role=self.__list[index].get(Auth.Constant.ROLE) if self.__list[index].get(Auth.Constant.ROLE) else None
				, token=self.__list[index].get(Auth.Constant.TOKEN) if self.__list[index].get(
					Auth.Constant.TOKEN) else None
			) if self.__list[index] else None

		except Exception as e:
			self.error.setTrue(code= 306, message= str(e))
			return None

	def getList(self, index: int) -> AuthList | None:
		"""

		:param index:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			return self.AuthList(
					username    = self.__list[index].get(Auth.Constant.USERNAME)
					, password  = self.__list[index].get(Auth.Constant.PASSWORD)
					, role      = self.__list[index].get(Auth.Constant.ROLE) if self.__list[index].get(Auth.Constant.ROLE) else None
					, token     = self.__list[index].get(Auth.Constant.TOKEN) if self.__list[index].get(Auth.Constant.TOKEN) else None
			) if self.__list[index] else None

		except Exception as e:
			self.error.setTrue(code= 301, message= str(e))
			return None

	def getToken(self, username: str, password: str ) -> str | None:
		"""

		:param username:
		:param password:
		:return:
		"""
		if self.findUsernamePassword(username= username, password= password):
			return self.__getTokenFromFile(username= username)
		#
		return None

	def generateToken(self, username: str, password: str) -> str | None:
		"""

		:param username:
		:param password:
		:return:
		"""
		if self.findUsernamePassword(username= username, password= password):
			return self.__generateToken(username= username)
		#
		return None

	def length(self) -> int:
		"""

		:return:
		"""
		return len(self.__data)

	def removeToken(self, username: str) -> None:
		"""

		:param username:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			filename = os.path.join(self.__path, username)

			#
			if os.path.exists(filename):
				os.remove(filename)

		except Exception as e:
			self.error.setTrue(code= 307, message= str(e))

	def setRootPath(self, path: str) -> None:
		"""

		:param path:
		:return:
		"""
		self.__path = os.path.join(path, self.__path)
