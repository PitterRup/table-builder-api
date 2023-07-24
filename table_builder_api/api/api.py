import json

from ninja import NinjaAPI
from pydantic.error_wrappers import ValidationError

from api.service_layer import create_dynamic_model_table, get_dynamic_model_records, update_dynamic_model_fields, add_dynamic_model_record
from api.schemas import NewTableSchemaIn, NewTableSchemaOut, UpdateTableSchemaIn
from api import exceptions
from api.dynamic_model import deserialize_fields_from_schema

api = NinjaAPI()


@api.post('/table', response=NewTableSchemaOut)
def add_table(request, data: NewTableSchemaIn):
    table_id = create_dynamic_model_table(data.name, deserialize_fields_from_schema(data.fields))
    return {'table_id': table_id}


@api.put('/table/{table_id}')
def update_table(request, table_id: int, data: UpdateTableSchemaIn):
    update_dynamic_model_fields(table_id, deserialize_fields_from_schema(data.fields))


@api.post('/table/{table_id}/row')
def add_table_record(request, table_id: int):
    if request.content_type != 'application/json':
        return api.create_response(
            request,
            {'message': "Unsupported content-type. Acceptable only \"application/json\""},
            status=415,
        )
    data = json.loads(request.body)
    add_dynamic_model_record(table_id, data)


@api.get('/table/{table_id}/rows')
def get_table_records(request, table_id: int):
    return get_dynamic_model_records(table_id)


@api.exception_handler(Exception)
def internal_error(request, exc):
    return api.create_response(
        request,
        {'message': "Internal error occured. Please try again later or contact with technical support."},
        status=500,
    )


@api.exception_handler(exceptions.DynamicTableExistsError)
def table_exists(request, exc):
    return api.create_response(
        request,
        {'message': "Table already exists."},
        status=409,
    )


@api.exception_handler(exceptions.DynamicTableNotExistsError)
def table_not_exists(request, exc):
    return api.create_response(
        request,
        {'message': "Table not found."},
        status=404,
    )


@api.exception_handler(exceptions.DynamicTableNotEmptyError)
def table_not_empty(request, exc):
    return api.create_response(
        request,
        {'message': "Cannot change table structure. Table is not empty."},
        status=409,
    )


@api.exception_handler(ValidationError)
def validation_error(request, exc):
    message = exceptions.handle_validation_error(exc)
    return api.create_response(
        request,
        message,
        status=422,
    )
