
from Logic.GenericRepository import GenericRepository
from models.inventory import Inventory

INVENTORIES = []

class Inventories(GenericRepository[Inventory]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "inventory.json",
            model=Inventory,
            key_fields=("item_id", "location_id"),
            debug=is_debug
        )

    def get_inventories(self):
        return [vars(inventory).copy() for inventory in self.get_all()]

    def get_inventory(self, item_id, location_id):
        inventory = self.get_by_id(item_id, location_id)

        if inventory is None:
            return None

        return vars(inventory).copy()

    def get_inventories_for_item(self, item_id):
        result = []
        for x in self.data:
            if x.item_id == item_id:
                result.append(vars(x).copy())
        return result

    def get_inventory_totals_for_item(self, item_id):
        result = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0,
        }
        for x in self.data:
            if x.item_id == item_id:
                result["total_expected"] += x.quantity_expected
                result["total_ordered"] += x.quantity_ordered
                result["total_allocated"] += x.quantity_allocated
                result["total_available"] += x.quantity_on_hand - x.quantity_allocated
        return result

    def add_inventory(self, inventory):
        # Composite key: upsert on (item_id, location_id).
        item_id = inventory["item_id"]
        location_id = inventory["location_id"]
        existing = self.get_by_id(item_id, location_id)

        inventory["created_at"] = self.get_timestamp()
        inventory["updated_at"] = self.get_timestamp()

        if existing is not None:
            updated_inventory = vars(existing).copy()
            updated_inventory.update(inventory)

            self.update(
                item_id,
                location_id,
                item=Inventory(**updated_inventory)
            )
        else:
            new_inventory = Inventory(**inventory)
            self.insert(new_inventory)

    def update_inventory(self, item_id, location_id, inventory):
        existing = self.get_by_id(item_id, location_id)

        if existing is None:
            return

        inventory["item_id"] = item_id
        inventory["location_id"] = location_id
        inventory["created_at"] = existing.created_at
        inventory["updated_at"] = self.get_timestamp()

        updated_inventory = Inventory(**inventory)
        self.update(item_id, location_id, item=updated_inventory)

    def remove_inventory(self, item_id, location_id):
        self.delete(item_id, location_id)
