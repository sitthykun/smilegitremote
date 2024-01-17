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


class Role:
	"""

	"""
	class Constant:
		"""

		"""
		ENABLE  = 'enable'
		ROLE    = 'role'

	class RoleList:
		"""

		"""
		def __init__(self, role: str, enable: str):
			"""

			:param role:
			:param enable:
			"""
			# public
			self.enable     = enable
			self.role       = role

	def __init__(self, data: dict):
		"""

		"""
		# private
		self.__data         = data
		self.__error        = ErrorBase()
		# # variable
		self.__keyMain      = 'role'
		# data
		self.__list         = []
		# lazy loading
		self.__load()

	def __load(self) -> None:
		"""

		:return:
		"""
		if self.__data.get(self.__keyMain):
			self.__list = self.__data.get(self.__keyMain)

	def get(self, index: int) -> RoleList | None:
		"""

		:param index:
		:return:
		"""
		try:
			return (
				self.RoleList(
					self.__list[index][Role.Constant.ROLE]
					, self.__list[index][Role.Constant.ENABLE]
				)
			) if self.__list[index] else None

		except Exception as e:
			self.__error.setTrue(code= 401, message= str(e))
			return None
