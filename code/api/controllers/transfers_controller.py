from providers import data_provider


class TransfersController:

    GET_FUNCTIONS = {
            ("transfers",): lambda resource_id: data_provider.fetch_transfer_pool().get_transfers(),
            ("transfers", "id"): lambda resource_id: data_provider.fetch_transfer_pool().get_transfer(resource_id),
            ("transfers", "id", "items"): lambda resource_id: data_provider.fetch_transfer_pool().get_items_in_transfer(resource_id)
    }

    POST_FUNCTIONS = {
            ("transfers",): lambda resource: data_provider.fetch_transfer_pool().add_transfer(resource)
    }
    
    PUT_FUNCTIONS = {
            ("transfers", "id"): lambda resource_id, updated_transfer: (
                        data_provider.fetch_transfer_pool().update_transfer(
                            resource_id, updated_transfer
                        ),
                        data_provider.fetch_transfer_pool().save()
                    )
    }

    DELETE_FUNCTIONS = {
            "transfers": lambda id: (data_provider.fetch_transfer_pool().remove_transfer(id), data_provider.fetch_transfer_pool().save())
    }


