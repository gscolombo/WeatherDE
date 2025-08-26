from pymongo.collection import Collection
from typing import Iterable, Callable

from shared.db import DB


class _Collection(DB):
    name: str
    collection: Collection

    def __init__(self, name, db: DB = None, **kwargs):
        self.name = name
        if db is None:
            super().__init__()  # Initialize new instance of DB
        else:
            self._db = db._db

        if not name in self._db.list_collection_names():
            print(f"Creating collection {name}...")
            self.collection = self._db.create_collection(name, **kwargs)
            print("Collection created successfully!")
            return

        print(f"Retrieving collection {name}")
        self.collection = self._db.get_collection(name)

    def insert(self, data: Iterable, m: Callable):
        print("Inserting new data...")
        return self.collection.insert_many([
            m(**entry) for entry in data
        ])
