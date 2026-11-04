from providers import data_provider


class InventoriesController:
    GET_FUNCTIONS = {
        ("inventories",): lambda resource_id: data_provider.fetch_inventory_pool().get_inventories()
    }

    POST_FUNCTIONS = {
        ("inventories",): lambda resource: (
            data_provider.fetch_inventory_pool().add_inventory(resource),
            data_provider.fetch_inventory_pool().save()
        )
    }

    DELETE_FUNCTIONS = {}