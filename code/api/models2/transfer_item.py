class TransferItem:
    def __init__(
        self,
        id: int,
        transfer_id: int,
        item_id: int,
        amount: int
    ):
        self.id = id
        self.transfer_id = transfer_id
        self.item_id = item_id
        self.amount = amount
