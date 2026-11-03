
import json
import os

from dataclasses import asdict, is_dataclass
from typing import Generic, Optional, Type, TypeVar

# om type t te gebruiken in python moet je de type en typevar hebben om zo type t aan te maken.
# optional geeft aan dat iets ook none zou kennen zijn.

T = TypeVar("T")


class GenericRepository(Generic[T]):

    def __init__(self, file_path: str, data: list[T], key_fields: tuple = ("id",), debug: bool = False):
        self.file_path = file_path
        self.data = data
        self.key_fields = key_fields
        # stel je moet net als bij inventory zoeken op item_id en location_id dan noem je dat een composite key.
        self.debug = debug

        # hierdoor niet constant opnieuw de code te openen, gewoon 1x bij het aanroepen, 
        # deze kan e dan gwn meteen pakkeb bij de all en dan hoef je het niet opnieuw af te lezen en aan te roepen, cashings onderdeel.  

    
    def _get_field(self, item: T, field: str):
        if isinstance(item, dict):
            return item.get(field)

        return getattr(item, field, None)


    # of object hoort bij meegegevenn id
    def _matches(self, item: T, key_values: tuple) -> bool:
        for index, field in enumerate(self.key_fields):
            if self._get_field(item, field) != key_values[index]:
                return False

        return True


#
    def get_all(self) -> list[T]:
        return self.data 



    def get_by_id(self, *key_values) -> T | None: # *key_values is dus alle items van de tupple mochten het er dus 1 zijn die afhankelijk is van 2 id's 
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        for item in self.data:
            if self._matches(item, key_values):
                return item

        return None

    
    def insert(self, item: T) -> T:
        key_values = tuple(
            self._get_field(item, field)
            for field in self.key_fields
        )

        if self.get_by_id(*key_values) is not None:
            raise ValueError("An item with this key already exists.")

        self.data.append(item) # item word dus toegevoegd aan de list van producten
        self.save()

        return item



    def update(self, *key_values, item: T) -> T | None:
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
            if isinstance(item, dict):
                records.append(item)

            elif is_dataclass(item) and not isinstance(item, type):
                records.append(asdict(item))

            elif hasattr(item, "__dict__"):
                records.append(item.__dict__)

            else:
                raise TypeError("Item cannot be converted to JSON.")

        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, default=str)

        if self.debug:
            print(f"Saved data to {self.file_path}")
