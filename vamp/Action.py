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
import entity.Params as EParam
from entity.data.Project import Project
from core.CGit import CGit
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
		self.__param            = {}
		self.__model            = Model(filePath= 'data', log= log)
		self.__res              = Response()
		# public
		self.log                = log

	def __checkout(self, projectId: str, branchName: str, username: str, password: str) -> dict:
		"""

		:param projectId:
		:param branchName:
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
				# instance first
				self.__git.setRepo(project.gitDir, project.gitRemoteURL)

				#
				if self.__git.error.isTrue():
					return self.__res.Fail(self.__git.error.getMessage(), 400)
				#
				else:
					# compare the branch to avoid broken something on next step after checkout branch or any source inside
					# the current directory
					if self.__git.getBranchName() != project.gitBranch:
						# checkout the branch
						self.__git.checkout(branchName)

						# found error
						if self.__git.error.isTrue():
							return self.__res.Fail(self.__git.error.getMessage(), 400)

						#
						else:
							#
							commitId = self.__git.getCommitHash()

							#
							return self.__res.Success(
								env             = project.env
								, projectName   = project.name
								, branchName    = branchName
								, commitId      = commitId
							)
					#
					else:
						#
						commitId = self.__git.getCommitHash()
						#
						return self.__res.Success(
							env             = project.env
							, projectName   = project.name
							, branchName    = project.gitBranch
							, commitId      = commitId
						)
			# fail
			return self.__res.Fail('Not found git directory', 400)
		# fail
		return self.__res.Fail('No directory', 400)

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

				# found error
				if self.__git.error.isTrue():
					return self.__res.Fail(self.__git.error.getMessage(), 400)

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
					return self.__res.Fail(self.__git.error.getMessage(), 400)

			self.log.warning(title= 'core.Action.pullGet 3', content= f'directory branch: {self.__git.getBranchName()}, request branch: {project.gitBranch}')

			# compare the branch to avoid broken something on next step after checkout branch or any source inside
			# the current directory
			if self.__git.getBranchName() != project.gitBranch:
				# checkout the branch
				self.__git.checkout(project.gitBranch)

				#
				if self.__git.error.isTrue():
					return self.__res.Fail(self.__git.error.getMessage(), 400)

			# # fetch the remote
			# self.__git.fetch()
			# #
			# if self.__git.error.isTrue():
			# 	return self.__respond(self.__git.error.getMessage(), 400)

			# get a new code
			self.__git.pull(project.gitRemoteOrigin)

			# found error
			if self.__git.error.isTrue():
				return self.__res.Fail(self.__git.error.getMessage(), 400)

			# the latest step
			commitId    = self.__git.getCommitHash()
			self.log.warning(title= 'core.Action.pullGet 2', content= f'{commitId}')

			#
			return self.__res.Success(
				env             = project.env
				, projectName   = project.name
				, branchName    = project.gitBranch
				, commitId      = commitId
			)
		#
		return self.__res.Fail('Totally, cannot pull', 400)

	def checkoutPost(self, projectId: str) -> Any:
		"""

		:param projectId:
		:return:
		"""
		return self.__checkout(
			projectId   = projectId
			, username  = self.__param.get(EParam.Checkout.USERNAME)
			, password  = self.__param.get(EParam.Checkout.PASSWORD)
			, branchName= self.__param.get(EParam.Checkout.BRANCH_NAME)
		)

	def pullPost(self, projectId: str) -> Any:
		"""

		:param projectId:
		:return:
		"""
		#
		return self.__pull(
			projectId   = projectId
			, username  = self.__param.get(EParam.Pull.USERNAME)
			, password  = self.__param.get(EParam.Pull.PASSWORD)
		)
