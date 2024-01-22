"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import os
import shutil
import subprocess
# internal
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
# internal
from core.ReqValidity import ReqValidity
# from entity.data.Project import Project


class GitProcess:
	def __init__(self, log: Logger):
		"""

		:param log:
		"""
		# private
		self.__dir          = ''
		self.__remoteUrl    = ''
		self.__repo         = ''
		# instance
		# public
		self.error          = ErrorBase()
		self.log            = log

	def __createFolder(self, theFolder: str) -> bool:
		"""

		:param theFolder:
		:return:
		"""
		try:
			if not os.path.exists(theFolder):
				os.mkdir(theFolder)
				self.log.info(title= 'core.GitProcess.__createFolder create the folder', content= f' {theFolder}')
				return True

		except Exception as e:
			self.log.error(title= 'core.GitProcess.__createFolder Exception', content= f'{str(e)}')
		#
		return False
