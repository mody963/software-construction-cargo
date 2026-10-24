class OrderItem:
    def __int__(
        self, 
        id: int,
        order_id: int,
        item_id:int,
        amount:int,
        unpit_price:int
        
    ):
        self.id=id
        self.order_id=order_id
        self.item_id=item_id
        self.amount=amount
        self.unpit_price=unpit_price
        
        
        