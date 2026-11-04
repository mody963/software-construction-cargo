from providers import data_provider


class LocationsController:

    GET_FUNCTIONS = {
            ("locations",): lambda resource_id: data_provider.fetch_location_pool().get_locations(),
            ("locations", "id"): lambda resource_id: data_provider.fetch_location_pool().get_location(resource_id)
        }

    POST_FUNCTIONS = {
            ("locations",): lambda resource: (
                data_provider.fetch_location_pool().add_location(resource),
                data_provider.fetch_location_pool().save()
            )
        }
    
    PUT_FUNCTIONS = {
            ("locations", "id"): lambda resource_id, updated_locatioon: (
                        data_provider.fetch_location_pool().update_location(
                            resource_id, updated_locatioon
                        ),
                        data_provider.fetch_location_pool().save()
                    )
    }

    DELETE_FUNCTIONS = {
    
"locations": lambda id: (data_provider.fetch_location_pool().remove_location(id), data_provider.fetch_location_pool().save()),
    }


