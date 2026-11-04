from providers import data_provider
from .base_controller import BaseController


class WarehousesController(BaseController):

    GET_FUNCTIONS = {
            ("warehouses",): lambda resource_id: data_provider.fetch_warehouse_pool().get_warehouses(),
            ("warehouses", "id"): lambda resource_id: data_provider.fetch_warehouse_pool().get_warehouse(resource_id),
            ("warehouses", "id", "locations"): lambda resource_id: data_provider.fetch_location_pool().get_locations_in_warehouse(resource_id)
    }

    POST_FUNCTIONS = {
            ("warehouses",): lambda resource: (
                data_provider.fetch_warehouse_pool().add_warehouse(resource),
                data_provider.fetch_warehouse_pool().save()
            )
    }
    
    PUT_FUNCTIONS = {
            ("warehouses", "id"): lambda resource_id, updated_warehouse: (
                data_provider.fetch_warehouse_pool().update_warehouse(
                    resource_id, updated_warehouse
                ),
                data_provider.fetch_warehouse_pool().save()
            )
    }

    DELETE_FUNCTIONS = {
    
            "warehouses": lambda id: (data_provider.fetch_warehouse_pool().remove_warehouse(id), data_provider.fetch_warehouse_pool().save())
    }


