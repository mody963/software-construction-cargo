
from Logic.GenericRepository import GenericRepository
from models.transfer_item import TransferItem


class TransferItems(GenericRepository[TransferItem]):
    """Rows of the `transfer_item` table (id, transfer_id, item_id, amount)."""

    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "transfer_item.json",
            model=TransferItem,
            key_fields=("id",),
            debug=is_debug
        )

    def get_items_for_transfer(self, transfer_id):
        return [
            vars(item).copy()
            for item in self.get_all()
            if item.transfer_id == transfer_id
        ]

    def set_items_for_transfer(self, transfer_id, items):
        """Replace every item row belonging to `transfer_id` with `items`
        (a list of {item_id, amount} dicts). New surrogate ids are assigned."""
        next_id = self._next_id()
        self.remove_items_for_transfer(transfer_id)

        for item in items:
            next_id += 1
            row = {
                "id": next_id,
                "transfer_id": transfer_id,
                "item_id": item["item_id"],
                "amount": item["amount"],
            }

            new_transfer_item = TransferItem(**row)
            self.insert(new_transfer_item)

    def remove_items_for_transfer(self, transfer_id):
        self.data = [
            item for item in self.data
            if item.transfer_id != transfer_id
        ]
        self.save()

    def _next_id(self):
        return max((item.id for item in self.data), default=0)
