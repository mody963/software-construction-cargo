from providers import data_provider
from .base_controller import BaseController


class OrdersController(BaseController):

    GET_FUNCTIONS = {
            ("orders",): lambda resource_id: data_provider.fetch_order_pool().get_orders(),
            ("orders", "id"): lambda resource_id: data_provider.fetch_order_pool().get_order(resource_id),
            ("orders", "id", "items"): lambda resource_id: data_provider.fetch_order_pool().get_items_in_order(resource_id)
    }

    POST_FUNCTIONS = {
            ("orders",): lambda resource: (
                data_provider.fetch_order_pool().add_order(resource),
                data_provider.fetch_order_pool().save()
            )
    }
    
    PUT_FUNCTIONS = {
            ("orders", "id"): lambda resource_id, updated_order: (
                       data_provider.fetch_order_pool().update_order(
                           resource_id, updated_order
                       ),
                       data_provider.fetch_order_pool().save()
                   ),
            ("orders", "id", "items"): lambda resource_id, updated_item_in_order: (
                       data_provider.fetch_order_pool().update_items_in_order(
                           resource_id, updated_item_in_order
                       ),
                       data_provider.fetch_order_pool().save()
                   )
    }

    DELETE_FUNCTIONS = {
            "orders": lambda id: (data_provider.fetch_order_pool().remove_order(id), data_provider.fetch_order_pool().save()),
    }