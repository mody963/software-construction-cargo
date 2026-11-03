class Warehouse:
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
        contact_phone: str,
        contact_email: str,
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
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.created_at = created_at
        self.updated_at = updated_at