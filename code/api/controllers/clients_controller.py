from providers import data_provider


class ClientsController:

    GET_FUNCTIONS = {
            ("clients",): lambda resource_id: data_provider.fetch_client_pool().get_clients(),
            ("clients", "id"): lambda resource_id: data_provider.fetch_client_pool().get_client(resource_id),
            ("clients", "id", "orders"): lambda resource_id: data_provider.fetch_order_pool().get_orders_for_client(resource_id)
    }

    POST_FUNCTIONS = {
            ("clients",): lambda resource: (
                data_provider.fetch_client_pool().add_client(resource),
                data_provider.fetch_client_pool().save()
            )
    }
    
    PUT_FUNCTIONS = {
            ("clients", "id"): lambda resource_id, updated_client: (
                        data_provider.fetch_client_pool().update_client(
                            resource_id, updated_client
                        ),
                        data_provider.fetch_client_pool().save()
                    )
    }

    DELETE_FUNCTIONS = {
            "clients": lambda id: (data_provider.fetch_client_pool().remove_client(id), data_provider.fetch_client_pool().save())
    }