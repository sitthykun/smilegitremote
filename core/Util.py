"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import base64
import random


class Util:
	"""

	"""
	RANDOM_TIME = 128

	@staticmethod
	def encrypt(time: int= RANDOM_TIME, value: str= None) -> str:
		"""

		:param time:
		:param value:
		:return:
		"""
		return Util.covertBase64(
			value   = Util.randomStr(
				time    = time
				, value = value
			)
		)

	@staticmethod
	def covertBase64(value: str) -> str:
		"""

		:param value:
		:return:
		"""
		# encodeType  = 'ascii'
		encodeType  = 'utf-8'
		#
		return (
			base64.b64encode(
				value.encode(encodeType)
			)
		).decode(encodeType)

	@staticmethod
	def mergeStr(value1: str, value2: str) -> str:
		"""

		:param value1:
		:param value2:
		:return:
		"""
		length1 = len(value1)
		length2 = len(value2)
		rndTime = random.randint(0, length1 - 1)
		value3  = f'{value2[:rndTime]}{Util.randomStr(time= len(value1), value= value1)}{value2[rndTime:]}'

		#
		return value3[:Util.RANDOM_TIME]

	@staticmethod
	def randomStr(time: int, value: str= '') -> str:
		"""

		:param time:
		:param value:
		:return:
		"""
		chars   = []

		#
		if not value:
			value   = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

		# generate a list
		chars   = list(
			map(
				lambda x: value[x]
				, range(
					0
					, len(value)
				)
			)
		)

		# convert list to str and return the final
		return ''.join(
			random.choices(
				chars
				, k = time
			)
		)
