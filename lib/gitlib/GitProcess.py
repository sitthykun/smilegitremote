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
import subprocess as sb
from typing import Any
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
		self.__response     = ''
		# instance
		# public
		self.error          = ErrorBase()
		self.log            = log

	def __cmd(self, arrayCmd: list) -> None:
		"""

		:param arrayCmd:
		:return:
		"""
		# reset
		self.__response = ''

		# commit_id = sb.Popen(['git', 'merge-base', 'FETCH_HEAD', 'HEAD'], stdout=sb.PIPE)
		# test = commit_id.communicate()[0]
		# print(test)
		# sb.Popen(['git', 'diff', '--name-status', test[:-1], 'HEAD'])
		arrayCmd.insert(0, f'cd {self.__dir}')
		cmd     = sb.Popen(arrayCmd, stdout= sb.PIPE)
		print(f'{cmd=}, {arrayCmd=}')
		print(f'{cmd.returncode=}')
		print(f'{cmd.stdout=}')
		print(f'{cmd.args=}')
		self.__response = cmd.communicate()[0]

	def __cmdRespond(self) -> str:
		"""

		:return:
		"""
		return ''

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

	def __getRemoteUrl(self) -> str:
		"""

		:return:
		"""
		# run
		self.__cmd(['git', 'config', '--get', 'remote.origin.url'])
		return self.__response

	def pull(self) -> bool:
		"""

		:return:
		"""
		self.__dir  = '/var/www/github/smileerror'
		print(self.__getRemoteUrl())
		return False
