
from Logic.GenericRepository import GenericRepository
from models.item import Items as Item

ITEMS = []

class Items(GenericRepository[Item]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "item.json",
            model=Item,
            key_fields=("id",),
            debug=is_debug
        )

    def get_items(self):
        return [vars(item).copy() for item in self.get_all()]

    def get_item(self, item_id):
        item = self.get_by_id(item_id)

        if item is None:
            return None

        return vars(item).copy()

    def get_items_for_item_line(self, item_line_id):
        result = []
        for x in self.data:
            if x.item_line_id == item_line_id:
                result.append(x.id)
        return result

    def get_items_for_item_group(self, item_group_id):
        result = []
        for x in self.data:
            if x.item_group_id == item_group_id:
                result.append(x.id)
        return result

    def get_items_for_item_type(self, item_type_id):
        result = []
        for x in self.data:
            if x.item_type_id == item_type_id:
                result.append(x.id)
        return result

    def get_items_for_supplier(self, supplier_id):
        result = []
        for x in self.data:
            if x.supplier_id == supplier_id:
                result.append(vars(x).copy())
        return result

    def add_item(self, item):
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()

        new_item = Item(**item)
        self.insert(new_item)

    def update_item(self, item_id, item):
        existing_item = self.get_by_id(item_id)

        if existing_item is None:
            return

        item["id"] = item_id
        item["created_at"] = existing_item.created_at
        item["updated_at"] = self.get_timestamp()

        updated_item = Item(**item)
        self.update(item_id, item=updated_item)

    def remove_item(self, item_id):
        self.delete(item_id)
