"""
connect(parameters...)
Constructor for creating a connection to the database. Returns a Connection Object. Parameters are the same as for the MySQL C API. In addition, there are a few additional keywords that correspond to what you would pass mysql_options() before connecting. Note that some parameters must be specified as keyword arguments! The default value for each parameter is NULL or zero, as appropriate. Consult the MySQL documentation for more details. The important parameters are:

host
name of host to connect to. Default: use the local host via a UNIX socket (where applicable)
user
user to authenticate as. Default: current effective user.
passwd
password to authenticate with. Default: no password.
db
database to use. Default: no default database.
port
TCP port of MySQL server. Default: standard port (3306).
unix_socket
location of UNIX socket. Default: use default location or TCP for remote hosts.
conv
type conversion dictionary. Default: a copy of MySQLdb.converters.conversions
compress
Enable protocol compression. Default: no compression.
connect_timeout
Abort if connect is not completed within given number of seconds. Default: no timeout (?)
named_pipe
Use a named pipe (Windows). Default: don’t.
init_command
Initial command to issue to server upon connection. Default: Nothing.
read_default_file
MySQL configuration file to read; see the MySQL documentation for mysql_options().
read_default_group
Default group to read; see the MySQL documentation for mysql_options().
cursorclass
cursor class that cursor() uses, unless overridden. Default: MySQLdb.cursors.Cursor. This must be a keyword parameter.
use_unicode
If True, CHAR and VARCHAR and TEXT columns are returned as Unicode strings, using the configured character set. It is best to set the default encoding in the server configuration, or client configuration (read with read_default_file). If you change the character set after connecting (MySQL-4.1 and later), you’ll need to put the correct character set name in connection.charset.

If False, text-like columns are returned as normal strings, but you can always write Unicode strings.

This must be a keyword parameter.

charset
If present, the connection character set will be changed to this character set, if they are not equal. Support for changing the character set requires MySQL-4.1 and later server; if the server is too old, UnsupportedError will be raised. This option implies use_unicode=True, but you can override this with use_unicode=False, though you probably shouldn’t.

If not present, the default character set is used.

This must be a keyword parameter.

sql_mode
If present, the session SQL mode will be set to the given string. For more information on sql_mode, see the MySQL documentation. Only available for 4.1 and newer servers.

If not present, the session SQL mode will be unchanged.

This must be a keyword parameter.

ssl
This parameter takes a dictionary or mapping, where the keys are parameter names used by the mysql_ssl_set MySQL C API call. If this is set, it initiates an SSL connection to the server; if there is no SSL support in the client, an exception is raised. This must be a keyword parameter.
apilevel
String constant stating the supported DB API level. ‘2.0’
"""

import pymysql as mydb

from ...engines_interact.abstract.dbclient import DbClient

try:
    from ....settings.parameters import DatabaseParameters
    dbinfo = DatabaseParameters.DB_INFO
except:
    dbinfo = None


class MySqlClient(DbClient):
    """
    This class commnunicates with mysql database to get raw data (datatable) or performs the following actions: update, delete.
    """

    _db_host = None
    _db_port = None
    _db_user = None
    _db_pass = None

    _db_name = None
    _db_table = None
    _client = None

    def __init__(self):  # , db_host = None, db_port = None, db_user = None, db_pass = None, db_table= None):
        if dbinfo == None:
            raise Exception('Parameter must not be null')
        else:
            self.__load_db_info()
        self._connect()

    def __load_db_info(self):
        self._db_host = dbinfo['DB_HOST']
        self._db_port = dbinfo['DB_PORT']
        self._db_user = dbinfo['DB_USER']
        self._db_pass = dbinfo['DB_PASS']
        self._db_name = dbinfo['DB_NAME']
        self._db_table = dbinfo['DB_TABLE']

    def _connect(self):
        self._client = mydb.connect(host=self._db_host, user=self._db_user, port=self._db_port, password=self._db_pass,
                                    db=self._db_name)

    def select(self, table=None, query=None):
        """ Return datatable (data) from `table_name'.

        This will return a tuple of data. And we need to handle this tuple.

        :param table: The table name

        :param query: The sql query.

        :return: The datatable. ([see more](https://dev.mysql.com/doc/refman/5.7/en/selecting-all.html))
        """
        if table == None and query == None:
            return None
        elif table != None:
            query = 'SELECT * FROM ' + str(table)
        else:
            pass
        try:
            if self._client == None:
                self._connect()
            # conn = mydb.connect(user='root', port = self.__db_port, host = self.__db_host, db = self.__db_name)
            # cur = conn.cursor()
            cur = self._client.cursor()
            cur.execute(query)  # = rows
            # print(cur.fetchall())
            datatable = cur.fetchall()
            return datatable
            # return True
        except Exception as e:
            print(e.__str__())
            return None
        finally:
            self._client = None

    def update(self, query=None):
        """Run SQL commands like: insert, update, delete

        :param query: The SQL query

        :return: The result of handling process.

        :rtype: [boolean] True: The command was executed successfully.

        :rtype: [boolean] False: The command was executed unsuccessfully.
        """
        if str(query).__eq__(''):
            return
        else:
            if self._client == None:
                self._connect()
            try:
                cursor = self._client.cursor()
                cursor.execute(query)
                # cursor.commit()
                self._client.commit()
                return True
            except Exception as e:
                print(e.__str__())
                return False
            finally:
                self._client = None

    def _delete(self):
        pass


# def select_test():
#     client = MySqlClient()
#     datatable = client.select(table='support')
#     for i in range(len(datatable)):
#         row = datatable[i]
#         id = row[0]
#         title = row[1]
#         print(id, title)
#         print(row)
#     # import pprint
#     # pprint.pprint(datatable)
#
# #
# # def test_insert():
# #     # query = SqlStringCommand.sql_string_select_command(tablename='test', condition='')
# #     data = dict()
# #     data['surname'] = 'abd'
# #     data['lastname'] = 'def'
# #     data['birthday'] = '21/06/1987'
# #     query = SqlStringCommand.sql_string_insert_command(tablename='test', data=data)
# #     client = MySqlClient()
# #     if client.update(query=query):
# #         print('Update successfully')
# #     else:
# #         print('Could not update. Check again')
# #         # pass
# #
# #
# # def test_update():
# #     data = dict()
# #     user_id = 5
# #     data['surname'] = 'Van A'
# #     data['lastname'] = 'Nguyen'
# #     data['birthday'] = '21/06/1987'
# #     query = SqlStringCommand.sql_string_update_command(tablename='test', field_name='user_id', field_value=user_id,
# #                                                        data=data)
# #     client = MySqlClient()
# #     if client.update(query=query):
# #         print("Update successfully")
# #     else:
# #         print("Could not be updated")
# #
# #
# # def test_delete():
# #     user_id = 8
# #     query = SqlStringCommand.sql_string_delete_command(tablename='test', field_name='user_id', field_value=user_id)
# #     client = MySqlClient()
# #     if client.update(query=query):
# #         print("Delete successfully")
# #     else:
# #         print("Delete unsuccessfully")
# #
# #
#
# def run():
#     print("Test select\n")
#     select_test()
#     # print("Test Insert")
#     # # test_insert()
#     # # test_select()
#     # print("Test update")
#     # # test_update()
#     # # test_select()
#     # print("Test delete")
#     # test_delete()
#     # test_select()
#
#
# if __name__ == '__main__':
#     run()
