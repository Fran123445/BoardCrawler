import pyodbc
from abc import ABC, abstractmethod

class Loader(ABC):

    def __init__(self, conn: pyodbc.Connection):
        self.conn = conn

    @abstractmethod
    def bulk_load(self, data_list: list):
        pass