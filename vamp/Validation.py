"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import json
# external
from flask import request
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
from smilevalidation.Validation import Validation as Validity
# internal
from vamp.Response import Response


class Validation:
	"""

	"""
	def __init__(self, log: Logger):
		"""

		"""
		# private
		self.__v    = Validity()
		# public
		self.log    = log

	def checkoutPost(self) -> bool:
		"""

		:return:
		"""
		try:
			return True

		except Exception as e:
			self.log.error(title= 'vamp.Validation.checkoutPost Exception', content= f'{str(e)}')
			return False

	def fail(self, message: str) -> dict:
		"""

		:param message:
		:return:
		"""
		#
		return Response().fail(
			errorMessage= message
			, errorNum  = 100
		)

	def pullPost(self) -> bool:
		"""

		:return:
		"""
		try:
			return True

		except Exception as e:
			self.log.error(title= 'vamp.Validation.pullPost Exception', content= f'{str(e)}')
			return False