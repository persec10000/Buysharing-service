from ..abstract.dbhelper import DBHelper
from .mongo import MongoDBClient
# from models.entity import Article


class DBHelperArticle(DBHelper):
	"""
	This class helps to interact with article in database.
	"""
	__dbname = 'newsfeed'  # database name
	__collection_name = 'article'
	__host = '138.68.85.117'  # host
	__port = 27017  # host
	__client = None  # the instance of MongoDBHelper


	def __init__(self, host=None, port = None, dbname = None, collection_name = None):
		"""
		Constructor of DBHelperArticle.

		:param host: The host of database server (e.g **`localhost`**).

		:param port: The port to connect to database (e.g **`27017`**)

		:param dbname: The database name.

		:param collection_name: The collection name (this is equivalent to table in relational database)
		"""
		super().__init__()
		if dbname!=None:
			self.__dbname = dbname
		if host != None:
			self.__host = host
		if port!=None:
			self.__port = port
		if collection_name!=None:
			self.__collection_name = collection_name

	# connect to DB
	def __connect__(self):
		self.__client = MongoDBClient(self.__host, self.__port)

	# close the connection
	def __disconnect__(self):
		self.__client = None

	def __parse_article(self,document):
		"""
		Parses document (the form of Mongodb record) to object article.

		:param document: The mongodb record.

		:return: The article.
		"""
		if document==None or not isinstance(document,dict):
			return None
		obj_id = document['_id']
		image = None
		if 'image' in document:
			image = document['image']
		url = None
		if 'url' in document:
			url = document['url']
		datetime = None
		if 'datetime' in document:
			datetime = document['datetime']
		abstract = None
		if 'abstract' in document:
			abstract = document['abstract']
		title = None
		if 'title' in document:
			title = document['title']
		topic = None
		if 'topic' in document:
			topic = document['topic']
		content = None
		if 'content' in document:
			content = document['content']
		type = None
		if 'type' in document:
			type = document['type']
		favorites = None
		if 'favorites' in document:
			favorites = document['favorites']
		comments = None
		if 'comments' in document:
			comments = document['comments']
		# article = Article(object_id=obj_id,image=image,url=url,datetime=datetime,abstract=abstract,title=title,topic=topic,content=content,type=type,favorites=favorites,comments=comments)
		return None #article

	def get_articles(self):
		"""
		Get all articles from db

		:return: The list of articles.

		:rtype: **`json`**
		"""
		if self.__client == None:
			self.__connect__()
		collection = self.__client.get_collection(self.__dbname,self.__collection_name)
		articles = []
		for document in collection.find():
			article = self.__parse_article(document=document)
			articles.append(article)
		return articles

	def get_articles_by_topic(self,topic):
		"""
		Get all articles with the specified topic

		:param topic: the topic to search article (that an article belongs to)

		:return: The list of articles.

		:rtype: **`json`**

		"""
		articles = []
		if self.__client ==None:
			self.__connect__()
			documents = self.__client.get_documents(dbname=self.__dbname, colname=self.__collection_name,filter_text={'topic':topic})
			for document in documents:
				article = self.__parse_article(document=document)
				articles.append(article)
		return articles