"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import os
import random
import subprocess
# external
from smileerror.ErrorBase import ErrorBase


class Trigger:
	"""

	"""
	def __init__(self, bashExec: str = None, dirExec: str= None):
		"""

		:param bashExec:
		:param dirExec:
		"""
		# private
		self.__bashExec = bashExec if bashExec else '/bin/bash'
		self.__dirExec  = dirExec if dirExec else 'temp'
		# # temporary files
		self.__eBefore  = f'{random.randint(1, 50)}.sh'
		self.__eAfter   = f'{random.randint(51, 99)}.sh'
		# #
		self.__message  = []
		# public
		self.error      = ErrorBase()

	def __doBase(self, filename: str, command: str) -> None:
		"""

		:param filename:
		:param command:
		:return:
		"""
		#
		result = ''

		#
		try:
			#
			self.error.setFalse()

			# os.path.join('', self.__dirExec, filename)
			filename    = f'{self.__dirExec}/{filename}'
			# subprocess.run(command, shell= True, executable= self.__bashExec)
			result      = subprocess.check_output(
				command
				, shell     = True
				, executable= self.__bashExec
				, stderr    = subprocess.STDOUT
			)

		except subprocess.CalledProcessError as e:
			self.error.setTrue(code= 505, message= str(e))
			result = e.output

		except Exception as e:
			self.error.setTrue(code= 501, message= str(e))

		finally:
			#
			for line in result.splitlines():
				#
				self.__message.append(line.decode())

	def __doSys(self, command: str) -> None:
		"""

		:param command:
		:return:
		"""
		try:
			#
			self.error.setFalse()

			# use c port via bash with -c option
			os.system(f'{self.__bashExec} -c "{command}"')

		except Exception as e:
			self.error.setTrue(code= 502, message= str(e))

	def __makeTemp(self) -> None:
		"""

		:return:
		"""
		try:
			#
			self.error.setFalse()

			#
			if not os.path.exists(self.__dirExec):
				os.mkdir(self.__dirExec)

		except Exception as e:
			self.error.setTrue(code= 505, message= str(e))

	def __writeBash(self, filename: str, command: list) -> None:
		"""

		:param filename:
		:param command:
		:return:
		"""
		#
		self.__makeTemp()

		#
		try:
			#
			self.error.setFalse()

			#
			if os.path.exists(filename):
				# append file
				with open(filename, 'a') as fo:
					#
					for c in command:
						fo.write(f'{c};')

		except Exception as e:
			self.error.setTrue(code= 503, message= str(e))

	def doAfter(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		#
		for c in command:
			#
			self.__doSys(c)

	def doBefore(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		#
		for c in command:
			#
			self.__doSys(c)
