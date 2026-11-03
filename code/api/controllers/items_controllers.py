from providers import data_provider


class ItemsController:

    GET_FUNCTIONS = {
            ("items",): lambda resource_id: data_provider.fetch_item_pool().get_items(),
            ("items", "id"): lambda resource_id: data_provider.fetch_item_pool().get_item(resource_id),
            ("items", "id", "inventory"): lambda resource_id: data_provider.fetch_inventory_pool().get_inventories_for_item(resource_id),
            ("items", "id", "inventory", "totals"): lambda resource_id: data_provider.fetch_inventory_pool().get_inventory_totals_for_item(resource_id)
    }

    POST_FUNCTIONS = {
            ("items",): lambda resource: data_provider.fetch_item_pool().add_item(resource)
    }
    
    PUT_FUNCTIONS = {
            ("items", "id"): lambda resource_id, updated_item: (
                data_provider.fetch_item_pool().update_item(
                    resource_id, updated_item
                ),
                data_provider.fetch_item_pool().save()
            )
    }

    DELETE_FUNCTIONS = {
            "items": lambda id: (data_provider.fetch_item_pool().remove_item(id), data_provider.fetch_item_pool().save())
    }