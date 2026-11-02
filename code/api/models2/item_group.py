class ItemGroup:
    def __init__(
            self,
            id: int,
            name: str, 
            description: str,
            created_at: str,
            updated_at: str
    ):
        self.id = id
        self.name = name
        self.description=description
        self.created_at= created_at
        self.updated_at= updated_at
        