# we both have synchronous and asynchronous, it must be chosen later
# in this version, we are using synchronous version
from algoliasearch import algoliasearch
import json


class Algolia:
	"""
	This class is implementation of Algolia search engine api, used for searching the occurences of search_key word in the index_file
	(Common search)
	"""
	__app_key = '1a9680186a5bd2aec8097935213d474e'
	__app_id = 'MFF8ADG6FQ'
	__client = None
	__index = None

	def __init__(self):
		self.__connect()

	def __connect(self):
		self.__client = algoliasearch.Client(app_id=self.__app_id, api_key=self.__app_key)

	def __create_index(self, index_name):
		if self.__client == None:
			self.__connect()
		self.__index = self.__client.init_index(index_name=index_name)

	# batch = json.load(open(file=file_name))
	# self.__index.add_objects(batch)

	def search(self, index_name, query_string):
		"""
		Search from index_name by quesy_string.

		:param index_name: The index_file name in algolia search engine.

		:param query_string: The query string.

		:return: The json format of the search result.

		"""
		if self.__index == None:
			self.__create_index(index_name=index_name)
		res = self.__index.search(query=query_string)
		return res

# dataname
# test
# indexname = 'aponow_default_products'
# query = 'FreeStyle'
# alg = Algolia()
# search = alg.search(index_name=indexname, query_string=query)
# import pprint
# pprint.pprint(search)


# pprint.pprint(search)
# with open('contacts.json','r') as f:
# 	jtext = json.load(f)
# 	pprint.pprint(jtext)
