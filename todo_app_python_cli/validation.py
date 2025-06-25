import json
from pydantic import ValidationError


def process_error(error: ValidationError, to_json=False) -> dict:
    errors = {}
    for err in error.errors():
        field = ".".join(str(loc) for loc in err["loc"])
        if field not in errors:
            errors[field] = err["msg"]

    return json.dumps(errors) if to_json else errors
