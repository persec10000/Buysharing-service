from ..engines_interact.mssql import mssql
from ...settings.parameters import SqlConnectionParameter, DatabaseParameters

sql_parameters = SqlConnectionParameter.MSSQLParameters()
sql_parameters.database = sql_parameters.database_digi
_mofa = mssql.MsSQLClient(sql_parameter=sql_parameters)

_dbo_tables = ['Item Ledger Entry Type', 'Prod Lot Ouput', '[Item Ledger Entry Type]', '[Prod Lot Ouput]']

DIGI_TABLES = DatabaseParameters.DIGI_TABLES
MOFA_TABLES = DatabaseParameters.MOFA_TABLES


def get_all_tables():
    _mofa_tables = list()
    sql_str = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
    dt = _mofa.select(query=sql_str)
    if not dt:
        return
    for i in range(len(dt)):
        row = dt[i]
        table_name = row[0]
        _mofa_tables.append(table_name)
    return _mofa_tables


def read_data(tablename):
    if not tablename in DIGI_TABLES:
        return None
    if ' ' in tablename and tablename in _dbo_tables:
        tablename = "[" + tablename + "]"
    elif ' ' in tablename and not tablename in _dbo_tables:
        tablename = "NAV." +"[" + tablename + "]"
    elif not ' ' in tablename and not tablename in _dbo_tables:
        tablename = "NAV." + tablename
    try:
        data = _mofa.select_to_data_frame(table=tablename)
    except Exception as e:
        data = None
        print(e.__str__())
    return data


def run():
    tables = get_all_tables()
    print(len(tables))
    for table in tables:
        data = read_data(tablename=table)
        if data is None:
            continue
        print(table, type(data), len(data))


if __name__ == '__main__':
    run()
