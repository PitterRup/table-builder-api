from ninja.errors import ValidationError

from api.schemas import RequestValidationErrorModel


class DynamicTableExistsError(Exception):
    pass


class DynamicTableNotExistsError(Exception):
    pass


class DynamicTableNotEmptyError(Exception):
    pass


def handle_validation_error(exc: ValidationError) -> RequestValidationErrorModel:  
    errors_mapping = {                                                             
        error.get("loc")[0]: error.get("msg")
        for error in exc.errors()
    }                                                                              
    return RequestValidationErrorModel(description=errors_mapping)                 

