
from Logic.GenericRepository import GenericRepository
from models.transfer import Transfer
from providers import data_provider

TRANSFERS = []

class Transfers(GenericRepository[Transfer]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "transfer.json",
            model=Transfer,
            key_fields=("id",),
            debug=is_debug
        )

    def get_transfers(self):
        return [self._with_items(transfer) for transfer in self.get_all()]

    def get_transfer(self, transfer_id):
        transfer = self.get_by_id(transfer_id)

        if transfer is not None:
            return self._with_items(transfer)

        return None

    def get_items_in_transfer(self, transfer_id):
        rows = data_provider.fetch_transfer_item_pool().get_items_for_transfer(transfer_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def add_transfer(self, transfer):
        items = transfer.pop("items", [])
        transfer["transfer_status"] = "Scheduled"
        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()

        new_transfer = Transfer(**transfer)
        self.insert(new_transfer)

        data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer["id"], items)

    def update_transfer(self, transfer_id, transfer):
        items = transfer.pop("items", None)
        existing_transfer = self.get_by_id(transfer_id)

        if existing_transfer is None:
            return

        transfer["id"] = transfer_id
        transfer["created_at"] = existing_transfer.created_at
        transfer["updated_at"] = self.get_timestamp()

        updated_transfer = Transfer(**transfer)
        self.update(transfer_id, item=updated_transfer)

        if items is not None:
            data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer_id, items)

    def remove_transfer(self, transfer_id):
        self.delete(transfer_id)
        data_provider.fetch_transfer_item_pool().remove_items_for_transfer(transfer_id)

    def _with_items(self, transfer):
        transfer = vars(transfer).copy()
        transfer["items"] = self.get_items_in_transfer(transfer["id"])
        return transfer
