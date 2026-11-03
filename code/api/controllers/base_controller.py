import json

from helpers import validator


class BaseController:
    GET_FUNCTIONS = {}
    POST_FUNCTIONS = {}
    PUT_FUNCTIONS = {}
    DELETE_FUNCTIONS = {}

    @classmethod
    def dispatch_request(cls, request_handler, method: str, paths: list[str]):
        method = method.upper()
        if method not in {"GET", "POST", "PUT", "DELETE"}:
            return 405, None

        functions = getattr(cls, f"{method}_FUNCTIONS", {})
        selected_function = None
        for route, function in functions.items():
            if isinstance(route, str):
                route = (route, "id") if method == "DELETE" else (route,)
            if len(route) != len(paths):
                continue
            if all(expected == actual or expected == "id" for expected, actual in zip(route, paths)):
                selected_function = function
                break

        if selected_function is None:
            return (405, None) if method == "DELETE" and len(paths) == 1 else (404, None)

        resource_id = None
        if len(paths) > 1:
            try:
                resource_id = int(paths[1])
            except ValueError:
                return 400, {"error": "ID must be an integer"}

        if method == "GET":
            result = selected_function(resource_id)
            return (404, None) if result is None else (200, result)

        if method in {"POST", "PUT"}:
            try:
                payload = request_handler.read_json_body()
            except (json.JSONDecodeError, UnicodeDecodeError):
                return 400, {"error": "Invalid JSON format"}

            resource = paths[0]
            if method == "POST" or len(paths) == 2:
                is_valid, error_message = validator.validate_request_body(resource, payload)
                if not is_valid:
                    return 400, {"error": error_message}

            if method == "POST":
                selected_function(payload)
                return 201, None

            selected_function(resource_id, payload)
            return 200, None

        selected_function(resource_id)
        return 200, None
