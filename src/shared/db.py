from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class DB:
    __mongo_client: MongoClient
    _db: Database

    def __init__(self):
        print("Setting MongoDB client...")
        self.__mongo_client = MongoClient(getenv("MONGODB_SERVER_URI"))
        print("Database is connected.")
        self._db = self.__mongo_client[getenv("MONGODB_DBNAME")]
