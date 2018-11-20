from pymongo import MongoClient
from .settings import MONGO_URL


class Services:
    def __init__(self):
        self.__mongo = None
        self.__ftp = None

    @property
    def mongo(self):
        return MongoClient(MONGO_URL)


services = Services()
