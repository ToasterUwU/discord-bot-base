import datetime
import os
import re
import uuid
from collections import UserDict
from functools import reduce
from typing import Any, Callable, Dict, List, Literal, Optional

import orjson

__all__ = ["CONFIG", "JsonDictSaver"]

if not os.path.isdir("data"):
    os.mkdir("data")


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
    """
    Note: If you enter a dataclass, you manually have to convert it from type dict after loading.
    """

    _supported_key_types = [
        str,
        int,
        float,
        bool,
        type(None),
        datetime.datetime,
        datetime.date,
        datetime.time,
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
        uuid.UUID,
        object,
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
            with open(self.filename, "w+", encoding="utf-8") as f:
                f.write(orjson.dumps(default, option=self.orjson_option).decode())

            if func_if_default:
                func_if_default()

        with open(self.filename, "r", encoding="utf-8") as f:
            data = orjson.loads(f.read())

        self.data = self._convert_data_to_correct_types(data)

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
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(orjson.dumps(self.data, option=self.orjson_option).decode())

    def _convert_single_value_to_correct_type(self, val):
        if isinstance(val, str):
            if val.isnumeric():
                val = int(val)

            elif val.replace(".", "").isnumeric() and val.count(".") == 1:
                val = float(val)

            elif val == "true":
                val = True

            elif val == "false":
                val = False

            elif val == "null":
                val = None

            elif re.match(r"\d{1,4}-\d{1,2}-\d{1,4}T\d{1,2}:\d{1,2}:\d{1,2}", val):
                val = datetime.datetime.fromisoformat(val)

            elif re.match(r"\d{1,4}-\d{1,2}-\d{1,4}", val):
                val = datetime.date.fromisoformat(val)

            elif re.match(r"\d{1,2}:\d{1,2}:\d{1,2}", val):
                val = datetime.time.fromisoformat(val)

            elif re.match(
                r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
                val,
            ):
                val = uuid.UUID("{" f"{val}" "}")

        return val

    def _convert_data_to_correct_types(self, data: dict):
        new_data = {}

        for key, sub_data in data.items():
            if isinstance(sub_data, dict):
                sub_data = self._convert_data_to_correct_types(sub_data)
            else:
                sub_data = self._convert_single_value_to_correct_type(sub_data)

            new_data[self._convert_single_value_to_correct_type(key)] = sub_data

        return new_data


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
