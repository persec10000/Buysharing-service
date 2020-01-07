import pypyodbc as pyodbc
import contextlib
from ....settings.parameters import SqlConnectionParameter, FileFolderParameters

SqlParameters = SqlConnectionParameter.MSSQLParameters


class BulkUpdate:
    _driver = SqlParameters.driver
    _db_host = SqlParameters.server
    _db_name = SqlParameters.database
    _db_user = SqlParameters.uid
    _db_password = SqlParameters.pwd
    _connection_string = None

    _sql_parameters = None

    def __init__(self, db_name=None):
        if db_name is not None:
            self._db_name = db_name
        self._init_connection_string()

    def _init_connection_string(self):
        self._connection_string = 'Driver=' + self._driver + ';Server=' + self._db_host + ';Database=' + self._db_name + ';UID=' + self._db_user + ';PWD=' + self._db_password + ';'

    def mytest(self):
        try:
            db = pyodbc.connect(self._connection_string)
            # SQL = 'CREATE TABLE saleout (id int PRIMARY KEY,product_name VARCHAR(25));'
            SQL = "SELECT * FROM MOFA1_A9_Data"
            cursor = db.cursor()
            cursor.execute(SQL)
            # Method 1, simple reading using cursor
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                print(row)
            db.cursor().close()
            db.close()
        except Exception as e:
            print(e.__str__())

    def bulk_insert(self, table_name, file_path, first_row=None):
        if not first_row:
            first_row = 3
        from ....settings.parameters import CsvParameters
        field_terminator = CsvParameters.delimiter
        if not self._connection_string or str(self._connection_string).strip().__eq__(""):
            self._init_connection_string()
        string = "BULK INSERT {} FROM '{}' WITH  (FORMAT = 'CSV',  FIRSTROW = "+str(first_row)+", FIELDTERMINATOR ='"+field_terminator+"', ROWTERMINATOR ='\n');"
        with contextlib.closing(pyodbc.connect(connectString=self._connection_string)) as conn:
            with contextlib.closing(conn.cursor()) as cursor:
                cursor.execute(string.format(table_name, file_path))
            conn.commit()
            # conn.close()

# import os
# table_name = "MOFA1_ST8_Data"
# file_path = os.path.join(FileFolderParameters.ZIP_FOLDER_NAME, "Digi4_20180906_045310/MOFA1_ST8_Data.csv")
#
# def run():
#     bulk_insert(table_name=table_name, file_path=file_path)
#
# if __name__ == '__main__':
#     # mytest()
#     bulk_insert(table_name=table_name, file_path=file_path)
