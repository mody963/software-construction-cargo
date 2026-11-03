from providers import data_provider
from processors import notification_processor
from .base_controller import BaseController
from services import transfer_service


class TransfersController(BaseController):

    GET_FUNCTIONS = {
            ("transfers",): lambda resource_id: data_provider.fetch_transfer_pool().get_transfers(),
            ("transfers", "id"): lambda resource_id: data_provider.fetch_transfer_pool().get_transfer(resource_id),
            ("transfers", "id", "items"): lambda resource_id: data_provider.fetch_transfer_pool().get_items_in_transfer(resource_id)
    }

    POST_FUNCTIONS = {
            ("transfers",): lambda resource: _add_transfer(resource)
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

    @classmethod
    def dispatch_request(cls, request_handler, method: str, paths: list[str]):
        if method.upper() == "PUT" and len(paths) == 3 and paths[2] == "commit":
            try:
                transfer_id = int(paths[1])
            except ValueError:
                return 400, {"error": "ID must be an integer"}
            return transfer_service.handle_transfer_commit(request_handler, transfer_id), None
        return super().dispatch_request(request_handler, method, paths)


def _add_transfer(resource):
    transfer_pool = data_provider.fetch_transfer_pool()
    transfer_pool.add_transfer(resource)
    transfer_pool.save()
    notification_processor.push(f"Scheduled batch transfer {resource['id']}")


