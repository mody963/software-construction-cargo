import json

from helpers.validator import validate_request_body

from main import ApiRequestHandler


def handle_post_version_1(self, paths: list[str], user: str | None):
    if not paths:
        return (400)

    resource = paths[0]

    try:
        payload = ApiRequestHandler.read_json_body(self)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return (400, {"error": "Invalid JSON format"})

    # Valideer de inkomende JSON tegen het schema
    is_valid, error_msg = validate_request_body(resource, payload)
    if not is_valid:
        # Als er velden missen of datatypes niet kloppen: 400 Bad Request
        return (400, {"error": error_msg})

    key = (resource,)
    route = ApiRequestHandler.POST_FUNCTIONS.get(key)
    if route is None:
        return (404)

    result = route(payload)

    return (201, result)
