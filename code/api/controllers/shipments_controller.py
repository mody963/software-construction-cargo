from providers import data_provider
from .base_controller import BaseController


class ShipmentsController(BaseController):

    GET_FUNCTIONS = {
            ("shipments",): lambda resource_id: data_provider.fetch_shipment_pool().get_shipments(),
            ("shipments", "id"): lambda resource_id: data_provider.fetch_shipment_pool().get_shipment(resource_id),
            ("shipments", "id", "orders"): lambda resource_id: data_provider.fetch_shipment_pool().get_order_ids_in_shipment(resource_id),
            ("shipments", "id", "items"): lambda resource_id: data_provider.fetch_shipment_pool().get_items_in_shipment(resource_id)
    }

    POST_FUNCTIONS = {
            ("shipments",): lambda resource: (
                data_provider.fetch_shipment_pool().add_shipment(resource),
                data_provider.fetch_shipment_pool().save()
            )
    }
    
    PUT_FUNCTIONS = {
            ("shipments", "id"): lambda resource_id, updated_shipment: (
                        data_provider.fetch_shipment_pool().update_shipment(
                            resource_id, updated_shipment
                        ),
                        data_provider.fetch_shipment_pool().save()
                    ),
            ("shipments", "id", "orders"): lambda resource_id, updated_order_in_shipment: (
                        data_provider.fetch_shipment_pool().update_orders_in_shipment(
                            resource_id, updated_order_in_shipment
                        ),
                        data_provider.fetch_shipment_pool().save()
                    ),
            ("shipments", "id", "items"): lambda resource_id, updated_item_in_shipment: (
                        data_provider.fetch_shipment_pool().update_items_in_shipment(
                            resource_id, updated_item_in_shipment
                        ),
                        data_provider.fetch_shipment_pool().save(),
                        data_provider.fetch_inventory_pool().save()
                    )
    }

    DELETE_FUNCTIONS = {
            ("shipments", "id"): lambda id: (data_provider.fetch_shipment_pool().remove_shipment(id), data_provider.fetch_shipment_pool().save())
    }