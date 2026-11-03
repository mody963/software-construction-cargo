from providers import data_provider


class Item_linesController:

    GET_FUNCTIONS = {
            ("item_groups",): lambda resource_id: data_provider.fetch_item_group_pool().get_item_groups(),
            ("item_groups", "id"): lambda resource_id: data_provider.fetch_item_group_pool().get_item_group(resource_id),
            ("item_groups", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_group(resource_id)
    }

    POST_FUNCTIONS = {
            ("item_groups",): lambda resource: data_provider.fetch_item_group_pool().add_item_group(resource),
    }
    
    PUT_FUNCTIONS = {
            ("item_groups", "id"): lambda resource_id, updated_item_group: (
                        data_provider.fetch_item_group_pool().update_item_group(
                            resource_id, updated_item_group
                        ),
                        data_provider.fetch_item_group_pool().save()
                    ),    
    }

    DELETE_FUNCTIONS = {
            "item_groups": lambda id: (data_provider.fetch_item_group_pool().remove_item_group(id), data_provider.fetch_item_group_pool().save()),
    }