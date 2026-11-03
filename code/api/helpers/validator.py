from jsonschema import validate, ValidationError
from schemas.schemas import SCHEMAS 

def validate_request_body(resource_name: str, payload: dict) -> tuple[bool, str | None]:
    """
    Checkt automatisch of de payload klopt voor de opgegeven resource.
    """
    schema = SCHEMAS.get(resource_name)
    
    # Als er geen schema voor bestaat (of het is een route zonder schema), keur het goed
    if not schema:
        return True, None

    try:
        validate(instance=payload, schema=schema)
        return True, None
    except ValidationError as e:
        # e.message geeft precies aan welk veld ontbreekt of verkeerd is
        return False, e.message
