class Inventory:
    def __init__(
            self,
            item_id: int,
            location_id: int, 
            quantity_on_hand: int,
            quantity_expected: int, 
            quantity_ordered: int,
            quantity_allocated: int,
            created_at: str, 
            updated_at: str
    ):
        self.item_id = item_id
        self.location_id = location_id
        self.quantity_on_hand = quantity_on_hand
        self.quantity_expected = quantity_expected
        self.quantity_ordered = quantity_ordered
        self.quantity_allocated = quantity_allocated
        self.created_at = created_at
        self.updated_at = updated_at


        
        