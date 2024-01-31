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
from flask import request
from smilelog.Logger import Logger
# internal
from core.CGit import CGit
from core.Trigger import Trigger
import entity.Params as EParam
# from entity.data.Project import Project
from vamp.Model import Model
from vamp.Response import Response


class Action:
	"""

	"""
	def __init__(self, log: Logger):
		"""

		:param log:
		"""
		# private
		# self.__dataProject      = Project()
		self.__git              = CGit(log)
		self.__isHeaderJson     = False
		self.__model            = Model(filePath= 'data', log= log)
		self.__res              = Response()
		self.__trigger          = Trigger()
		# public
		self.log                = log

	def __checkout(self, projectId: str, branchName: str, username: str, token: str) -> dict:
		"""

		:param projectId:
		:param branchName:
		:param username:
		:param token:
		:return:
		"""
		# init
		commitId    = ''
		# find project
		project     = self.__model.data.getProjectById(projectId)
		project.auth.setRootPath(path= self.__model.getPath())

		# verify dir and compare auth
		if project.gitDir != '' and project.auth.findUsernameToken(username= username, token= token):
			#
			if not self.__git.exist(project.gitDir, project.gitRemoteOrigin):
				# instance first
				self.__git.setRepo(project.gitDir, project.gitRemoteURL)

				#
				if self.__git.error.isTrue():
					# remove token
					project.auth.removeToken(username= username)
					#
					return self.__res.fail(self.__git.error.getMessage(), 400)
				#
				else:
					# compare the branch to avoid broken something on next step after checkout branch or any source inside
					# the current directory
					if self.__git.getBranchName() != project.gitBranch:
						# checkout the branch
						self.__git.checkout(branchName)

						# found error
						if self.__git.error.isTrue():
							# remove token
							project.auth.removeToken(username= username)
							#
							return self.__res.fail(self.__git.error.getMessage(), 400)

						#
						else:
							#
							commitId = self.__git.getCommitHash()
							# remove token
							project.auth.removeToken(username= username)

							#
							return self.__res.success(
								env             = project.env
								, projectName   = project.name
								, branchName    = branchName
								, commitId      = commitId
							)
					#
					else:
						#
						commitId = self.__git.getCommitHash()
						# remove token
						project.auth.removeToken(username=username)

						#
						return self.__res.success(
							env             = project.env
							, projectName   = project.name
							, branchName    = project.gitBranch
							, commitId      = commitId
						)

			# remove token
			project.auth.removeToken(username= username)
			# fail
			return self.__res.fail('Not found git directory', 400)

		# remove token
		project.auth.removeToken(username=username)
		# fail
		return self.__res.fail('No directory', 400)

	def __doAfter(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		self.__trigger.doAfter(command)

	def __doBefore(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		self.__trigger.doBefore(command)

	def __generateToken(self, username: str, password: str) -> dict:
		"""

		:param username:
		:param password:
		:return:
		"""
		#
		auth    = self.__model.data.getAuths()
		auth.setRootPath(path= self.__model.getPath())
		self.log.info(title= 'vamp.Action.__generateToken 1', content= f'{username=}, {password=}')

		#
		if auth.findUsernamePassword(username= username, password= password):
			self.log.warning(title= 'vamp.Action.__generateToken 2', content= f'{username=}, {password=}')

			#
			return self.__res.plain({
				'token': auth.generateToken(
					username    = username
					, password  = password
				)
			})

		# fail
		return self.__res.fail('No authentication', 400)

	def __param(self, key: str, defaultValue: Any= None) -> Any | None:
		"""

		:param key:
		:param defaultValue:
		:return:
		"""
		try:
			# json
			if request.get_json().get(key):
				return request.get_json().get(key)

			# form
			elif request.args.get(key):
				return request.args.get(key)

			elif request.values.get(key):
				return request.values.get(key)

			elif request.form.get(key):
				return request.form.get(key)

			else:
				return defaultValue

		except Exception as e:
			self.log.error(title= 'vamp.Action.__param Exception', content= f'{str(e)}')
			return defaultValue

	def __pull(self, projectId: str, username: str, token: str) -> dict:
		"""

		:param projectId:
		:param username:
		:param token:
		:return:
		"""
		# init
		commitId    = ''
		# find project
		project     = self.__model.data.getProjectById(projectId)
		project.auth.setRootPath(path= self.__model.getPath())

		# verify dir and compare auth
		if project.gitDir != '' and project.auth.findUsernameToken(username= username, token= token):
			# run before
			self.__doBefore(project.trigger.before)

			#
			if not self.__git.exist(project.gitDir, project.gitRemoteOrigin):
				# if no dir, it will automatically create a new one
				self.__git.cloneFrom(
					repoURL = project.gitRemotePrivateURL
					, dir   = project.gitDir
				)

				# found error
				if self.__git.error.isTrue():
					# remove token
					project.auth.removeToken(username= username)
					#
					return self.__res.fail(self.__git.error.getMessage(), 400)

				else:
					commitId = self.__git.getCommitHash()
					self.log.warning(title= 'core.Action.pullGet 1', content= f'{commitId}')

			# found the repository
			else:
				# instance first
				self.__git.setRepo(
					dir     = project.gitDir
					, url   = project.gitRemoteURL
				)
				self.log.warning(title= 'core.Action.pullGet 2', content= f'{self.__git.remote().url}')
				# # clean a branch first
				# self.__git.checkout('.')

				#
				if self.__git.error.isTrue():
					# remove token
					project.auth.removeToken(username= username)
					#
					return self.__res.fail(self.__git.error.getMessage(), 400)

			self.log.warning(title= 'core.Action.pullGet 3', content= f'directory branch: {self.__git.getBranchName()}, request branch: {project.gitBranch}')

			# compare the branch to avoid broken something on next step after checkout branch or any source inside
			# the current directory
			if self.__git.getBranchName() != project.gitBranch:
				# checkout the branch
				self.__git.checkout(branchName= project.gitBranch)

				#
				if self.__git.error.isTrue():
					# remove token
					project.auth.removeToken(username= username)
					#
					return self.__res.fail(self.__git.error.getMessage(), 400)

			# # fetch the remote
			# self.__git.fetch()
			# #
			# if self.__git.error.isTrue():
			# 	return self.__respond(self.__git.error.getMessage(), 400)

			# get a new code
			self.__git.pull(remoteOrigin= project.gitRemoteOrigin)

			# found error
			if self.__git.error.isTrue():
				# remove token
				project.auth.removeToken(username= username)
				#
				return self.__res.fail(self.__git.error.getMessage(), 400)

			# the latest step
			commitId    = self.__git.getCommitHash()
			self.log.warning(title= 'core.Action.pullGet 2', content= f'{commitId}')

			# run after
			self.__doAfter(project.trigger.after)

			# remove token
			project.auth.removeToken(username= username)

			#
			return self.__res.success(
				env             = project.env
				, projectName   = project.name
				, branchName    = project.gitBranch
				, commitId      = commitId
			)

		# remove token
		project.auth.removeToken(username= username)
		#
		return self.__res.fail('Totally, cannot pull', 400)

	def checkoutPost(self, projectId: str) -> Any:
		"""

		:param projectId:
		:return:
		"""
		return self.__checkout(
			projectId   = projectId
			, username  = self.__param(EParam.Checkout.USERNAME)
			, token     = self.__param(EParam.Checkout.TOKEN)
			, branchName= self.__param(EParam.Checkout.BRANCH_NAME)
		)

	def pullPost(self, projectId: str) -> Any:
		"""

		:param projectId:
		:return:
		"""
		#
		return self.__pull(
			projectId   = projectId
			, username  = self.__param(EParam.Pull.USERNAME)
			, token     = self.__param(EParam.Pull.TOKEN)
		)

	def tokenPost(self) -> Any:
		"""

		:return:
		"""
		return self.__generateToken(
			username    = self.__param(EParam.Token.USERNAME)
			, password  = self.__param(EParam.Token.PASSWORD)
		)
