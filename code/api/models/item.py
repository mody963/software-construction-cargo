class Item_Line:
    def __init__(
            self,
            id: int,
            name: str,
            description: str,
            barcode:str,
            model_number:str,
            commodity_code:str,
            unit_weight: float,
            item_line_id: int,
            item_group_id: int,
            item_type_id: int,
            min_purchase_qty: int,
            case_size: int, 
            packaging_type: str,
            order_multiple: int,
            supplier_id: int, 
            supplier_sku: str,
            created_at: str,
            updated_at: str
    ):
        self.id=id
        self.name=name
        self.description=description
        self.barcode=barcode
        self.model_number=model_number
        self.commodity_code=commodity_code
        self.unit_weight=unit_weight
        self.item_line_id=item_line_id
        self.item_group_id=item_group_id
        self.item_type_id=item_type_id
        self.min_purchase_qty=min_purchase_qty
        self.case_size=case_size
        self.packaging_type=packaging_type
        self.order_multiple=order_multiple
        self.supplier_id=supplier_id
        self.supplier_sku=supplier_sku
        self.created_at=created_at
        self.updated_at=updated_at
        
        
        
        
        
        
        
        
        
        
        