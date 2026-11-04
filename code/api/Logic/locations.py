
from Logic.GenericRepository import GenericRepository
from models.location import Location

LOCATIONS = []

class Locations(GenericRepository[Location]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "location.json",
            model=Location,
            key_fields=("id",),
            debug=is_debug
        )

    def get_locations(self):
        return [vars(location).copy() for location in self.get_all()]

    def get_location(self, location_id):
        location = self.get_by_id(location_id)

        if location is None:
            return None

        return vars(location).copy()

    def get_locations_in_warehouse(self, warehouse_id):
        result = []
        for location in self.data:
            if location.warehouse_id == warehouse_id:
                result.append(vars(location).copy())
        return result

    def add_location(self, location):
        location["created_at"] = self.get_timestamp()
        location["updated_at"] = self.get_timestamp()

        new_location = Location(**location)
        self.insert(new_location)

    def update_location(self, location_id, location):
        existing_location = self.get_by_id(location_id)

        if existing_location is None:
            return

        location["id"] = location_id
        location["created_at"] = existing_location.created_at
        location["updated_at"] = self.get_timestamp()

        updated_location = Location(**location)
        self.update(location_id, item=updated_location)

    def remove_location(self, location_id):
        self.delete(location_id)
