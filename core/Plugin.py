"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import os
# external
from smileerror.ErrorBase import ErrorBase


class Plugin:
	"""

	"""
	def __init__(self, bashExec: str = None):
		"""

		:param bashExec:
		"""
		# private
		self.__bashExec = bashExec if bashExec else '/bin/bash'
		# #
		self.__message  = []
		# public
		self.error      = ErrorBase()

	def __doSys(self, command: str) -> None:
		"""

		:param command:
		:return:
		"""
		try:
			#
			self.error.setFalse()

			#
			if command:
				# use c port via bash with -c option
				os.system(f'{self.__bashExec} -c "{command}"')

		except Exception as e:
			self.error.setTrue(code= 502, message= str(e))

	def __readBatch(self, filename: str, extension: str= '.txt', pluginPath: str= 'plugin') -> None:
		"""
		filename has no extension
		ex:
			plugin/flask/init
			plugin/flask/clean
		:param filename:
		:param extension:
		:param pluginPath:
		:return:
		"""
		#
		try:
			#
			self.error.setFalse()

			#
			filename = filename.replace('.', '/')
			filename = os.path.join(
				pluginPath
				, f'{filename}{extension}'
			)

			#
			if os.path.exists(filename) and os.path.isfile(filename):
				#
				with open(filename, 'r') as fo:
					#
					self.__doSys(command= fo.readline())

		except Exception as e:
			self.error.setTrue(code= 503, message= str(e))

	def doBefore(self, filename: str) -> None:
		"""

		:param filename:
		:return:
		"""
		self.__readBatch(filename= filename)

	def doAfter(self, filename: str) -> None:
		"""

		:param filename:
		:return:
		"""
		self.__readBatch(filename= filename)
