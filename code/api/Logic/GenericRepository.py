
import json
import os

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from typing import Generic, Optional, Type, TypeVar

# om type t te gebruiken in python moet je de type en typevar hebben om zo type t aan te maken.
# optional geeft aan dat iets ook none zou kennen zijn.

T = TypeVar("T")


class GenericRepository(Generic[T]):

    def __init__(self, file_path: str, model: Type[T], key_fields: tuple[str, ...] = ("id",), debug: bool = False):
        self.file_path = file_path
        self.model = model
        self.key_fields = key_fields
        # stel je moet net als bij inventory zoeken op item_id en location_id dan noem je dat een composite key.("item_id", "location_id")
        self.debug = debug

        self.data: list[T] = self.load()
# hierdoor niet constant opnieuw de code te openen, gewoon 1x bij het aanroepen,
# deze kan e dan gwn meteen pakkeb bij de all en dan hoef je het niet opnieuw af te lezen en aan te roepen, cashings onderdeel.

    def get_timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")



    # of object hoort bij meegegevenn id
    def _matches(self, item: T, key_values: tuple) -> bool:
        for index, field in enumerate(self.key_fields):
            if getattr(item, field, None) != key_values[index]:
                return False

        return True


    def load(self) -> list[T]:
        if self.debug:
            return []

        if not os.path.exists(self.file_path):
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            records: list[dict] = json.load(file)

        return [self.model(**record) for record in records]


#
    def get_all(self) -> list[T]:
        return self.data.copy() # hierbij dus die cashing aangeroepen.



    def get_by_id(self, *key_values) -> Optional[T]: # *key_values is dus alle items van de tupple mochten het er dus 1 zijn die afhankelijk is van 2 id's
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        for item in self.data:
            if self._matches(item, key_values):
                return item

        return None



    def _get_key_values(self, item: T) -> tuple:
        return tuple(
            getattr(item, field)
            for field in self.key_fields
        )


    def insert(self, item: T) -> T:
        key_values = self._get_key_values(item)

        if self.get_by_id(*key_values) is not None:
            raise ValueError("An item with this key already exists.")

        timestamp = self.get_timestamp()

        if hasattr(item, "created_at"):
            setattr(item, "created_at", timestamp)

        if hasattr(item, "updated_at"):
            setattr(item, "updated_at", timestamp)

        self.data.append(item)
        self.save()

        return item



    def update(self, *key_values, item: T) -> Optional[T]:
        if len(key_values) != len(self.key_fields):
            raise ValueError("The number of key values does not match the key fields.")

        if self._get_key_values(item) != key_values:
            raise ValueError("The key fields cannot be changed.")

        for index, existing_item in enumerate(self.data):
            if self._matches(existing_item, key_values):
                if hasattr(existing_item, "created_at") and hasattr(item, "created_at"):
                    setattr(
                        item,
                        "created_at",
                        getattr(existing_item, "created_at")
                    )

                if hasattr(item, "updated_at"):
                    setattr(item, "updated_at", self.get_timestamp())

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




    def save(self) -> None:
        if self.debug:
            return

        records = []

        for item in self.data:
            if is_dataclass(item) and not isinstance(item, type):
                records.append(asdict(item))

            elif hasattr(item, "__dict__"):
                records.append(vars(item).copy())

            else:
                raise TypeError(
                    f"Model {self.model.__name__} cannot be converted to JSON."
                )

        # Zorg dat de directory bestaat voordat het bestand wordt opgeslagen.
        directory = os.path.dirname(self.file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, default=str)
