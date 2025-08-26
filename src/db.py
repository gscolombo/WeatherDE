from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class DB:
    __mongo_client: MongoClient
    _db: Database

    def __init__(self):
        self.__mongo_client = MongoClient(getenv("MONGODB_SERVER_URI"))
        self._db = self.__mongo_client[getenv("MONGODB_DBNAME")]
