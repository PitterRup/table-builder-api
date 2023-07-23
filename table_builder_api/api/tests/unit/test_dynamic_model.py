from django.db import models

from api.dynamic_model import NumberField, BooleanField, StringField, create_dynamic_model


class TestDynamicModel:
    def test_return_django_model_for_provided_fields(self):
        # given
        name = 'TestModel'
        fields = [
            StringField(name='col_str'),
            NumberField(name='col_number'),
            BooleanField(name='col_bool'),
        ]

        # when
        model = create_dynamic_model(name, fields)

        # then
        assert model is not None
        assert isinstance(model, models.base.ModelBase)
        assert model.__name__ == name
        model_fields = list(model.__dict__.keys())
        for field in fields:
            assert field.name in model_fields

    def test_create_string_field(self, db):
        # given
        name = 'TestModel'
        field = StringField(name='col_str')

        # when
        model = create_dynamic_model(name, [field])

        # then
        col = getattr(model, field.name, None)
        assert col
        assert isinstance(col.field, models.CharField)

    def test_create_number_field(self, db):
        # given
        name = 'TestModel'
        field = NumberField(name='col_int')

        # when
        model = create_dynamic_model(name, [field])

        # then
        col = getattr(model, field.name, None)
        assert col
        assert isinstance(col.field, models.IntegerField)

    def test_create_bool_field(self, db):
        # given
        name = 'TestModel'
        field = BooleanField(name='col_bool')

        # when
        model = create_dynamic_model(name, [field])

        # then
        col = getattr(model, field.name, None)
        assert col
        assert isinstance(col.field, models.BooleanField)

    def test_auto_create_id_field(self, db):
        # given
        name = 'TestModel'

        # when
        model = create_dynamic_model(name, [])

        # then
        col = getattr(model, 'id', None)
        assert col
        assert isinstance(col.field, models.BigAutoField)

