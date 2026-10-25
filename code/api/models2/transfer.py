class Transfer:
    def __init__(
        self,
        id: int,
        reference: str,
        from_location_id: int,
        to_location_id: int,
        transfer_status: str,
        created_at: str,
        updated_at: str
    ):
        self.id = id
        self.reference = reference
        self.from_location_id = from_location_id
        self.to_location_id = to_location_id
        self.transfer_status = transfer_status
        self.created_at = created_at
        self.updated_at = updated_at
