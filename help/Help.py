"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.1.0
"""
# built-in
from typing import Any
# internal
import entity.Params as EParam


class Help:
	"""

	"""
	def __help(self, title: str, method: str, url: str, body: dict, code: int= 200) -> Any:
		"""

		:param title:
		:param method:
		:param url:
		:param body:
		:param code:
		:return:
		"""
		# append
		url = f'https://domain/{url}'

		# final
		return {f'{title}_document': {'method': method, 'url': url, 'body': body}}, code

	@staticmethod
	def checkout() -> dict:
		"""

		:return:
		"""
		return Help().__help(
			title   = 'checkout'
			, method= 'post'
			, url   = 'checkout/<projectId>'
			, body  = {
				f'{EParam.Checkout.USERNAME}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Checkout.TOKEN}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Checkout.BRANCH_NAME}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Pull.BATCH}{EParam._OPTIONAL}': {
					f'{EParam.Events.AFTER}{EParam._OPTIONAL}': 'xxx.xxx'
				}
			}
		)

	@staticmethod
	def pull() -> dict:
		"""

		:return:
		"""
		return Help().__help(
			title   = 'pull'
			, method= 'post'
			, url   = 'pull/<projectId>'
			, body  = {
				f'{EParam.Pull.USERNAME}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Pull.TOKEN}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Pull.BRANCH}{EParam._OPTIONAL}':'xxx'
				, f'{EParam.Pull.BATCH}{EParam._OPTIONAL}': {
					f'{EParam.Events.BEFORE}{EParam._OPTIONAL}': 'xxx.xxx'
					, f'{EParam.Events.AFTER}{EParam._OPTIONAL}': 'xxx.xxx'
				}
			}
		)

	@staticmethod
	def tokenRequest() -> dict:
		"""

		:return:
		"""
		return Help().__help(
			title   = 'token/<projectId>'
			, method= 'post'
			, url   = 'token'
			, body  = {
				f'{EParam.Token.USERNAME}{EParam._REQUIRE}': 'xxx'
				, f'{EParam.Token.PASSWORD}{EParam._REQUIRE}': 'xxx'
			}
		)
