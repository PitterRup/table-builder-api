from django.db.models.base import ModelBase

from api.dynamic_model import Field, create_dynamic_model


class TestDynamicModel:
    def test_return_django_model_for_provided_fields(self):
        # given
        name = 'TestModel'
        fields = []

        # when
        model = create_dynamic_model(name, fields)

        # then
        assert model is not None
        assert isinstance(model, ModelBase)
        assert model.__name__ == name
        model_fields = list(model.__dict__.keys())
        for field in fields:
            assert field.name in model_fields
