
from Logic.GenericRepository import GenericRepository
from models.item_line import ItemLine



class ItemLines(GenericRepository[ItemLine]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "item_line.json",
            model=ItemLine,
            key_fields=("id",),
            debug=is_debug
        )

    def get_item_lines(self):
        return [vars(item_line).copy() for item_line in self.get_all()]

    def get_item_line(self, item_line_id):
        item_line = self.get_by_id(item_line_id)

        if item_line is None:
            return None

        return vars(item_line).copy()

    def add_item_line(self, item_line):
        item_line["created_at"] = self.get_timestamp()
        item_line["updated_at"] = self.get_timestamp()

        new_item_line = ItemLine(**item_line)
        self.insert(new_item_line)

    def update_item_line(self, item_line_id, item_line):
        existing_item_line = self.get_by_id(item_line_id)

        if existing_item_line is None:
            return

        item_line["id"] = item_line_id
        item_line["created_at"] = existing_item_line.created_at
        item_line["updated_at"] = self.get_timestamp()

        updated_item_line = ItemLine(**item_line)
        self.update(item_line_id, item=updated_item_line)

    def remove_item_line(self, item_line_id):
        self.delete(item_line_id)
