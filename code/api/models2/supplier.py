class Supplier:
    def __init__(
        self,
        id: int,
        code: str,
        name: str,
        address: str,
        city: str,
        zip_code: str,
        province: str,
        country: str,
        contact_name: str,
        phone_number: str,
        reference: str,
        created_at: str,
        updated_at: str
    ):
        self.id = id
        self.code = code
        self.name = name
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.province = province
        self.country = country
        self.contact_name = contact_name
        self.phone_number = phone_number
        self.reference = reference
        self.created_at = created_at
        self.updated_at = updated_at
