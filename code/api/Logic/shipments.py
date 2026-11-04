from Logic.GenericRepository import GenericRepository
from models.shipment import Shipment
from providers import data_provider



class Shipments(GenericRepository[Shipment]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "shipment.json",
            model=Shipment,
            key_fields=("id",),
            debug=is_debug
        )

    def get_shipments(self):
        result = []
        for x in self.get_all():
            result.append(self._with_items(x))
        return result

    def get_shipment(self, shipment_id):
        shipment = self.get_by_id(shipment_id)
        if shipment is not None:
            return self._with_items(shipment)
        return None

    def get_items_in_shipment(self, shipment_id):
        rows = data_provider.fetch_shipment_item_pool().get_items_for_shipment(shipment_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def get_order_ids_in_shipment(self, shipment_id):
        """In the new schema shipment.order_id -> order.id (1:1), so a shipment
        carries exactly one order id (or none)."""
        shipment = self.get_by_id(shipment_id)
        if shipment is not None:
            order_id = shipment.order_id
            return [order_id] if order_id is not None else []
        return []

    def add_shipment(self, shipment):
        items = shipment.pop("items", [])
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()

        new_shipment = Shipment(**shipment)
        self.insert(new_shipment)

        data_provider.fetch_shipment_item_pool().set_items_for_shipment(shipment["id"], items)

    def update_shipment(self, shipment_id, shipment):
        items = shipment.pop("items", None)
        existing_shipment = self.get_by_id(shipment_id)

        if existing_shipment is None:
            return

        shipment["id"] = shipment_id
        shipment["created_at"] = existing_shipment.created_at
        shipment["updated_at"] = self.get_timestamp()

        updated_shipment = Shipment(**shipment)
        self.update(shipment_id, item=updated_shipment)

        if items is not None:
            self.update_items_in_shipment(shipment_id, items)

    def update_items_in_shipment(self, shipment_id, items):
        """Replace the items of a shipment and keep `quantity_ordered` in sync."""
        current = self.get_items_in_shipment(shipment_id)
        current_by_item = {x["item_id"]: x["amount"] for x in current}
        new_by_item = {x["item_id"]: x["amount"] for x in items}

        inventory_pool = data_provider.fetch_inventory_pool()
        for item_id, new_amount in new_by_item.items():
            old_amount = current_by_item.get(item_id, 0)
            delta = new_amount - old_amount
            if delta != 0:
                self._apply_ordered_delta(inventory_pool, item_id, delta)
        for item_id, old_amount in current_by_item.items():
            if item_id not in new_by_item:
                self._apply_ordered_delta(inventory_pool, item_id, -old_amount)

        data_provider.fetch_shipment_item_pool().set_items_for_shipment(shipment_id, items)

    @staticmethod
    def _apply_ordered_delta(inventory_pool, item_id, delta):
        inventories = inventory_pool.get_inventories_for_item(item_id)
        if not inventories:
            return
        target = max(inventories, key=lambda z: z["quantity_on_hand"])
        target["quantity_ordered"] = max(0, target["quantity_ordered"] + delta)
        inventory_pool.update_inventory(item_id, target["location_id"], target)

    def update_orders_in_shipment(self, shipment_id, order_ids):
        """In the new schema a shipment references a single order (shipment.order_id).
        We accept a list for backwards compatibility with the v1 endpoint and keep
        the first id, clearing the link when the list is empty."""
        shipment = self.get_by_id(shipment_id)

        if shipment is not None:
            updated_shipment = vars(shipment).copy()
            updated_shipment["order_id"] = order_ids[0] if order_ids else None
            updated_shipment["updated_at"] = self.get_timestamp()

            self.update(
                shipment_id,
                item=Shipment(**updated_shipment)
            )

    def remove_shipment(self, shipment_id):
        self.delete(shipment_id)
        data_provider.fetch_shipment_item_pool().remove_items_for_shipment(shipment_id)

    def _with_items(self, shipment):
        shipment = vars(shipment).copy()
        shipment["items"] = self.get_items_in_shipment(shipment["id"])
        return shipment
