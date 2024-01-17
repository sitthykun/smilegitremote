"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# external
from smilelog.Logger import Logger
from smileerror.ErrorBase import ErrorBase
# internal
from entity.data.Auth import Auth
from entity.data.Project import Project
from entity.data.Role import Role


class Data:
	"""

	"""
	class Constant:
		"""

		"""
		PROJECTS    = 'projects'

	def __init__(self, auth: list, project: dict, role: list):
		"""

		:param auth:
		:param project:
		:param role:
		"""
		# private
		self.__auth     = auth
		self.__project  = project
		self.__role     = role

	def getAuth(self) -> list:
		"""

		:return:
		"""
		return self.__auth

	def getAuthById(self, id: int) -> Auth:
		"""

		:param id:
		:return:
		"""
		return self.__auth[id] if self.__auth[id] else None

	def getProjectById(self, id: str) -> Project | None:
		"""

		:param id:
		:return:
		"""
		if self.__project.get(self.Constant.PROJECTS).get(id):
			return Project(
				data    = self.__project.get(self.Constant.PROJECTS).get(id)
			)

		#
		return None

	def getProjects(self) -> list:
		"""

		:return:
		"""
		#
		temp    = []

		#
		for project in self.__project.get(self.Constant.PROJECTS):
			temp.append(
				Project(
					data    = self.__project.get(self.Constant.PROJECTS).get(project)
				)
			)
		#
		return temp

	def getRole(self) -> list:
		"""

		:return:
		"""
		#
		return self.__role

	def getRoleById(self, id: int) -> Role:
		"""

		:param id:
		:return:
		"""
		return self.__role[id] if self.__role[id] else None
