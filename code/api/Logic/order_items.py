from Logic.GenericRepository import GenericRepository
from models.order_item import OrderItem


class OrderItems(GenericRepository[OrderItem]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "order_item.json",
            model=OrderItem,
            key_fields=("id",),
            debug=is_debug
        )

    def get_items_for_order(self, order_id):
        result = []
        for x in self.data:
            if x.order_id == order_id:
                result.append(vars(x).copy())
        return result

    def set_items_for_order(self, order_id, items):
        next_id = self._next_id()
        self.remove_items_for_order(order_id)

        for item in items:
            next_id += 1
            row = {
                "id": next_id,
                "order_id": order_id,
                "item_id": item["item_id"],
                "amount": item["amount"],
            }
            if "unit_price" in item:
                row["unit_price"] = item["unit_price"]

            new_order_item = OrderItem(**row)
            self.insert(new_order_item)

    def remove_items_for_order(self, order_id):
        self.data = [x for x in self.data if x.order_id != order_id]
        self.save()

    def _next_id(self):
        return max((x.id for x in self.data), default=0)
