
class Order:
    def __init__(
        self,
        id: int,
        client_id: int,
        order_date: str,
        request_date: str,
        reference: str,
        customer_po_number: str,
        order_status: str,
        shipping_notes: str,
        warehouse_id: int,
        ship_to_client_id: int,
        bill_to_client_id: int,
        updated_at: str
    ):
        self.id = id
        self.client_id = client_id
        self.order_date = order_date
        self.request_date = request_date
        self.reference = reference
        self.customer_po_number = customer_po_number
        self.order_status = order_status
        self.shipping_notes = shipping_notes
        self.warehouse_id = warehouse_id
        self.ship_to_client_id = ship_to_client_id
        self.bill_to_client_id = bill_to_client_id
        self.updated_at = updated_at
