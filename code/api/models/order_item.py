class OrderItem:
    def __init__(
        self, 
        id: int,
        order_id: int,
        item_id:int,
        amount:int,
        unit_price:int
        
    ):
        self.id=id
        self.order_id=order_id
        self.item_id=item_id
        self.amount=amount
        self.unit_price=unit_price
        
        
        