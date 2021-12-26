import json
import os
from collections import UserDict


class JsonDataSaver(UserDict):
    def __init__(self, name: str, __dict=..., **kwargs) -> None:
        super().__init__(__dict=__dict, **kwargs)
        self.filename = f"{name}.json"
        if not os.path.exists(self.filename):
            with open(self.filename, "w+") as f:
                f.write("{}")

        with open(self.filename, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def __del__(self):
        self.save()


CONFIG = JsonDataSaver("config")
