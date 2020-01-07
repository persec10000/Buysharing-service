import pyodbc

from ...engines_interact.abstract.dbclient import DbClient
from ....utils import log
import pandas as pd
from pandas import DataFrame


# try:
#     from settings.parameters import SqlConnectionParameter as SqlParameter
#
#     SqlParameter = SqlParameter.MSSQLParameters
# except:
#     SqlParameter = None


class MsSQLClient(DbClient):
    """
    This class makes a connection and manage interaction with MSSQL database.
    """
    _db_server = None
    _db_driver = None
    _db_database = None
    _db_uid = None
    _db_pwd = None
    _sql_parameter = None

    _conn = None

    def __init__(self, sql_parameter):
        if sql_parameter == None:
            raise Exception('Parameter must not be Null')
        else:
            self._sql_parameter = sql_parameter
            self.__load_db_info()
        # self._connect()

    def __load_db_info(self):
        self._db_driver = self._sql_parameter.driver
        self._db_server = self._sql_parameter.server
        self._db_database = self._sql_parameter.database
        self._db_uid = self._sql_parameter.uid
        self._db_pwd = self._sql_parameter.pwd

    def _connect(self):
        self._conn = pyodbc.connect(r'DRIVER=' + self._db_driver + ';'
                                                                   r'SERVER=' + self._db_server + ';'
                                                                                                  r'DATABASE=' + self._db_database + ';'
                                                                                                                                     r'UID=' + self._db_uid + ';'
                                                                                                                                                              r'PWD=' + self._db_pwd + ';')

    def select(self, table=None, query=None):
        """ Return datatable (data) from `table_name'.

               This will return a tuple of data. And we need to handle this tuple.

               :param table: The table name

               :param query: The sql query.

               :return: The datatable.
        """
        if table == None and query == None:
            return None
        elif query is not None:
            pass
        else:
            query = 'SELECT * FROM ' + str(table)

        try:
            if self._conn is None:
                self._connect()
            cursor = self._conn.cursor()
            result = cursor.execute(query)
            if cursor:
                datatable = result.fetchall()
            else:
                datatable = None
            # self._conn.close()
            return datatable
        except Exception as e:
            # log.log_sql_error(content=str(e))
            # print(str(e))
            return None
        finally:
            if self._conn:
                self._conn.close()
                self._conn = None

    def select_to_data_frame(self, table=None, query=None):
        if table == None and query == None:
            return None
        elif query is not None:
            pass
        else:
            query = 'SELECT * FROM ' + str(table)

        try:
            if self._conn is None:
                self._connect()
            df = pd.read_sql(con=self._conn, sql=query)
            return df
            # cursor = self._conn.cursor()
            # result = cursor.execute(query)
            # if cursor:
            #     datatable = result.fetchall()
            #     frame = DataFrame(data=datatable)
            #     frame.columns = result.keys()
            # else:
            #     datatable = None
            #     frame = None
            # # self._conn.close()
            # return frame
        except Exception as e:
            # log.log_sql_error(content=str(e))
            print(str(e))
            return None
        finally:
            if self._conn:
                self._conn.close()
                self._conn = None

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
            if self._conn == None:
                self._connect()
            try:
                cursor = self._conn.cursor()
                count = cursor.execute(query).rowcount
                # cursor.commit()
                self._conn.commit()
                # self._conn.close()
                if count != 0:
                    return True
                else:
                    return False
            except Exception as e:
                # log.log_sql_error(str(e))
                # print(e.__str__())
                return False
            finally:
                if self._conn:
                    self._conn.close()
                    self._conn = None

# def select_test():
#     client = MsSQLClient()
#     datatable = client.select(table='NAV.Feature')
#     for i in range(len(datatable)):
#         row = datatable[i]
#         id = row[0]
#         title = row[1]
#         print(id, title)
#         print(row)
# import pprint
# pprint.pprint(datatable)


# def test_insert():
#     # query = SqlStringCommand.sql_string_select_command(tablename='test', condition='')
#     data = dict()
#     data['Surname'] = 'abd'
#     data['Lastname'] = 'def'
#     data['Birthday'] = '21/06/1987'
#     data['Phone'] = '09876568909'
#     data['Address'] = 'Viet Nam'
#     query = SqlStringCommand.sql_string_insert_command(tablename='People', data=data)
#     client = MsSQLClient()
#     if client.update(query=query):
#         print('Update successfully')
#     else:
#         print('Could not update. Check again')
#         # pass
#
#
# def test_update():
#     data = dict()
#     user_id = 3
#     data['Surname'] = 'Van A'
#     data['Lastname'] = 'Nguyen'
#     data['Birthday'] = '21/06/1987'
#     query = SqlStringCommand.sql_string_update_command(tablename='People', field_name='ID', field_value=user_id,
#                                                        data=data)
#     client = MsSQLClient()
#     if client.update(query=query):
#         print("Update successfully")
#     else:
#         print("Could not be updated")
#
#
# def test_delete():
#     user_id = 3
#     query = SqlStringCommand.sql_string_delete_command(tablename='People', field_name='ID', field_value=user_id)
#     client = MsSQLClient()
#     if client.update(query=query):
#         print("Delete successfully")
#     else:
#         print("Delete unsuccessfully")
#
#
#
# def run():
#     print("Test select\n")
#     select_test()
#     # print("Test Insert")
#     # test_insert()
#     # select_test()
#     # print("Test update")
#     # test_update()
#     # select_test()
#     # print("Test delete")
#     # test_delete()
#     # select_test()
#
#
# if __name__ == '__main__':
#     run()
