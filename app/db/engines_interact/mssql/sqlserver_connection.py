import pyodbc

from ....settings.parameters import SqlConnectionParameter
SqlConnectionParameter = SqlConnectionParameter.MSSQLParameters


# print(pyodbc.drivers())


def open_connection():
    conn = pyodbc.connect(
        r'DRIVER=' + SqlConnectionParameter.driver + ';'
                                                      r'SERVER=' + SqlConnectionParameter.server + ';'
                                                                                                   r'DATABASE=' + SqlConnectionParameter.database + ';'
                                                                                                                                                    r'UID=' + SqlConnectionParameter.uid + ';'
                                                                                                                                                                                           r'PWD=' + SqlConnectionParameter.pwd + ';'
    )
    return conn

def select(conn, command):
    if not conn or not command:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(command)
        row = cursor.fetchone()
        # print(row)
        return row
    except:
        return None

conn = open_connection()
if conn:
    print("Connect successful")
    row = select(conn=conn, command='Select * From People')
    print(row)
else:
    print("Can not connect")

