from abc import ABC


class DBHelper(ABC):
    """
    This class manages interation with DBClient and get data to return to controllers
    """

    _dbclient = None

    def __init__(self):
        pass
