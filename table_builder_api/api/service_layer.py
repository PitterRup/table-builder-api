from django.db import transaction, connection
from django.db.utils import IntegrityError
from ninja.orm import create_schema

from api.dynamic_model import create_dynamic_model, Field, serialize_fields, deserialize_fields, compare_fields
from api.models import DynamicTable
from api.exceptions import DynamicTableExistsError, DynamicTableNotExistsError, DynamicTableNotEmptyError


def create_dynamic_model_table(name: str, fields: list[Field]):
    dynamic_model = create_dynamic_model(name, fields)
    try:
        with transaction.atomic():
            t = DynamicTable(name=name, fields=serialize_fields(fields))
            t.save()
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(dynamic_model)
    except IntegrityError as err:
        if err.__cause__.pgcode == '23505':
            raise DynamicTableExistsError(f'Table with {name=} already exists')
        raise
    return t.id


def update_dynamic_model_fields(table_id: int, fields: list[Field]):
    with transaction.atomic():
        try:
            dynamic_table = DynamicTable.objects.get(id=table_id)
        except DynamicTable.DoesNotExist:
            raise DynamicTableNotExistsError(f'Table with id={table_id} not exists')
        old_dynamic_model = create_dynamic_model(dynamic_table.name, deserialize_fields(dynamic_table.fields))
        if len(old_dynamic_model.objects.all()) > 0:
            raise DynamicTableNotEmptyError(f'Cannot change structure of table with id={table_id} because it is not empty')
        dynamic_table.fields = serialize_fields(fields)
        dynamic_table.save()
        new_dynamic_model = create_dynamic_model(dynamic_table.name, fields)
        # TODO: optimization of altering dynamic table
        '''
        new_fields, removed_fields, changed_fields = compare_fields(
            deserialize_fields(dynamic_table.fields),
            fields,
        )
        for field in new_fields:
            with connection.schema_editor() as schema_editor:
                schema_editor.add_field(dynamic_model, field)
        '''
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(old_dynamic_model)
            schema_editor.create_model(new_dynamic_model)


def add_dynamic_model_record(table_id: int, data: dict):
    with transaction.atomic():
        try:
            dynamic_table = DynamicTable.objects.get(id=table_id)
        except DynamicTable.DoesNotExist:
            raise DynamicTableNotExistsError(f'Table with id={table_id} not exists')                
        dynamic_model = create_dynamic_model(dynamic_table.name, deserialize_fields(dynamic_table.fields))
        dynamic_model_schema = create_schema(dynamic_model, exclude=['id'])
        validated_data = dynamic_model_schema(**data)
        d = dynamic_model(**validated_data.dict())
        d.save()
    return d.id


def get_dynamic_model_records(table_id: int):
    try:
        dynamic_table = DynamicTable.objects.get(id=table_id)
    except DynamicTable.DoesNotExist:
        raise DynamicTableNotExistsError(f'Table with id={table_id} not exists')
    dynamic_model = create_dynamic_model(dynamic_table.name, deserialize_fields(dynamic_table.fields))
    dynamic_model_schema = create_schema(dynamic_model)
    return [
        dynamic_model_schema.from_orm(o).dict()
        for o in dynamic_model.objects.all()
    ]
