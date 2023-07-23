from dataclasses import dataclass

from django.db import models


@dataclass
class Field:
    name: str


class StringField(Field):
    max_length: int = 32

    @property
    def django_type(self):
        return models.CharField(max_length=self.max_length)


class NumberField(Field):
    @property
    def django_type(self):
        return models.IntegerField()


class BooleanField(Field):
    @property
    def django_type(self):
        return models.BooleanField()


def create_dynamic_model(name: str, fields: list[Field]):
    dest_fields = {
        field.name: field.django_type
        for field in fields
    }
    dest_fields['__module__'] = 'api.models'
    return type(name, (models.Model, ), dest_fields)
