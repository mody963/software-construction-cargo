import json

from services import transfer_service
from services import lamba_functions_service

from helpers import validator


def handle_put_version_1(self, paths):
    if len(paths) < 2:
        return int(404)

    resource = paths[0]

    try:
        resource_id = int(paths[1])
    except ValueError:
        return (400, {"error": "ID must be an integer"})

    # Speciale afhandeling voor transfers commit (geeft geen payload)
    if resource == "transfers" and len(paths) == 3 and paths[2] == "commit":
        code = transfer_service.handle_transfer_commit(self, resource_id)
        return code

    try:
        payload = self.read_json_body()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return (400, {"error": "Invalid JSON format"})

    # Bepaal de key voor PUT_FUNCTIONS
    if len(paths) == 2:
        key = (resource, "id")

        # Valideer het hoofdschema alleen bij directe updates (bijv. /warehouses/1)
        is_valid, error_msg = validator.validate_request_body(
            resource, payload)
        if not is_valid:
            return (400, {"error": error_msg})

    else:
        # Voor sub-routes (zoals /orders/1/items) skippen we de validatie tegen
        # de * zorgt voor unpacking dus je krijgt geen list met antwoord maar alleen antwoord
        key = (resource, "id", *paths[2:])

    put_function = lamba_functions_service.PUT_FUNCTIONS.get(key)

    if put_function is None:
        return (404)

    # DIT MOET NOG GEBEUREN
    # Controleer in je data-provider of het item wel bestaat
    # voordat je het updatet, anders krijg je bugs waar niet-bestaande items
    # worden toegevoegd of de server crasht. het liefst doet de data-provider dit,
    # of je voegt hier een GET check toe.

    put_function(resource_id, payload)
    return (200)
