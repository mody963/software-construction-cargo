from providers import data_provider
from .base_controller import BaseController


class SuppliersController(BaseController):

    GET_FUNCTIONS = {
            ("suppliers",): lambda resource_id: data_provider.fetch_supplier_pool().get_suppliers(),
            ("suppliers", "id"): lambda resource_id: data_provider.fetch_supplier_pool().get_supplier(resource_id),
            ("suppliers", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_supplier(resource_id)
    }

    POST_FUNCTIONS = {
                        ("suppliers",): lambda resource: (
                                data_provider.fetch_supplier_pool().add_supplier(resource),
                                data_provider.fetch_supplier_pool().save()
                        )
    }
    
    PUT_FUNCTIONS = {
           ("suppliers", "id"): lambda resource_id, updated_supplier: (
                       data_provider.fetch_supplier_pool().update_supplier(
                           resource_id, updated_supplier
                       ),
                       data_provider.fetch_supplier_pool().save()
                   )
    }

    DELETE_FUNCTIONS = {
            "suppliers": lambda id: (data_provider.fetch_supplier_pool().remove_supplier(id), data_provider.fetch_supplier_pool().save())
    }