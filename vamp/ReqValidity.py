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
from smilevalidation.Validation import Validation


class ReqValidity:
	"""

	"""
	def __init__(self, log: Logger):
		"""

		"""
		# public
		self.error  = ErrorBase()
		self.log    = log

	def pullGet(self) -> dict:
		"""

		:return:
		"""
		try:
			self.error.setFalse()
			return {}

		except Exception as e:
			self.error.setTrue(code= 601, message= str(e))
			self.log.error(title= 'core.ReqValidation.pullGet Exception', content= f'{str(e)}')
			return {}

	def pullPost(self) -> dict:
		"""

		:return:
		"""
		try:
			self.error.setFalse()
			return {}

		except Exception as e:
			self.error.setTrue(code= 602, message= str(e))
			self.log.error(title= 'core.ReqValidation.pullPost Exception', content= f'{str(e)}')
			return {}
