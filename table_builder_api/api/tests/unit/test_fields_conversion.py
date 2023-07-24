from api.dynamic_model import serialize_fields, deserialize_fields, deserialize_fields_from_schema, StringField, NumberField, BooleanField
from api.schemas import NewTableField, ColumnType


def test_serialize_fields():
    # given
    fields = [
        StringField(name='col_str'),
        NumberField(name='col_int'),
        BooleanField(name='col_bool'),
    ]

    # when
    ret = serialize_fields(fields)

    # then
    assert ret == [
        {'name': 'col_str', '_type': 'string', 'max_length': 32},
        {'name': 'col_int', '_type': 'number'},
        {'name': 'col_bool', '_type': 'bool'},
    ]


def test_deserialize_fields():
    # given
    fields = [
        {'name': 'col_str', '_type': 'string', 'max_length': 32},
        {'name': 'col_int', '_type': 'number'},
        {'name': 'col_bool', '_type': 'bool'},
    ]

    # when
    ret = deserialize_fields(fields)

    # then
    assert ret == [
        StringField(name='col_str'),
        NumberField(name='col_int'),
        BooleanField(name='col_bool'),
    ]


def test_deserialize_fields_from_schema():
    # given
    fields = [
        NewTableField(name='col_str', col_type=ColumnType.string),
        NewTableField(name='col_int', col_type=ColumnType.number),
        NewTableField(name='col_bool', col_type=ColumnType.boolean),
    ]

    # when
    ret = deserialize_fields_from_schema(fields)

    # then
    assert ret == [
        StringField(name='col_str'),
        NumberField(name='col_int'),
        BooleanField(name='col_bool'),
    ]
