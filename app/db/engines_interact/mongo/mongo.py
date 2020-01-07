from pymongo import MongoClient

from ...engines_interact.abstract.dbclient import DbClient


class MongoDBClient(DbClient):
	"""
	The helper class to connect to MongoDb and execute the query commands (select, update, insert, delete).

	"""
	__host = 'localhost'  # host address
	__port = 27017  # port to connect
	# __dbname = None	#the database name
	__db = None  # the database
	# __collection_name = None	#the collection name
	__collection = None  # the collection, equivalent to table
	__client = None

	def __init__(self, host=None, port=None):
		"""
		The constructor.

		:param host: The MongoDB address to connect.

		:param port: The port to MongoDB (27017 by default).

		"""
		if host != None:
			self.__host = host
		if port != None:
			self.__port = port
		# self.__dbname = dbname
		self._connect()

	def _connect(self):
		self.__client = MongoClient(host=self.__host, port=self.__port)

	def get_db(self, dbname=None):
		"""
		Return a database in Mongo Database

		:param dbname: database name

		:return: Database
		"""
		if dbname == None:
			return None
		else:
			if self.__client == None:
				self._connect()
			self.__db = self.__client[dbname]
			return self.__db

	def get_collection(self, dbname, colname):
		"""
		Returns collection (all documents) in the database.

		:param dbname: database name.

		:param colname: collection name.

		:return: The collection of documents.
		"""
		if dbname == None or colname == None:
			return None
		else:
			if self.__client == None:
				self._connect()
			# if self.__db == None:
			# 	self.db = self.__client[dbname]
			# self.__db = self.__client[dbname]
			self.get_db(dbname=dbname)
			self.__collection = self.__db[colname]
			return self.__collection

	def get_documents(self, dbname, colname, filter_text=None):
		"""
		Returns a collection of documents by filter text.

		:param dbname: The database name.

		:param colname: The collection name.

		:param filter_text:	The filter text.

		:return: The collection of documents.

		"""
		if filter_text == None:
			return None
		if self.__collection == None:
			self.get_collection(dbname=dbname, colname=colname)
		return self.__collection.find(filter_text)

	def get_document(self, dbname, colname, filter_text=None):
		"""
		Return the document by filter text.

		:param dbname: The database name.

		:param colname:	The colection Name.

		:param filter_text:	the filter text.

		:return: the document that satisfied the condition in filter text.
		"""
		if filter_text == None:
			return None
		if self.__collection == None:
			self.get_collection(dbname=dbname, colname=colname)
		return self.__collection.find_one(filter_text)

	def get_object_id(self, dbname, colname, filter_text):
		"""
		Return the object_id of the document in the collection by filter_text.

		:param dbname: the database name.

		:param colname: the collection name.

		:param filter_text: the filter text (uses for filter the condition).

		:return: the object_id.
		"""
		document = self.get_document(dbname=dbname, colname=colname, filter_text=filter_text)
		if document == None:
			return None
		else:
			return document['_id']

	def insert_document(self, dbname, collection, document):
		"""
		Inserts the document into database.

		:param dbname: the database name.

		:param collection: the collection name.

		:param document: the document to insert.

		:return: The result of the inserting process.
		"""
		if self.__client == None:
			self._connect()
		if self.__db == None:
			self.__db = self.__client[dbname]
		return self.__db[collection].insert_one(document=document)

	def update_document(self, dbname, collection, id_field, id_value, field_name, field_value):
		"""
		Update field in a document in collection by using id_field.

		:param dbname: the database name.

		:param collection: the collectio name.

		:param id_field: the field_id (id of document).

		:param id_value: the id value.

		:param field_name: the field name that needs to be changed.

		:param field_value: the new value to change.

		:return: The result of the updating process.
		"""
		if self.__client == None:
			self._connect()
		if self.__db == None:
			self.__db = self.__client[dbname]
		return self.__db[collection].update_one({id_field: id_value}, {"$set": {field_name: field_value}})

	def update_document_by_id(self, dbname, collection, id_value, field_name, field_value):
		"""
		Update field in a document in collection by using the object_id.

		:param dbname: the database name.

		:param collection: the collection name.

		:param id_value: the id value.

		:param field_name: the field name.

		:param field_value: the field value.

		:return: The result of the updating process.
		"""
		if self.__client == None:
			self._connect()
		if self.__db == None:
			self.__db = self.__client[dbname]
		return self.__db[collection].update_one({"_id": id_value}, {"$set": {field_name: field_value}})

	def remove_all_document(self, dbname, collection):
		"""
		Remove all document in a colleciton (remove collection from db).

		:param dbname: the database name.

		:param collection: the collection name.

		:return: The result of the removing process.
		"""
		if self.__client == None:
			self._connect()
		if self.__db == None:
			self.__db = self.__client[dbname]
		return self.__db[collection].remove()

	def remove_document(self, dbname, collection, delete_criteria=None):
		"""
		Remove document by criteria.

		:param dbname: the database name.

		:param collection: the collection name.

		:param delete_criteria: the criteria used to delete.

		:return: The result of the deleting process.
		"""
		if self.__client == None:
			self._connect()
		if self.__db == None:
			self.__db = self.__client[dbname]
		if delete_criteria == None:  # remove all document
			return self.__db[collection].remove()
		else:
			return self.__db[collection].remove(delete_criteria, 1)

# this is region test


# dbname = 'users'
# colname = 'users'
#
# dbhelper = MongoDBClient()
# # dbhelper.get_collection(dbname, colname)
# # db = dbhelper.get_db(dbname=dbname)
# # users = db[colname]
#
# print("test get collection")
# collection = dbhelper.get_collection(dbname=dbname, colname=colname)
# print(collection.count())
# for col in collection.find():
# 	pprint.pprint(col)
#
# print("test get many documents")
# filter_text = {'age': 29}
# documents = dbhelper.get_documents(filter_text=filter_text)
# print(documents.count())
# for doc in documents:
# 	pprint.pprint(doc)
#
# filter_text = {'user_id': 'user123'}
# print("test get only one document")
# document = dbhelper.get_document(filter_text)
# pprint.pprint(document)
#
# print("text get object id")
# object_id = dbhelper.get_object_id(filter_text)
# print(object_id)
#
# field_name = 'weight'
# field_value = '70'
#
# update_result = dbhelper.update_document_by_id(dbname=dbname, collection=colname, id_value=object_id,
# 											   field_name=field_name, field_value=field_value)
# print(update_result.raw_result)
