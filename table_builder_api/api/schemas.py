from ninja import Schema
from enum import Enum


class ColumnType(str, Enum):
    string = 'string'
    number = 'number'
    boolean = 'bool'


class NewTableField(Schema):
    name: str
    col_type: ColumnType


class NewTableSchemaIn(Schema):
    name: str
    fields: list[NewTableField]


class NewTableSchemaOut(Schema):
    table_id: int


class UpdateTableSchemaIn(Schema):
    fields: list[NewTableField]
