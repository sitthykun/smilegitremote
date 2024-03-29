"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.2
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

	def __respond(self, status: str, data: dict, code: int= 200) -> Any:
		"""

		:param status:
		:param data:
		:param code:
		:return:
		"""
		#  curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"kara\", \"token\" : \"\"}" "http://127.0.0.1:6060/pull/123"
		#  curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"jojo\", \"token\" : \"eThjojjxY3Y5b2lETWxkZlVIM2VCTVlWaE1Ta0JDS3VmSllCbURJZ0FweE4wUFNtTkNqWG1Wam0ycDB4a2FhSlNHOTcyaE81cmFJOTY2NWFzZ0JtS2xZQnV5MloyOTZK\"}" "http://127.0.0.1:6060/pull/123"
		#  curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"jojo\", \"password\" : \"kara\"}" "http://127.0.0.1:6060/token/"
		# append datetime
		data.update({'datetime': self.__getDateTime()})

		#
		r   = jsonify({'status': status, 'data': data})
		r.status_code = code

		# return last
		return r

	def fail(self, errorMessage: str, errorNum: int, status: str= 'fail', hsc: int = 400) -> dict:
		"""

		:param errorMessage:
		:param errorNum:
		:param status:
		:param hsc: http status code
		:return:
		"""
		return self.__respond(
			status  = status
			, data  = {
				'error'     : {
					'code'      : errorNum
					, 'message' : errorMessage
				}
			}
			, code  = hsc
		)

	def plain(self, value: dict, status: str= 'success', hsc: int= 200) -> dict:
		"""

		:param value:
		:param status:
		:param hsc:
		:return:
		"""
		return self.__respond(
			status  = status
			, data  = value
			, code  = hsc
		)

	def success(self, env: str, projectName: str, branchName: str, commitId: str, status: str= 'success', hsc: int = 200) -> dict:
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
			status  = status
			, data  = {
				'env'           : env
				, 'project_name': projectName
				, 'branch_name' : branchName
				, 'commit'      : commitId
			}
			, code  = hsc
		)
