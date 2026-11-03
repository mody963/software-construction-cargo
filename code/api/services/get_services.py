import json

from helpers.validator import validate_request_body

from main import ApiRequestHandler


def handle_get_version_1(self, paths: list[str], user: str | None):
    key_delen = []

    for index, part in enumerate(paths):
        if index == 1:
            key_delen.append("id")
        else:
            key_delen.append(part)

    key = tuple(key_delen)

    route = ApiRequestHandler.GET_FUNCTIONS.get(key)
    if route is None:
        return (404)

    resource_id = None

    if len(paths) > 1:
        try:
            resource_id = int(paths[1])
        except ValueError:
            return (400)  # Voorkomt de 500-crash met strings

    result = route(resource_id)

    # Voorkomt dat een niet-bestaand ID (zoals 9999) een 200 met null geeft
    if result is None:
        return (404)

    return (200, result)
