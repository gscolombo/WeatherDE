from shared.db import DB


class View(DB):
    __collections: list[str]

    def __init__(self):
        super().__init__()
        print("Retrieving list of collections...")
        self.__collections = self._db.list_collection_names()

    def create_view(self, name: str, on: str, pipeline: list, replace=False):
        command = "create" if not replace else "collMod"
        print(f"{"Creating" if not replace else "Replacing"} view {name} on {on}...")
        return self._db.command({
            command: name,
            "viewOn": on,
            "pipeline": pipeline
        })

    def view_exists(self, name: str):
        return name in self.__collections
