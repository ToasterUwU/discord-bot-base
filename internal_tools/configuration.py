import json
import os
from collections import UserDict
from typing import Callable


class JsonDataSaver(UserDict):
    def __init__(
        self, name: str, default={}, func_if_default: Callable = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.filename = f"{name}.json"
        if not os.path.exists(self.filename):
            with open(self.filename, "w+") as f:
                json.dump(default, f, indent=4)
            if func_if_default:
                func_if_default()

        with open(self.filename, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)


def _inform_and_exit():
    print("Config generated, please edit the new config.json file.")
    exit()


with open("_base_config.json", "r") as f:
    default_config = json.load(f)

CONFIG = JsonDataSaver(
    "config", default=default_config, func_if_default=_inform_and_exit
)
