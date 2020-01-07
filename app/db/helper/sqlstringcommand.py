from ...utils.checker import Checker


class SqlStringCommand:
    """
    The database utitily helps to prepare SQL queries.
    """

    @staticmethod
    def sql_string_select_command(tablename, condition=None):
        """ Prepare the select command.

        :param tablename: The table name

        :param condition: The condition for filtering in select command.

        :return: The datatable
        """
        if condition != None and not str(condition).__eq__(''):
            return "SELECT * FROM " + tablename
        else:
            return "SELECT * FROM " + tablename + ' ' + condition

    @staticmethod
    def sql_string_insert_command(tablename, data=dict):
        """
        Making a sql query to insert data to database.

        :param tablename: The table name

        :param data: The data in the dictionary format

        :return: The string query.
        """
        if data is None or data.__len__() == 0:
            return ''
        query = """INSERT INTO """ + tablename + """ ("""
        for key in data.keys():
            query += str(key) + ""","""
        query = query[:query.__len__() - 1]
        query += """) VALUES ("""
        for key in data.keys():
            # sittuation to check:
            # if value is binary --> keep
            # if value is number --> keep
            # if value is string --> to unicode
            # if value is datetime --> convert to datetime
            value = data[key]
            if value is None or str(value).upper().__eq__('NAN'):
                continue
            # print(type(value))
            if isinstance(value, str):
                query += """N'""" + str(value) + """',"""
            elif isinstance(value, float):
                query += str(value) + ","
            elif isinstance(value, int):
                query += str(value) + ","
            elif Checker.is_date(str(value)):
                query += """convert(datetime,'""" + str(value) + """',121),"""
            else:
                query += """'""" + str(value) + """',"""
            # if not str(value).isnumeric() and not Checker.is_date(str(value)):
            #
            #     pass
            # else:
            #     pass
        query = query[:query.__len__() - 1]
        query += """)"""
        return query

    @staticmethod
    def sql_string_update_command(tablename, field_name, field_value, data=dict):
        """
        Making SQL query to update data to the database.

        :param tablename: The table name

        :param field_name: The field to update data

        :param field_value: The value to update

        :param data: The data in dictionary format.

        :return:
        """
        if data == None or len(data) == 0:
            return ''
        query = """UPDATE """ + tablename + """ SET """
        for key in data.keys():
            # if str(key).upper().__contains__('ID'):
            #     continue
            value = data[key]
            if value is None or str(value).upper().__eq__('NAN'):
                continue
            # value = str(data[key])
            if isinstance(value, str):
                query += key + "=N'" + str(value) + "',"
            elif isinstance(value, float):
                query += key + "=" + str(value) + ","
            elif isinstance(value, int):
                query += key + "=" + str(value) + ","
            elif Checker.is_date(str(value)):
                query += key + "=convert(datetime,'" + str(value) + "',121),"
            else:
                query += key + "=N'" + str(value) + "',"
        query = query[:query.__len__() - 1]
        query += " WHERE " + field_name + "='" + str(field_value) + "'"
        return query

    @staticmethod
    def sql_string_delete_command(tablename, field_name, field_value):
        query = "DELETE FROM " + tablename + " WHERE " + field_name + "='" + str(field_value) + "'"
        return query
