from providers import data_provider
from .base_controller import BaseController


class Item_linesController(BaseController):

    GET_FUNCTIONS = {
            ("item_lines",): lambda resource_id: data_provider.fetch_item_line_pool().get_item_lines(),
            ("item_lines", "id"): lambda resource_id: data_provider.fetch_item_line_pool().get_item_line(resource_id),
            ("item_lines", "id", "items"): lambda resource_id: data_provider.fetch_item_pool().get_items_for_item_line(resource_id),
    }

    POST_FUNCTIONS = {
                        ("item_lines",): lambda resource: (
                                data_provider.fetch_item_line_pool().add_item_line(resource),
                                data_provider.fetch_item_line_pool().save()
                        )
    }
    
    PUT_FUNCTIONS = {
            ("item_lines", "id"): lambda resource_id, updated_item_line: (
                        data_provider.fetch_item_line_pool().update_item_line(
                            resource_id, updated_item_line
                        ),
                        data_provider.fetch_item_line_pool().save()
                    )
    }

    DELETE_FUNCTIONS = {
            "item_lines": lambda id: (data_provider.fetch_item_line_pool().remove_item_line(id), data_provider.fetch_item_line_pool().save())
    }