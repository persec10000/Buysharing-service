import logging

from ...engines_interact.abstract.dbhelper import DBHelper
from ...engines_interact.mysql.mysql import MySqlClient
from ...helper.sqlstringcommand import SqlStringCommand
# from models.entity import User

logger = logging.getLogger(__name__)

class DbHelperMySQLUser(DBHelper):
    """
    DbHelperUser helps to work with mongo database easier.
	In this class including following functions:

	1. Get all users from database

	2. Save user to database.

	3. Update user's field.

	4. Delete user or user's field.
    """

    def __init__(self):
        super().__init__()
        self._dbclient = MySqlClient()

    def __parse_user(self, datarow):
        # if not datarow is tuple:
        #     return None
        id = datarow[0]
        user_number = datarow[1]
        first_name = datarow[2]
        last_name = datarow[3]
        birthady = datarow[4]
        about = datarow[5]
        image = datarow[6]
        active = datarow[7]
        email = datarow[8]
        mobile = datarow[9]
        create_date = datarow[10]
        last_change_time = datarow[11]
        sex = datarow[12]
        user_name = datarow[13]
        password = datarow[14]
        group_id = datarow[15]
        delete = datarow[16]
        # user = User(id, user_number, fname=first_name, lname=last_name,bday= birthady,about=about,image=image, active=active,email=email,mobile=mobile, create_date=create_date, last_change_time=last_change_time, sex=sex, user_name=user_name, password=password, group_id=group_id, delete = delete)
        # return user


    def get_users(self):
        table = 'marie.user'
        query = "SELECT id, user_number, first_name, last_name, birthday, about, image, active, email, mobile, create_date, last_change_time, sex, user_name, password, group_id, deleted FROM "+table
        datatable = self._dbclient.select(query=query)
        users = list()
        for i in range(len(datatable)):
            datarow = datatable[i]
            user = self.__parse_user(datarow=datarow)
            users.append(user)
        return users


    def get_user_by_userid(self,userid):
        users = self.get_users()
        user = None
        for i in range(len(users)):
            u = users[i]
            if u.user_id == userid:
                user = u
                break
        return user

    def add_user(self, user):
        data = user.user_to_dict()
        query = SqlStringCommand.sql_string_insert_command(tablename='user',data=data)
        if not self._dbclient.update(query=query):
            logger.log("Could not insert user {"+user.__dict__+"} to database")


    def save_user(self, user):
        pass

    def update_user_field(self, id_field, id_value, field_name, field_value):
        pass

    def get_user_field(self, id_field, id_value, field_name):
        pass
    
    def delete_user_by_id(self, id_field, id_value):
        pass
