import logging

from ..abstract.dbhelper import DBHelper
from .mongo import MongoDBClient
# from models.entity import User

logger = logging.getLogger(__name__)

try:
    from ....settings.parameters import DatabaseParameters

    DB_INFO = DatabaseParameters.DB_INFO
except:
    DB_INFO = None


class DbHelperUserMongo(DBHelper):
    """
    DbHelperUser helps to work with mongo database easier.
    In this class including following functions:

    1. Get all users from database

    2. Save user to database.

    3. Update user's field.

    4. Delete user or user's field.

    """
    __dbname = 'chatbot'  # database name
    __collection_name = 'users'
    # __host = '46.101.137.23'  # host
    __host = 'localhost'
    __port = 27017  # host
    __client = None  # the instance of MongoDBHelper

    __fields = (
        '_id', 'token', 'id', 'name', 'lname', 'bday', 'about', 'image', 'verified', "height", 'weight',
        'temp_location', 'location_city', 'location_temp_city', 'location_plz', "allergies", "sports", 'sex',
        'interests', 'positions', 'location_gps', 'age', 'bmi', 'profiling', 'allergies_notify')

    def __init__(self):  # , host=None, port=None, dbname=None, colname=None):
        """
        The constructor of DBHelperUser.
        """
        super().__init__()
        if DB_INFO != None:
            try:
                self.__host = DB_INFO['DB_HOST']
                port = DB_INFO['DB_PORT']
                if not isinstance(port, int):
                    port = int(port)
                self.__port = port  # DB_INFO['DB_PORT']
                self.__dbname = DB_INFO['DB_NAME']
                self.__collection_name = DB_INFO['DB_COLLECTION_NAME']
            except:
                logger.log("Can not parse db parameters, check it again in setting file.")
                self.__assign_db_info_default()
        else:
            self.__assign_db_info_default()
        self.__connect__()

    def __assign_db_info_default(self):
        self.__host = 'localhost'
        self.__port = 27017
        self.__dbname = 'chatbot'
        self.__collection_name = 'users'

    # connect to DB
    def __connect__(self):
        self.__client = MongoDBClient(self.__host, self.__port)

    # close the connection
    def __disconnect__(self):
        self.__client = None

    def __parse_user(self, document):
        """
        Parses document (form of mongo database record) to user object.

        :param document: The document that gets from database.

        :return: The user object.

        :rtype: **`json`**

        """
        if document == None:
            return None
        obj_id = document['_id']
        user_id = document['id']
        token = None
        if 'token' in document:
            token = document['token']
        name = document['name']
        lname = document['lname']
        bday = None
        if 'bday' in document:
            bday = document['bday']
        about = None
        if 'about' in document:
            about = document['about']
        image = None
        if 'image' in document:
            image = document['image']
        verified = None
        if 'verified' in document:
            verified = document['verified']
        height = None
        if 'height' in document:
            height = document['height']
        weight = None
        if 'weight' in document:
            weight = document['weight']
        temp_loc = None
        if 'temp_location' in document:
            temp_loc = document['temp_location']
        location_city = None
        if 'location_city' in document:
            location_city = document['location_city']
        location_temp_city = None
        if 'location_temp_city' in document:
            location_temp_city = document['location_temp_city']
        location_plz = None
        if 'location_plz' in document:
            location_plz = document['location_plz']
        allergies = None
        if 'allergies' in document:
            allergies = document['allergies']
        sports = None
        if 'sports' in document:
            sports = document['sports']
        sex = None
        if 'sex' in document:
            sex = document['sex']
        interests = None
        if 'interests' in document:
            interests = document['interests']
        positions = None
        if 'positions' in document:
            positions = document['positions']
        location_gps = None
        if 'location_gps' in document:
            location_gps = document['location_gps']
        age = None
        if 'age' in document:
            age = document['age']
        bmi = None
        if 'bmi' in document:
            bmi = document['bmi']
        profiling = None
        if 'profiling' in document:
            profiling = document['profiling']
        allergies_notify = None
        if 'allergies_notify' in document:
            allergies_notify = document['allergies_notify']

        # user = User(objid=obj_id, id=user_id, token=token, fname=name, lname=lname, bday=bday, about=about,
        #             image=image, verified=verified, height=height, weight=weight, temp_lo=temp_loc,
        #             location_city=location_city, location_temp_city=location_temp_city, location_plz=location_plz,
        #             allergies=allergies, sports=sports, sex=sex, interests=interests, positions=positions,
        #             location_gps=location_gps, age=age, bmi=bmi, profiling=profiling, allergies_notify=allergies_notify)
        # return user

    def get_users(self):
        """
        Gets all users from db.

        :return: The list of users in db.

        """
        if self.__client == None:
            self.__connect__()
        collection = self.__client.get_collection(self.__dbname, self.__collection_name)
        users = []
        for document in collection.find():
            user = self.__parse_user(document=document)
            users.append(user)
        return users

    def get_user_by_userid(self, userid):
        """
        Gets user from db by user_id.

        :param userid: the user id.

        :return: the user.
        """
        res_user = None
        try:
            if self.__client == None:
                self.__connect__()
            document = self.__client.get_document(dbname=self.__dbname, colname=self.__collection_name,
                                                  filter_text={'id': userid})
            res_user = self.__parse_user(document=document)
        except IOError as error:
            print(error)
        finally:
            self.__disconnect__()
        return res_user

    def add_user(self, user):
        """
        Add new user to the collection in db.

        :param user: the user object to add to database.

        :return: The result of adding process.
        """
        # if isinstance(user, User):
        #     document = user.__dict__
        #     if self.__client == None:
        #         self.__connect__()
        #     self.__client.insert_document(self.__dbname, self.__collection_name, document=document)
        return

    def save_user(self, user):
        """
        Save all user's changes into db.

        :param user: The user that need to save changes.

        :return: The result of updating process.

        """
        obj_id = user.object_id
        if self.__client == None:
            self.__connect__()
        for field in self.__fields:
            if field != '_id':
                self.update_user_field('_id', obj_id, field_name=field, field_value=user.__dict__[field])
        # self.update_user_field('_id', obj_id, field_name=field, field_value=user.__dict__[field])
        # self.__client.update_document_by_id(dbname=self.__dbname, collection=self.__collection_name,id_value=obj_id, field_name=field, field_value=user.__dict__[field])

    def update_user_field(self, id_field, id_value, field_name, field_value):
        """
        Update any field in database.

        :param id_field: The id_field to define a document

        :param id_value: The id_value

        :param field_name:	The field_name that need to be updated

        :param field_value: The new field value

        :return: The result of updating process.
        """
        if self.__client == None:
            self.__connect__()
        self.__client.update_document(dbname=self.__dbname, collection=self.__collection_name, id_field=id_field,
                                      id_value=id_value, field_name=field_name, field_value=field_value)

    def get_user_field(self, id_field, id_value, field_name):
        """
        Get value of the specified field name.

        :param id_field: The id field to define a document

        :param id_value: The id value of id field

        :param field_name: The field name that we need to get the value

        :return: The result of updating process.
        """
        if self.__client == None:
            self.__connect__()
        document = self.__client.get_document(dbname=self.__dbname, colname=self.__collection_name,
                                              filter_text={id_field: id_value})
        res = document[field_name]
        return res

    def delete_user_by_id(self, id_field, id_value):
        """
        Delete the document (user) by any identified field.

        :param id_field: The identified field.

        :param id_value: The value of the identified field.

        :return: The result of updating process.
        """
        if self.__client == None:
            self.__connect__()
        self.__client.remove_document(self.__dbname, self.__collection_name, {id_field: id_value})

# dbhelper = DbHelperUser()
# # user = User(objid=None, id='15',name='noi',lname='nguyen')
# # dbhelper.add_user(user=user)
# users = dbhelper.get_users()
# # print(len(users))
# for user in users:
# 	user.profiling = None
# 	dbhelper.save_user(user=user)
# 	# print(user.__dict__)
# users = dbhelper.get_users()
# # print(len(users))
# for user in users:
# 	print(user.__dict__)

# history = History()
# history.user = user
# history.mesage = "Hello"
# history.save()
# user = dbhelper.get_user_by_userid(userid=69)
# print(user.__dict__)
# dbhelper.delete_user_by_id(id_field='id', id_value=user.id)
# user = dbhelper.get_user_by_userid(userid=390)
# print(user.__dict__)
# user.height='180'
# dbhelper.update_user_field(id_field='id',id_value=user.id, field_name='height', field_value=user.height.__str__())
# user = dbhelper.get_user_by_userid(userid=390)
# print(user.__dict__)


# user_id = 'user123456789'
# user = dbhelper.get_user_by_userid(userid=user_id)
# if user != None:
# 	print(user.to_json())
