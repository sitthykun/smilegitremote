"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# external
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
# internal
from entity.data.Auth import Auth
from entity.data.Role import Role


class Project:
	"""

	"""
	class Constant:
		AUTH            = 'auth'
		DATE_TIME       = 'datetime_format'
		ENV             = 'env'
		FORCE_CLONE     = 'force_clone'
		FORCE_PULL      = 'force_pull'
		GIT_BRANCH      = 'git_branch'
		GIT_DIR         = 'git_dir'
		GIT_TOKEN       = 'git_token'
		GIT_REMOTE_ORIGIN   = 'git_remote_origin'
		GIT_REMOTE_URL  = 'git_remote_url'
		GIT_USERNAME    = 'git_username'
		NAME            = 'name'
		NOTE            = 'note'
		TRIGGER         = 'trigger'
		WHITE_IP        = 'white_ip'

	class Trigger:
		# array of them
		AFTER           = 'after'
		BEFORE          = 'before'

		def __init__(self, data: dict):
			"""

			:param data:
			"""
			self.after  = []
			self.before = []
			# load data with validation
			self.__load(data)

		def __load(self, data: dict) -> None:
			"""

			:param data:
			:return:
			"""
			if data:
				# add if valid
				if data.get(self.BEFORE):
					self.before = data.get(self.BEFORE)
				# add if valid
				if data.get(self.AFTER):
					self.after  = data.get(self.AFTER)

	def __init__(self, data: dict):
		"""

		:param data:
		"""
		# private
		# # 1234567
		self.__id           = ''
		# # load all data
		self.__data         = data

		# public
		self.auth           = self.__getAuth(self.__data.get(Project.Constant.AUTH))
		self.dateTime       = self.__data.get(Project.Constant.DATE_TIME)
		self.env            = self.__data.get(Project.Constant.ENV)
		self.forceClone     = self.__data.get(Project.Constant.FORCE_CLONE)         or  'false'
		self.forcePull      = self.__data.get(Project.Constant.FORCE_PULL)          or  'false'
		self.gitBranch      = self.__data.get(Project.Constant.GIT_BRANCH)
		self.gitDir         = self.__data.get(Project.Constant.GIT_DIR)
		self.gitRemoteOrigin= self.__data.get(Project.Constant.GIT_REMOTE_ORIGIN)   or 'origin'
		self.gitRemotePrivateURL    = self.__getRemotePrivateURL(self.__data)
		self.gitRemoteURL   = self.__data.get(Project.Constant.GIT_REMOTE_URL)
		self.gitToken       = self.__data.get(Project.Constant.GIT_TOKEN)
		self.gitUsername    = self.__data.get(Project.Constant.GIT_USERNAME)
		self.name           = self.__data.get(Project.Constant.NAME)
		self.note           = self.__data.get(Project.Constant.NOTE)
		self.trigger        = self.Trigger(self.__data.get(Project.Constant.TRIGGER))
		self.whiteIP        = self.__data.get(Project.Constant.WHITE_IP)

	def __getAuth(self, auth: dict) -> Auth:
		"""

		:param auth:
		:return:
		"""
		return Auth(auth)

	def __getRemotePrivateURL(self, data: dict) -> str:
		"""

		:param data:
		:return:
		"""
		# append username and token
		return str(data.get(Project.Constant.GIT_REMOTE_URL)).replace('//', f'//{data.get(Project.Constant.GIT_USERNAME)}:{data.get(Project.Constant.GIT_TOKEN)}@')

	def getAll(self) -> dict:
		"""

		:return:
		"""
		return {
			Project.Constant.AUTH           : self.auth
			, Project.Constant.DATE_TIME    : self.dateTime
			, Project.Constant.ENV          : self.env
			, Project.Constant.FORCE_CLONE  : self.forceClone
			, Project.Constant.FORCE_PULL   : self.forcePull
			, Project.Constant.GIT_BRANCH   : self.gitBranch
			, Project.Constant.GIT_DIR      : self.gitDir
			, Project.Constant.GIT_TOKEN    : self.gitToken
			, Project.Constant.GIT_REMOTE_ORIGIN: self.gitRemoteOrigin
			, Project.Constant.GIT_REMOTE_URL   : self.gitRemoteURL
			, Project.Constant.GIT_USERNAME : self.gitUsername
			, Project.Constant.NAME         : self.name
			, Project.Constant.NOTE         : self.note
			, Project.Constant.TRIGGER      : self.trigger
			, Project.Constant.WHITE_IP     : self.whiteIP
		}
