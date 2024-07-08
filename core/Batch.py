"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.3
"""
# built-in
import os
# external
from smileerror.ErrorBase import ErrorBase


class Batch:
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

			# double-check
			if command and len(command) > 1:
				# use c port via bash with -c option
				os.system(f'{self.__bashExec} -c "{command}"')

		except Exception as e:
			self.error.setTrue(code= 502, message= str(e))

	def __readBatch(self, filename: str, extension: str= '.txt', batchPath: str= 'batch') -> None:
		"""
		filename has no extension
		ex:
			batch/flask/init
			batch/flask/clean
		:param filename:
		:param extension:
		:param batchPath:
		:return:
		"""
		#
		try:
			#
			self.error.setFalse()

			# prevent empty string
			if filename != '':
				#
				filename = filename.replace('.', '/')
				filename = os.path.join(
					batchPath
					, f'{filename}{extension}'
				)

				#
				if os.path.exists(filename) and os.path.isfile(filename):
					#
					with open(filename, 'r') as fo:
						# # read all lines
						# lines   = fo.readlines()
						#
						# # loop to execute all commands as possible
						# for line in lines:
						# 	#
						# 	self.__doSys(command= line)
						# loop
						for line in fo:
							self.__doSys(command= line)

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
