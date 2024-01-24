"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.1
"""
# built-in
import datetime
import json
from typing import Any
# external
from flask import jsonify, request


class Response:
	"""

	"""
	def __init__(self, isHeaderJson: bool= True):
		"""

		:param isHeaderJson:
		"""
		# private
		self.__dateTimeFormat   = '%Y-%m-%d %H:%M:%S'
		self.__isHeaderJson     = isHeaderJson

	def __getDateTime(self) -> str:
		"""

		:return:
		"""
		return datetime.datetime.utcnow().strftime(self.__dateTimeFormat)

	def __respond(self, data: dict, code: int= 200) -> Any:
		"""

		:param data:
		:param code:
		:return:
		"""
		#  curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"kara\", \"password\" : \"123456\"}" "http://127.0.0.1:6060/pull/123"
		self.__setHeaderJson()
		#
		if self.__isHeaderJson:
			if isinstance(data, dict):
				r               = jsonify(data)
				r.status_code   = code
				return r

			elif isinstance(data, str):
				r               = jsonify({'data': data})
				r.status_code   = code
				#
				return r

			# default
			elif isinstance(data, int):
				r               = jsonify({'data': data})
				r.status_code   = code
				#
				return r
		#
		return data, code

	def __setHeaderJson(self) -> None:
		"""

		:return:
		"""
		#
		contentType = request.headers.get('Content-Type')

		#
		if contentType == 'application/json':
			self.__isHeaderJson = True
			self.__param        = request.json

	def Fail(self, errorMessage: str, errorNum: int, status: str= 'fail', hsc: int = 400) -> dict:
		"""

		:param errorMessage:
		:param errorNum:
		:param status:
		:param hsc: http status code
		:return:
		"""
		return self.__respond(
			data    = {
				'status'        : status
				, 'error'       : {
					'code'      : errorNum
					, 'message' : errorMessage
				}
				, 'datetime'    : self.__getDateTime()
			}
			, code  = hsc
		)

	def Success(self, env: str, projectName: str, branchName: str, commitId: str, status: str= 'success', hsc: int = 200) -> dict:
		"""

		:param env:
		:param projectName:
		:param branchName:
		:param commitId:
		:param status:
		:param hsc: http status code
		:return:
		"""
		return self.__respond(
			data    = {
				'status'        : status
				, 'env'         : env
				, 'project_name': projectName
				, 'branch_name' : branchName
				, 'commit'      : commitId
				, 'datetime'    : self.__getDateTime()
			}
			, code  = hsc
		)
