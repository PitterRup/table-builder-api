from api.dynamic_model import compare_fields, StringField, NumberField


def test_new_fields():
    # given
    fields_old = [StringField(name='col_str')]
    fields_new = [StringField(name='col_str'), StringField(name='col_str2')]

    # when
    new_fields, removed_fields, changed_fields = compare_fields(fields_old, fields_new)

    # then
    assert new_fields == [StringField(name='col_str2')]
    assert removed_fields == []
    assert changed_fields == []


def test_removed_fields():
    # given
    fields_old = [StringField(name='col_str'), StringField(name='col_str2')]
    fields_new = [StringField(name='col_str')]

    # when
    new_fields, removed_fields, changed_fields = compare_fields(fields_old, fields_new)

    # then
    assert new_fields == []
    assert removed_fields == [StringField(name='col_str2')]
    assert changed_fields == []


def test_changed_fields():
    # given
    fields_old = [StringField(name='col_str'), StringField(name='col_str2')]
    fields_new = [StringField(name='col_str'), NumberField(name='col_str2')]

    # when
    new_fields, removed_fields, changed_fields = compare_fields(fields_old, fields_new)

    # then
    assert new_fields == []
    assert removed_fields == []
    assert changed_fields == [(StringField(name='col_str2'), NumberField(name='col_str2'))]
