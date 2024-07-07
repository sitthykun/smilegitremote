"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.3
"""
# built-in
import os
# os.environ['GIT_PYTHON_REFRESH']        = 'quiet'
# os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = '/usr/bin/git'
import shutil
# external
# import git
from git import Repo, Remote
from git.exc import GitError, GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from smileerror.ErrorBase import ErrorBase
from smilelog.Logger import Logger
# internal
# from entity.data.Project import Project


class CGit:
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
				self.log.info(title= 'core.CGit.__createFolder create the folder', content= f' {theFolder}')
				return True

		except Exception as e:
			self.log.error(title= 'core.CGit.__createFolder Exception', content= f'{str(e)}')
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

			self.log.info(title='core.CGit.__cloneFrom 1', content= f'{url=}, {dir=}')
			return Repo.clone_from(
				url         = url
				, to_path   = dir
			)

		except GitCommandError as e:
			self.error.setTrue(code= 212, message= str(e))
			self.log.error(title= 'core.CGit.__cloneFrom GitCommandError', content= f'{str(e)}')

		except Exception as e:
			self.log.error(title= 'core.CGit.__cloneFrom Exception', content= f'{str(e)}')
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
			self.log.error(title= 'core.CGit.__getRepo Exception', content= f'{str(e)}')
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
				self.log.info(title= 'core.CGit.__removeFolder remove the folder tree', content= f' {theFolder}')
				#
				return True

		except Exception as e:
			self.log.error(title= 'core.CGit.__removeFolder Exception', content= f'{str(e)}')
		#
		return False

	def checkout(self, branchName: str) -> None:
		"""

		:param branchName:
		:return:
		"""
		try:
			self.error.setFalse()
			# validate
			if self.__repo.git:
				#
				self.__repo.git.checkout(branchName)
				# self.__repo.git.checkout('-b', branchName)

		except Exception as e:
			self.error.setTrue(code= 205, message= str(e))
			self.log.error(title= 'core.CGit.checkout Exception', content= f'{str(e)}')

	def cloneFrom(self, repoURL: str, dir: str= None, force: bool= False) -> None:
		"""

		:param repoURL:
		:param dir:
		:param force:
		:return:
		"""
		# get date by condition
		tempDir = dir if dir else self.__dir
		self.log.info(title= 'core.CGit.cloneFrom 2', content= f'dir: {tempDir}, {dir=}, {self.__dir=}, {repoURL=}, {force=}')
		#
		try:
			self.error.setFalse()

			# if no dir, it will automatically create a new one
			# repo_url = 'https://sitthykun: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@github.com/sitthykun/test-repo-private.git'
			r   = self.__cloneFrom(
				url     = repoURL
				, dir   = tempDir
			)

			# error
			if self.error.isTrue() and self.error.getCode() == 212:

				# must remove and create
				if force:
					# no repo, but has files (dirty)
					if self.__removeFolder(theFolder= tempDir) and self.__createFolder(theFolder= tempDir):
						self.log.info(title= 'core.CGit.cloneFrom 4', content= f'removed dir:{tempDir}, created dir: {tempDir}')

				else:
					# create only
					if self.__createFolder(theFolder= tempDir):
						self.log.info(title= 'core.CGit.cloneFrom 3', content= f'created dir: {tempDir}')

				# start cloning again
				r = self.__cloneFrom(
					url     = repoURL
					, dir   = tempDir
				)

				# check result again
				if self.error.isTrue():
					self.log.fail(title= 'core.CGit.cloneFrom 4', content= f'{self.error.getMessage()}')

				else:
					# update object
					self.__repo = r
					self.__dir  = dir
					self.log.success(title= 'core.CGit.cloneFrom 5', content= f'dir: {tempDir}, {dir=}, {self.__dir=}, {repoURL=}')

			# no error
			else:
				self.__repo = r
				self.__dir  = tempDir
				self.log.info(title= 'core.CGit.cloneFrom 1', content= f'dir: {tempDir}, {dir=}, {self.__dir=}, {repoURL=}')

		except GitError as e:
			self.error.setTrue(code= 213, message= str(e))
			self.log.error(title= 'core.CGit.GitError GitError', content= f'{str(e)}')

		except Exception as e:
			self.error.setTrue(code= 204, message= str(e))
			self.log.error(title= 'core.CGit.cloneFrom Exception', content= f'{str(e)}')

	def exist(self, dir: str= None, remoteOrigin: str= None) -> bool:
		"""

		:param dir:
		:param remoteOrigin:
		:return:
		"""
		#
		found       = False
		minPathChars= 3
		self.log.info(title= 'core.CGit.exist 1', content= f'{dir=}')

		#
		try:
			self.error.setFalse()

			# dir not found
			if not os.path.exists(dir):
				self.error.setTrue(code= 222, message= 'The directory not found')
				return False

			#
			if dir and len(dir) > minPathChars:
				self.__repo = Repo(dir, search_parent_directories= True)
				self.log.info(title= 'core.CGit.exist 2', content= f'{dir=}, {self.__repo.working_tree_dir=}, {self.__repo.remote(remoteOrigin).url=}, lengthRemoteUrl={len(self.__repo.remote(remoteOrigin).url)}, minPatchChars: {minPathChars}')
				# check length of path
				return len(self.__repo.remote(remoteOrigin).url) > minPathChars
			#
			elif self.__dir and len(self.__dir) > minPathChars:
				self.log.info(title= 'core.CGit.exist 3', content= f'{self.__dir=}, {self.__repo.working_tree_dir=}, {self.__repo.remote(remoteOrigin).url=}, {minPathChars=}')
				# check length of path
				return len(self.__repo.remote(remoteOrigin).url) > minPathChars

		except InvalidGitRepositoryError as e:
			self.error.setTrue(code= 223, message= str(e))
			self.log.error(title= 'core.CGit.exist InvalidGitRepositoryError', content= f'{str(e)}, not found the repository')

		except Exception as e:
			self.error.setTrue(code= 221, message= str(e))
			self.log.error(title= 'core.CGit.exist Exception', content= f'{str(e)}')
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
			self.log.error(title= 'core.CGit.fetch Exception', content= f'{str(e)}')

	def getBranchName(self) -> str:
		"""

		:return:
		"""
		try:
			# https://gist.github.com/igniteflow/1760854
			return self.__repo.active_branch.name if self.__repo.active_branch else ''

		except Exception as e:
			self.log.error(title= 'core.CGit.getBranchName Exception', content= f'{str(e)}')
			return ''

	def getBranchRemoteName(self) -> str:
		"""

		:return:
		"""
		try:
			return self.__repo.active_branch.remote_name if self.__repo.active_branch else ''

		except Exception as e:
			self.log.error(title= 'core.CGit.getBranchRemoteName Exception', content= f'{str(e)}')
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
			self.log.error(title= 'core.CGit.getCommitHash Exception', content= f'{str(e)}')
			return ''

	def pull(self, remoteOrigin: str= None) -> None:
		"""

		:param remoteOrigin:
		:return:
		"""
		try:
			#
			self.error.setFalse()

			if self.__repo:
				# git
				# self.__repo.remotes.origin.pull()
				self.__repo.remote(remoteOrigin).pull()
				self.log.info(title= 'core.CGit.pull 1', content= f'{remoteOrigin=}, {self.__repo.remote(remoteOrigin).url=}')

			else:
				#
				self.error.setTrue(code= 208, message= 'no reference')

		except Exception as e:
			self.error.setTrue(code= 202, message= str(e))
			self.log.error(title= 'core.CGit.pull Exception', content= f'{str(e)}')

	def remote(self, origin: str= 'origin') -> Remote | None:
		"""

		:param origin:
		:return:
		"""
		return self.__repo.remote(origin) if self.__repo else None

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
			self.__repo     = Repo(self.__dir, search_parent_directories= True)
			self.log.info(title= 'core.CGit.setRepo 1', content= f'{self.__dir=}, {self.__remoteUrl=}')

		except Exception as e:
			self.error.setTrue(code= 203, message= str(e))
			self.log.error(title= 'core.CGit.setRepo Exception', content= f'{str(e)}')
