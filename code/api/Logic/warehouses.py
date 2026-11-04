
from Logic.GenericRepository import GenericRepository
from models.warehouse import Warehouse


class Warehouses(GenericRepository[Warehouse]):
    def __init__(self, root_path, is_debug=False):
        super().__init__(
            file_path=root_path + "warehouse.json",
            model=Warehouse,
            key_fields=("id",),
            debug=is_debug
        )

    def get_warehouses(self):
        return [vars(warehouse).copy() for warehouse in self.get_all()]

    def get_warehouse(self, warehouse_id):
        warehouse = self.get_by_id(warehouse_id)

        if warehouse is None:
            return None

        return vars(warehouse).copy()

    def add_warehouse(self, warehouse):
        warehouse["created_at"] = self.get_timestamp()
        warehouse["updated_at"] = self.get_timestamp()

        new_warehouse = Warehouse(**warehouse)
        self.insert(new_warehouse)

    def update_warehouse(self, warehouse_id, warehouse):
        existing_warehouse = self.get_by_id(warehouse_id)

        if existing_warehouse is None:
            return

        warehouse["id"] = warehouse_id
        warehouse["created_at"] = existing_warehouse.created_at
        warehouse["updated_at"] = self.get_timestamp()

        updated_warehouse = Warehouse(**warehouse)
        self.update(warehouse_id, item=updated_warehouse)

    def remove_warehouse(self, warehouse_id):
        self.delete(warehouse_id)
