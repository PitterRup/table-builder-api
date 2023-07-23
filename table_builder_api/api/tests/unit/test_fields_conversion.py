from api.dynamic_model import serialize_fields, deserialize_fields, StringField, NumberField, BooleanField


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
