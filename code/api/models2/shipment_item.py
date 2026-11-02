class ShipmentItem:
    def __init__(
        self,
        id: int,
        shipment_id: int,
        item_id: int,
        amount: int
    ):
        self.id = id
        self.shipment_id = shipment_id
        self.item_id = item_id
        self.amount = amount
