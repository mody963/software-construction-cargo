from Logic.GenericRepository import GenericRepository
from models.shipment_item import ShipmentItem


class ShipmentItems(GenericRepository[ShipmentItem]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "shipment_item.json",
            model=ShipmentItem,
            key_fields=("id",),
            debug=is_debug
        )

    def get_items_for_shipment(self, shipment_id):
        result = []
        for x in self.data:
            if x.shipment_id == shipment_id:
                result.append(vars(x).copy())
        return result

    def set_items_for_shipment(self, shipment_id, items):
        next_id = self._next_id()
        self.remove_items_for_shipment(shipment_id)

        for item in items:
            next_id += 1
            row = {
                "id": next_id,
                "shipment_id": shipment_id,
                "item_id": item["item_id"],
                "amount": item["amount"],
            }

            new_shipment_item = ShipmentItem(**row)
            self.insert(new_shipment_item)

    def remove_items_for_shipment(self, shipment_id):
        self.data = [x for x in self.data if x.shipment_id != shipment_id]
        self.save()

    def _next_id(self):
        return max((x.id for x in self.data), default=0)
