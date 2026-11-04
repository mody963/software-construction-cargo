
from Logic.GenericRepository import GenericRepository
from models.supplier import Supplier


class Suppliers(GenericRepository[Supplier]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "supplier.json",
            model=Supplier,
            key_fields=("id",),
            debug=is_debug
        )

    def get_suppliers(self):
        return [vars(supplier).copy() for supplier in self.get_all()]

    def get_supplier(self, supplier_id):
        supplier = self.get_by_id(supplier_id)

        if supplier is None:
            return None

        return vars(supplier).copy()

    def add_supplier(self, supplier):
        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()

        new_supplier = Supplier(**supplier)
        self.insert(new_supplier)

    def update_supplier(self, supplier_id, supplier):
        existing_supplier = self.get_by_id(supplier_id)

        if existing_supplier is None:
            return

        supplier["id"] = supplier_id
        supplier["created_at"] = existing_supplier.created_at
        supplier["updated_at"] = self.get_timestamp()

        updated_supplier = Supplier(**supplier)
        self.update(supplier_id, item=updated_supplier)

    def remove_supplier(self, supplier_id):
        self.delete(supplier_id)
