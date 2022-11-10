import datetime
import enum
import os
import uuid
from collections import UserDict
from dataclasses import dataclass
from functools import reduce
from typing import Any, Callable, Dict, List, Literal, Optional

import orjson

__all__ = ["CONFIG", "JsonDictSaver"]


class Config(UserDict):
    def __init__(self, categories: Dict[str, "JsonDictSaver"] = {}):
        super().__init__()

        for k, v in categories.items():
            if not isinstance(k, str) or not isinstance(v, JsonDictSaver):
                raise TypeError(
                    "Key needs to be str and item needs to be JsonDictSaver"
                )

            self[k] = v

        self.save()

    def __setitem__(self, key: str, item: "JsonDictSaver") -> None:
        if not isinstance(key, str) or not isinstance(item, JsonDictSaver):
            raise TypeError("Key needs to be str and item needs to be JsonDictSaver")

        return super().__setitem__(key, item)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    def save(self):
        for jds in self.values():
            jds.save()


class JsonDictSaver(UserDict):
    _supported_key_types = [
        str,
        int,
        float,
        bool,
        type(None),
        datetime.datetime,
        datetime.date,
        datetime.time,
        enum.Enum,
        uuid.UUID,
    ]
    _supported_value_types = [
        list,
        dict,
        str,
        int,
        float,
        bool,
        type(None),
        datetime.datetime,
        datetime.date,
        datetime.time,
        enum.Enum,
        uuid.UUID,
        type(dataclass),
    ]

    def __init__(
        self,
        name: str,
        default: dict = {},
        func_if_default: Optional[Callable] = None,
        data_type: Literal["data", "config", "config/default"] = "data",
        orjson_flags: List[int] = [orjson.OPT_INDENT_2],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.filename = f"{data_type}/{name}.json"

        orjson_flags.extend(
            [
                orjson.OPT_NON_STR_KEYS,
            ]
        )
        self.orjson_option = reduce(
            lambda x, y: x | y, orjson_flags
        )  # Bitwise OR for every flag

        if not os.path.exists(self.filename):
            with open(self.filename, "w+") as f:
                f.write(orjson.dumps(default, option=self.orjson_option).decode())

            if func_if_default:
                func_if_default()

        with open(self.filename, "r") as f:
            self.data = orjson.loads(f.read())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    def __setitem__(self, key: Any, item: Any) -> None:
        if not any([isinstance(key, c) for c in self._supported_key_types]):
            raise TypeError(f"Key value '{key}' ({type(key)}) is not supported")

        if not any([isinstance(item, c) for c in self._supported_value_types]):
            raise TypeError(f"Item value '{item}' ({type(item)}) is not supported")

        return super().__setitem__(key, item)

    def save(self):
        with open(self.filename, "w") as f:
            f.write(orjson.dumps(self.data, option=self.orjson_option).decode())


categories = {}
for entry in os.scandir("config/default/"):
    if entry.is_file():
        category_name = entry.name.replace(".json", "")

        default = JsonDictSaver(category_name, data_type="config/default")
        conf = JsonDictSaver(category_name, data_type="config")

        for k, v in default.items():
            if k not in conf:
                conf[k] = v

        conf.save()
        categories[category_name] = conf

        del default

CONFIG = Config(categories)

del categories
