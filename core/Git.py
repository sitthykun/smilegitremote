"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
"""
# built-in
import os
import shutil
import subprocess
# external
# import git
from git import Repo, Remote
from git.exc import GitError, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
# internal
from core.ReqValidity import ReqValidity
# from entity.data.Project import Project


class Git:
	"""

	"""
	def __init__(self, log: Logger):
		"""

		:param log:
		"""
		# private
		self.__dir      = ''
		self.__remoteUrl= ''
		self.__repo     = Repo()
		# instance
		# public
		self.error      = ErrorBase()
		self.log        = log

	def __createFolder(self, theFolder: str) -> bool:
		"""

		:param theFolder:
		:return:
		"""
		try:
			if not os.path.exists(theFolder):
				os.mkdir(theFolder)
				self.log.info(title= 'core.Git.__createFolder create the folder', content=f' {theFolder}')
				return True

		except Exception as e:
			self.log.error(title= 'core.Git.__createFolder Exception', content= f'{str(e)}')
		#
		return False

	def __cloneFrom(self, url: str, dir: str) -> Repo | None:
		"""

		:param url:
		:param dir:
		:return:
		"""
		try:
			#
			self.error.setFalse()

			self.log.info(title='core.Git.__cloneFrom 1', content= f'{url=}, {dir=}')
			return Repo.clone_from(
				url         = url
				, to_path   = dir
			)

		except GitCommandError as e:
			self.error.setTrue(code= 212, message= str(e))
			self.log.error(title= 'core.Git.__cloneFrom GitCommandError', content= f'{str(e)}')

		except Exception as e:
			self.log.error(title= 'core.Git.__cloneFrom Exception', content= f'{str(e)}')
			return None

	def __getRepo(self, dir: str= None) -> Repo | None:
		"""

		:param dir:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			return Repo(dir)

		except Exception as e:
			self.error.setTrue(code= 206, message= str(e))
			self.log.error(title= 'core.Git.__getRepo Exception', content= f'{str(e)}')
			return None

	def __removeFolder(self, theFolder: str, force: bool= True) -> bool:
		"""

		:param theFolder:
		:param force:
		:return:
		"""
		try:
			if os.path.exists(theFolder):
				shutil.rmtree(theFolder)
				self.log.info(title= 'core.Git.__removeFolder remove the folder tree', content= f' {theFolder}')
				#
				return True

		except Exception as e:
			self.log.error(title='core.Git.__removeFolder Exception', content= f'{str(e)}')
		#
		return False

	def checkout(self, branchName: str) -> None:
		"""

		:param branchName:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			self.__repo.git.checkout(branchName)
			# self.__repo.git.checkout('-b', branchName)

		except Exception as e:
			self.error.setTrue(code= 205, message= str(e))
			self.log.error(title= 'core.Git.checkout Exception', content= f'{str(e)}')

	def cloneFrom(self, repoURL: str, dir: str= None, force: bool= False) -> None:
		"""

		:param repoURL:
		:param dir:
		:param force:
		:return:
		"""
		# get date by condition
		temp    = dir if dir else self.__dir
		self.log.info(title= 'core.Git.cloneFrom 2', content= f'dir: {temp}, {dir=}, {self.__dir=}, {repoURL=}, {force=}')
		#
		try:
			self.error.setFalse()

			# if no dir, it will automatically create a new one
			# repo_url = 'https://sitthykun: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@github.com/sitthykun/test-repo-private.git'
			r   = self.__cloneFrom(
				url     = repoURL
				, dir   = temp
			)

			# error
			if self.error.isTrue() and self.error.getCode() == 212:

				# must remove and create
				if force:
					# no repo, but has files (dirty)
					if self.__removeFolder(theFolder= temp) and self.__createFolder(theFolder= temp):
						self.log.info(title= 'core.Git.cloneFrom 4', content= f'removed dir:{temp}, created dir: {temp}')

				else:
					# create only
					if self.__createFolder(theFolder= temp):
						self.log.info(title= 'core.Git.cloneFrom 3', content= f'created dir: {temp}')

				# start cloning again
				r = self.__cloneFrom(
					url     = repoURL
					, dir   = temp
				)

				# check result again
				if self.error.isTrue():
					self.log.fail(title= 'core.Git.cloneFrom 4', content= f'{self.error.getMessage()}')

				else:
					self.__repo = r
					self.log.success(title= 'core.Git.cloneFrom 5', content= f'dir: {temp}, {dir=}, {self.__dir=}, {repoURL=}')

			# no error
			else:
				self.__repo = r
				self.log.info(title= 'core.Git.cloneFrom 1', content= f'dir: {temp}, {dir=}, {self.__dir=}, {repoURL=}')

		except GitError as e:
			self.error.setTrue(code= 213, message= str(e))
			self.log.error(title= 'core.Git.GitError GitError', content= f'{str(e)}')

		except Exception as e:
			self.error.setTrue(code= 204, message= str(e))
			self.log.error(title= 'core.Git.cloneFrom Exception', content= f'{str(e)}')

	def exist(self, dir: str= None, remoteOrigin: str= None) -> bool:
		"""

		:param dir:
		:param remoteOrigin:
		:return:
		"""
		#
		found       = False
		minPathChars= 3
		self.log.info(title= 'core.Git.exist 1', content= f'{dir=}')

		#
		try:
			self.error.setFalse()

			# dir not found
			if not os.path.exists(dir):
				self.error.setTrue(code= 222, message= 'The directory not found')
				return False

			#
			if dir and len(dir) > minPathChars:
				g   = Repo(dir, search_parent_directories= True)
				self.log.info(title= 'core.Git.exist 2', content= f'{dir=}, {g.working_tree_dir=}, {g.remote(remoteOrigin).url=}')
				# check length of path
				return len(g.remote(remoteOrigin).url) > minPathChars
			#
			elif self.__dir and len(self.__dir) > minPathChars:
				self.log.info(title= 'core.Git.exist 3', content= f'{self.__dir=}, {self.__repo.working_tree_dir=}, {self.__repo.remote(remoteOrigin).url=}')
				# check length of path
				return len(self.__repo.remote(remoteOrigin).url) > minPathChars

		except InvalidGitRepositoryError as e:
			self.error.setTrue(code= 223, message= str(e))
			self.log.error(title= 'core.Git.exist InvalidGitRepositoryError', content= f'{str(e)}, not found the repository')

		except Exception as e:
			self.error.setTrue(code= 221, message= str(e))
			self.log.error(title= 'core.Git.exist Exception', content= f'{str(e)}')
		#
		return found

	def fetch(self) -> None:
		"""

		:return:
		"""
		try:
			self.error.setFalse()

			#
			for remote in self.__repo.remotes:
				remote.fetch()

		except Exception as e:
			self.error.setTrue(code= 201, message= str(e))
			self.log.error(title= 'core.Git.fetch Exception', content= f'{str(e)}')

	def getBranchName(self) -> str:
		"""

		:return:
		"""
		try:
			# https://gist.github.com/igniteflow/1760854
			return self.__repo.active_branch.name

		except Exception as e:
			self.log.error(title= 'core.Git.getBranchName Exception', content= f'{str(e)}')
			return ''

	def getBranchRemoteName(self) -> str:
		"""

		:return:
		"""
		try:
			return self.__repo.active_branch.remote_name

		except Exception as e:
			self.log.error(title= 'core.Git.getBranchRemoteName Exception', content= f'{str(e)}')
			return ''

	def getCommitHash(self, short: bool= False, length: int= 8) -> str:
		"""

		:param short:
		:param length:
		:return:
		"""
		try:
			# https://stackoverflow.com/questions/31956506/get-short-sha-of-commit-with-gitpython
			shaFull = self.__repo.head.commit.hexsha
			shaShort= self.__repo.git.rev_parse(shaFull, short= length)

			# return full by default
			return shaShort if short else shaFull

		except Exception as e:
			return ''

	def pull(self, remoteOrigin: str= None) -> None:
		"""

		:param remoteOrigin:
		:return:
		"""
		try:
			#
			self.error.setFalse()

			# git
			# self.__repo.remotes.origin.pull()
			self.__repo.remote(remoteOrigin).pull()
			self.log.info(title= 'core.Git.pull 1', content= f'{remoteOrigin=}, {self.__repo.remote(remoteOrigin).url=}')

		except Exception as e:
			self.error.setTrue(code= 202, message= str(e))
			self.log.error(title= 'core.Git.pull Exception', content= f'{str(e)}')

	def remote(self, origin: str= 'origin') -> Remote:
		"""

		:return:
		"""
		return self.__repo.remote(origin)

	def setRepo(self, dir: str, url: str) -> None:
		"""

		:param dir:
		:param url:
		:return:
		"""
		try:
			self.error.setFalse()
			#
			self.__dir      = dir
			self.__remoteUrl= url
			self.__repo     = git.Repo(self.__dir, search_parent_directories= True)
			self.log.info(title= 'core.Git.setRepo 1', content= f'{self.__dir=}, {self.__remoteUrl=}')

		except Exception as e:
			self.error.setTrue(code= 203, message= str(e))
			self.log.error(title= 'core.Git.setRepo Exception', content= f'{str(e)}')
