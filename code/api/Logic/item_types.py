
from Logic.GenericRepository import GenericRepository
from models.item_type import ItemType



class ItemTypes(GenericRepository[ItemType]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "item_type.json",
            model=ItemType,
            key_fields=("id",),
            debug=is_debug
        )

    def get_item_types(self):
        return [vars(item_type).copy() for item_type in self.get_all()]

    def get_item_type(self, item_type_id):
        item_type = self.get_by_id(item_type_id)

        if item_type is None:
            return None

        return vars(item_type).copy()

    def add_item_type(self, item_type):
        item_type["created_at"] = self.get_timestamp()
        item_type["updated_at"] = self.get_timestamp()

        new_item_type = ItemType(**item_type)
        self.insert(new_item_type)

    def update_item_type(self, item_type_id, item_type):
        existing_item_type = self.get_by_id(item_type_id)

        if existing_item_type is None:
            return

        item_type["id"] = item_type_id
        item_type["created_at"] = existing_item_type.created_at
        item_type["updated_at"] = self.get_timestamp()

        updated_item_type = ItemType(**item_type)
        self.update(item_type_id, item=updated_item_type)

    def remove_item_type(self, item_type_id):
        self.delete(item_type_id)
