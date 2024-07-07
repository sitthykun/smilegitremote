"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.4
"""
# built-in
from typing import Any
# external
from flask import request
from smilelog.Logger import Logger
# internal
from core.CGit import CGit
from core.Batch import Batch
from core.Trigger import Trigger
import entity.Params as EParam
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
		self.__batch            = Batch()
		self.__git              = CGit(log)
		self.__isHeaderJson     = False
		self.__model            = Model(filePath= 'data', log= log)
		self.__res              = Response()
		self.__trigger          = Trigger()
		# public
		self.log                = log

	def __batchBefore(self) -> None:
		"""

		:return:
		"""
		try:
			# found command
			if self.__param(EParam.Pull.BATCH) and self.__param(EParam.Pull.BATCH).get(EParam.Events.BEFORE):
				self.__batch.doBefore(self.__param(EParam.Pull.BATCH)[EParam.Events.BEFORE])

		except Exception as e:
			self.log.error(title= 'vamp.Action.__batchBefore Exception', content= f'{str(e)}')

	def __batchAfter(self) -> None:
		"""

		:return:
		"""
		try:
			# found command
			if self.__param(EParam.Pull.BATCH) and self.__param(EParam.Pull.BATCH).get(EParam.Events.AFTER):
				self.__batch.doAfter(self.__param(EParam.Pull.BATCH)[EParam.Events.AFTER])

		except Exception as e:
			self.log.error(title= 'vamp.Action.__batchAfter Exception', content= f'{str(e)}')

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
			if self.__git.exist(project.gitDir, project.gitRemoteOrigin):
				# instance first
				self.log.info(title= 'Action.__checkout', content='git not exist > before setRepo')
				self.__git.setRepo(project.gitDir, project.gitRemoteURL)
				self.log.info(title= 'Action.__checkout', content= 'git not exist > after setRepo')

				#
				if self.__git.error.isTrue():
					# remove token
					project.auth.removeToken(username= username)
					self.log.warning(title= 'Action.__checkout', content= 'git not exist after setRepo is found error')
					#
					return self.__res.fail(self.__git.error.getMessage(), 400)
				#
				else:
					# compare the branch to avoid broken something on next step after checkout branch or any source inside
					# the current directory
					if self.__git.getBranchName() != project.gitBranch:
						self.log.warning(title= 'Action.__checkout', content= 'not a default')
						# checkout the branch
						self.log.warning(title='Action.__checkout', content= 'before checkout')
						self.__git.checkout(branchName)
						self.log.warning(title= 'Action.__checkout', content= 'after checkout')

						# found error
						if self.__git.error.isTrue():
							self.log.warning(title= 'Action.__checkout', content= 'found error after checkout command and then remove token')
							# remove token
							project.auth.removeToken(username= username)
							#
							return self.__res.fail(self.__git.error.getMessage(), 400)

						#
						else:
							self.log.success(title= 'Action.__checkout', content= 'checkout success')
							#
							commitId = self.__git.getCommitHash()
							self.log.info(title= 'Action.__checkout', content= f'{commitId=}')
							# render batch after
							self.__batchAfter()
							# remove token
							project.auth.removeToken(username= username)

							#
							return self.__res.success(
								env             = project.env
								, projectName   = project.name
								, branchName    = branchName
								, commitId      = commitId
							)
					# default branch
					else:
						self.log.success(title= 'Action.__checkout', content= 'checkout the default branch name')
						#
						commitId = self.__git.getCommitHash()
						# render batch after
						self.__batchAfter()
						# remove token
						project.auth.removeToken(username=username)

						#
						return self.__res.success(
							env             = project.env
							, projectName   = project.name
							, branchName    = project.gitBranch
							, commitId      = commitId
						)

			# exits
			self.log.info(title= 'Action.__checkout', content= 'git.exists')
			# remove token
			project.auth.removeToken(username= username)
			# fail
			return self.__res.fail('Not found git directory', 400)

		# remove token
		project.auth.removeToken(username=username)
		# fail
		return self.__res.fail('No directory', 400)

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

	def __pull(self, projectId: str, username: str, token: str, branch: str= None) -> dict:
		"""

		:param projectId:
		:param username:
		:param token:
		:param branch:
		:return:
		"""
		# init
		commitId    = ''
		foundDirty  = False
		# find project
		project     = self.__model.data.getProjectById(projectId)
		project.auth.setRootPath(path= self.__model.getPath())

		# verify dir and compare auth
		if project.gitDir != '' and project.auth.findUsernameToken(username= username, token= token):
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
					self.__trigBefore(project.trigger.before)

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
			self.log.warning(title= 'core.Action.pullGet 4', content= f'before run __trigBefore')
			# run
			self.__trigBefore(project.trigger.before)
			self.log.warning(title= 'core.Action.pullGet 4', content= f'after run __trigBefore')
			# compare the branch to avoid broken something on next step after checkout branch or any source inside
			# the current directory
			# branch is a current request
			# project.gitBranch is a default setting
			branchName  = branch if branch else project.gitBranch

			#
			if self.__git.getBranchName() != branchName:
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
			# run before
			self.__batchBefore()

			#
			if self.__git.isDirty():
				#
				foundDirty  = True
				# git stash add
				self.__git.stashAdd()

			# get a new code
			self.__git.pull(remoteOrigin= project.gitRemoteOrigin)

			# clear stash
			if foundDirty:
				self.__git.stashClear()

			# found error
			if self.__git.error.isTrue():
				# remove token
				project.auth.removeToken(username= username)
				#
				return self.__res.fail(self.__git.error.getMessage(), 400)

			# the latest step
			commitId    = self.__git.getCommitHash()
			self.log.warning(title= 'core.Action.pullGet 2', content= f'{commitId}')

			# batch
			self.__batchAfter()
			# run after
			self.__trigAfter(project.trigger.after)

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

	def __trigAfter(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		self.__trigger.doAfter(command)

	def __trigBefore(self, command: list) -> None:
		"""

		:param command:
		:return:
		"""
		self.__trigger.doBefore(command)

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
			, branch    = self.__param(EParam.Pull.BRANCH)
		)

	def tokenPost(self) -> Any:
		"""

		:return:
		"""
		return self.__generateToken(
			username    = self.__param(EParam.Token.USERNAME)
			, password  = self.__param(EParam.Token.PASSWORD)
		)
