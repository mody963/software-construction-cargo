
import json
import os

from dataclasses import asdict, is_dataclass
from typing import Generic, Optional, Type, TypeVar
# om type t te gebruiken in python moet je de type en typevar hebben om zo type t aan te maken. 
# optional geeft aan dat iets ook none zou kennen zijn. 

T = TypeVar("T")


class GenericRepository(Generic[T]):

    def __init__(self, file_path: str, model: Type[T], key_fields: tuple = ("id",), debug: bool = False):
        self.file_path = file_path
        self.model = model
        self.key_fields = key_fields # stel je moet net als bij inventory zoeken op item_id en locaion_id dan noem je dat een composite key. 
        self.debug = debug

        self.data = self.load()

    def load(self) -> list[T]:
        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            records = json.load(file)

        return [self.model(**record) for record in records]

    def get_all(self) -> list[T]:
        return self.data

    def get_by_id(self, *key_values) -> Optional[T]:
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        for item in self.data:
            if self._matches(item, key_values):
                return item

        return None

    def insert(self, item: T) -> T:
        key_values = self._get_key_values(item)

        if self.get_by_id(*key_values) is not None:
            raise ValueError("An item with this key already exists.")

        self.data.append(item)
        self.save()

        return item

    def update(self, *key_values, item: T) -> Optional[T]:
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        for index, existing_item in enumerate(self.data):
            if self._matches(existing_item, key_values):
                self.data[index] = item
                self.save()

                return item

        return None

    def delete(self, *key_values) -> bool:
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        for index, existing_item in enumerate(self.data):
            if self._matches(existing_item, key_values):
                del self.data[index]
                self.save()

                return True

        return False

    def save(self):
        records = []

        for item in self.data:
            if is_dataclass(item):
                records.append(asdict(item))
            elif hasattr(item, "__dict__"):
                records.append(item.__dict__)
            else:
                raise TypeError(
                    f"Model {self.model.__name__} cannot be converted to JSON."
                )

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, default=str)

        if self.debug:
            print(f"Saved data to {self.file_path}")

    def _matches(self, item: T, key_values: tuple) -> bool:
        for index, field in enumerate(self.key_fields):
            if getattr(item, field, None) != key_values[index]:
                return False

        return True

    def _get_key_values(self, item: T) -> tuple:
        return tuple(
            getattr(item, field)
            for field in self.key_fields
        )
