
from Logic.GenericRepository import GenericRepository
from models.item_group import ItemGroup


class ItemGroups(GenericRepository[ItemGroup]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "item_group.json",
            model=ItemGroup,
            key_fields=("id",),
            debug=is_debug
        )

    def get_item_groups(self):
        return [vars(item_group).copy() for item_group in self.get_all()]

    def get_item_group(self, item_group_id):
        item_group = self.get_by_id(item_group_id)

        if item_group is None:
            return None

        return vars(item_group).copy()

    def add_item_group(self, item_group):
        item_group["created_at"] = self.get_timestamp()
        item_group["updated_at"] = self.get_timestamp()

        new_item_group = ItemGroup(**item_group)
        self.insert(new_item_group)

    def update_item_group(self, item_group_id, item_group):
        existing_item_group = self.get_by_id(item_group_id)

        if existing_item_group is None:
            return

        item_group["id"] = item_group_id
        item_group["created_at"] = existing_item_group.created_at
        item_group["updated_at"] = self.get_timestamp()

        updated_item_group = ItemGroup(**item_group)
        self.update(item_group_id, item=updated_item_group)

    def remove_item_group(self, item_group_id):
        self.delete(item_group_id)
