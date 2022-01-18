from pydantic import ValidationError


def extract_validation_errors(e: ValidationError):
    return list(
        map(lambda err: f"{err['loc'][0]} {err['msg']}", e.errors())
    )
