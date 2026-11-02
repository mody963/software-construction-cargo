class Shipment:
    def __init__(
        self,
        id: int,
        reference: str,
        order_id: int,
        shipment_date: str,
        shipment_type: str,
        shipment_status: str,
        carrier_name: str,
        shipping_method: str,
        payment_type: str,
        updated_at: str
    ):
        self.id = id
        self.reference = reference
        self.order_id = order_id
        self.shipment_date = shipment_date
        self.shipment_type = shipment_type
        self.shipment_status = shipment_status
        self.carrier_name = carrier_name
        self.shipping_method = shipping_method
        self.payment_type = payment_type
        self.updated_at = updated_at
