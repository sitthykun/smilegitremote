"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.1
"""
import datetime
# built-in
import json
from typing import Any
# external
from flask import request, jsonify
from smilelog.Logger import Logger
# internal
from core.Model import Model
from core.ReqValidity import ReqValidity
from entity.param.Pull import Pull
from lib.gitlib.GitPyLib import GitPyLib
from lib.gitlib.GitProcess import GitProcess


class Action:
	"""

	"""
	def __init__(self, log: Logger):
		"""

		:param log:
		"""
		# private
		self.__dateTimeFormat   = '%Y-%m-%d %H:%M:%S'
		self.__git              = GitPyLib(log)
		self.__gs               = GitProcess(log)
		self.__isHeaderJson     = False
		self.__param            = {}
		self.__model            = Model(filePath= 'data', log= log)
		self.__reqVal           = ReqValidity(log)
		# public
		self.log                = log

	def __pull(self, projectId: str, username: str, password: str) -> dict:
		"""

		:param projectId:
		:param username:
		:param password:
		:return:
		"""
		# init
		commitId    = ''
		# find project
		project     = self.__model.data.getProjectById(projectId)

		# verify dir and compare auth
		if project.gitDir != '' and project.auth.findUsernamePassword(username= username, password= password):
			#
			if not self.__git.exist(project.gitDir, project.gitRemoteOrigin):
				# if no dir, it will automatically create a new one
				self.__git.cloneFrom(project.gitRemotePrivateURL, project.gitDir)

				if self.__git.error.isTrue():
					return self.__respond(self.__git.error.getMessage(), 400)

				else:
					commitId = self.__git.getCommitHash()
					self.log.warning(title= 'core.Action.pullGet 1', content= f'{commitId}')

			# found the repository
			else:
				# instance first
				self.__git.setRepo(project.gitDir, project.gitRemoteURL)
				self.log.warning(title= 'core.Action.pullGet 2', content= f'{self.__git.remote().url}')
				# # clean a branch first
				# self.__git.checkout('.')

				#
				if self.__git.error.isTrue():
					return self.__respond(self.__git.error.getMessage(), 400)

			self.log.warning(title= 'core.Action.pullGet 3', content= f'directory branch: {self.__git.getBranchName()}, request branch: {project.gitBranch}')
			# compare the branch to avoid broken something on next step after checkout branch or any source inside
			# the current directory
			if self.__git.getBranchName() != project.gitBranch:
				# checkout the branch
				self.__git.checkout(project.gitBranch)

				#
				if self.__git.error.isTrue():
					return self.__respond(self.__git.error.getMessage(), 400)

			# # fetch the remote
			# self.__git.fetch()
			# #
			# if self.__git.error.isTrue():
			# 	return self.__respond(self.__git.error.getMessage(), 400)

			# get a new code
			self.__git.pull(project.gitRemoteOrigin)

			#
			if self.__git.error.isTrue():
				return self.__respond(self.__git.error.getMessage(), 400)

			# the latest step
			commitId    = self.__git.getCommitHash()
			self.log.warning(title= 'core.Action.pullGet 2', content= f'{commitId}')

			#
			return self.__respond({
				'status'        : 'success'
				, 'env'         : project.env
				, 'project_name': project.name
				, 'branch_name' : project.gitBranch
				, 'commit'      : commitId
				, 'datetime'    : datetime.datetime.utcnow().strftime(self.__dateTimeFormat)
			})
		#
		return self.__respond({'status': 'fail'})

	def __pull2(self, projectId: str, username: str, password: str) -> Any:
		"""

		:param projectId:
		:param username:
		:param password:
		:return:
		"""
		# init
		commitId = ''
		# find project
		project = self.__model.data.getProjectById(projectId)

		# verify dir and compare auth
		if project.gitDir != '' and project.auth.findUsernamePassword(username= username, password= password):
			return 'success' if self.__gs.pull() else 'fail'

		return ''

	def __help(self, title: str, method: str, url: str, body: dict, code: int= 200) -> Any:
		"""

		:param title:
		:param method:
		:param url:
		:param body:
		:param code:
		:return:
		"""
		return {f'{title}_document': {'method': method, 'url': url, 'body': body}}, code

	def __respond(self, data: dict, code: int= 200) -> Any:
		"""

		:param data:
		:param code:
		:return:
		"""
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

	def pullGet(self, projectId: str, username: str, password: str, isJson: bool= False) -> Any:
		"""

		:param projectId:
		:param username:
		:param password:
		:param isJson:
		:return:
		"""
		# return self.__pull(projectId, username, password)
		return self.__pull2(projectId, username, password)

	def pullHelp(self) -> Any:
		"""

		:return:
		"""
		return self.__help(title= 'pull', method= 'post', url= 'https://domain/pull/projectId', body= {'username':'xxx', 'password': 'xxx'})

	def pullPost(self, projectId: str) -> Any:
		"""

		:param projectId:
		:return:
		"""
		#
		self.__setHeaderJson()
		#  curl -X POST -H "Content-type: application/json" -d "{\"username\" : \"kara\", \"password\" : \"123456\"}" "http://127.0.0.1:6060/pull/123"

		#
		return self.pullGet(
			projectId   = projectId
			, username  = self.__param.get(Pull.USERNAME)
			, password  = self.__param.get(Pull.PASSWORD)
		)
