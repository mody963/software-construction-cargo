class Location:
    def __int__(
        self, 
        id: int,
        warehouse_id: int,
        code:str,
        name: str,
        created_at:str,
        updated_at:str
    ):
        self.id=id
        self.warehouse_id=warehouse_id
        self.code=code
        self.name=name
        self.created_at=created_at
        self.updated_at=updated_at