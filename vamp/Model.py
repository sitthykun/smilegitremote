"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import json
import os
# external
from git import Repo
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
# internal
from entity.Data import Data


class Model(ErrorBase):
	"""

	"""
	AUTH    = 'auth'
	PROJECT = 'project'
	ROLE    = 'role'

	def __init__(self, filePath: str, log: Logger):
		"""

		:param filePath:
		:param log:
		"""
		# init
		super().__init__()

		# private
		self.__filePath = filePath

		# public
		self.data       = Data(
			auth        = self.__readList(f'{self.__filePath}/{self.AUTH}.json')
			, project   = self.__readDict(f'{self.__filePath}/{self.PROJECT}.json')
			, role      = self.__readList(f'{self.__filePath}/{self.ROLE}.json')
		)
		self.log        = log

	def __readDict(self, filename: str) -> dict | list:
		"""

		:param filename:
		:return:
		"""
		try:
			self.setFalse()
			#
			if os.path.exists(filename):
				with open(filename, 'r') as fo:
					return json.load(fo)
			# empty
			return {}

		except Exception as e:
			self.setTrue(code= 101, message= str(e))
			self.log.error(title= 'core.Model.__readDict Exception', content= f'{str(e)}')
			# empty
			return {}

	def __readList(self, filename: str) -> list:
		"""

		:param filename:
		:return:
		"""
		try:
			self.setFalse()
			#
			if os.path.exists(filename):
				with open(filename, 'r') as fo:
					return json.load(fo)
			# empty
			return []

		except Exception as e:
			self.setTrue(code= 102, message= str(e))
			self.log.error(title= 'core.Model.__readList Exception', content= f'{str(e)}')
			# empty
			return []

	def getPath(self) -> str:
		"""

		:return:
		"""
		return self.__filePath
