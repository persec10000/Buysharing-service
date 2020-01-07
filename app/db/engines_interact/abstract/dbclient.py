import abc
from abc import ABC


class DbClient(ABC):
    """
    The settings class to interact with database.

    """

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def select(self, table=None, query = None):
        """Return a datatable from database. (perform `select` sql command)

        :param table: The name of table.

        :param query: The query to perform.

        :return: The tuple of row data (equivalent to datatable).
        """
        pass

    @abc.abstractmethod
    def update(self, query = None):
        """Perform insert, update, delete query.

        :param query: The query to perform.

        :return: True if success and False vise-versa.
        """
        pass