"""
Author: masakokh
Year: 2024
Package: project
Note:
Version: 1.0.0
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
		return Help().__help(title= 'checkout', method= 'post', url= 'checkout/<projectId>', body= {f'{EParam.Checkout.USERNAME}': 'xxx', f'{EParam.Checkout.PASSWORD}': 'xxx', f'{EParam.Checkout.BRANCH_NAME}': 'xxx'})

	@staticmethod
	def pull() -> dict:
		"""

		:return:
		"""
		return Help().__help(title= 'pull', method= 'post', url= 'pull/<projectId>', body= {f'{EParam.Pull.USERNAME}': 'xxx', f'{EParam.Pull.PASSWORD}': 'xxx'})
