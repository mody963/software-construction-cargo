import json

from helpers import validator

from services import lamba_functions_service
from services import json_service


def handle_post_version_1(self, paths: list[str], user: str | None):
    if not paths:
        return (400)

    resource = paths[0]

    try:
        payload = json_service.ApiRequestHandlerService.read_json_body(self)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return (400, {"error": "Invalid JSON format"})

    # Valideer de inkomende JSON tegen het schema
    is_valid, error_msg = validator.validate_request_body(resource, payload)
    if not is_valid:
        # Als er velden missen of datatypes niet kloppen: 400 Bad Request
        return (400, {"error": error_msg})

    key = (resource,)
    route = lamba_functions_service.POST_FUNCTIONS.get(key)
    if route is None:
        return (404)

    result = route(payload)

    return result
