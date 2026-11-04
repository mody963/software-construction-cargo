from providers import data_provider
from .base_controller import BaseController


class Item_typesController(BaseController):

    GET_FUNCTIONS = {
            ("item_types",): lambda resource_id: data_provider.fetch_item_type_pool().get_item_types(),
            ("item_types", "id"): lambda resource_id: data_provider.fetch_item_type_pool().get_item_type(resource_id),
            ("item_types", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_type(resource_id),
    }

    POST_FUNCTIONS = {
                        ("item_types",): lambda resource: (
                                data_provider.fetch_item_type_pool().add_item_type(resource),
                                data_provider.fetch_item_type_pool().save()
                        )
            }
    
    PUT_FUNCTIONS = {
           ("item_types", "id"): lambda resource_id, updated_item_type: (
                       data_provider.fetch_item_type_pool().update_item_type(
                           resource_id, updated_item_type
                       ),
                       data_provider.fetch_item_type_pool().save()
                   ),
    }

    DELETE_FUNCTIONS = {
            "item_types": lambda id: (data_provider.fetch_item_type_pool().remove_item_type(id), data_provider.fetch_item_type_pool().save()),
    }