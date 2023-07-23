from typing import Optional

from dataclasses import dataclass

from django.db import models


@dataclass
class Field:
    name: str

    def serialize(self):
        ret = {
            'name': self.name,
        }
        ret.update(self._serialize())
        return ret

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**{
            k: v
            for k, v in data.items()
            if k != '_type'
        })


@dataclass
class StringField(Field):
    max_length: Optional[int] = 32

    @property
    def django_type(self):
        return models.CharField(max_length=self.max_length)

    def _serialize(self):
        return {
            '_type': 'string',
            'max_length': self.max_length,            
        }


@dataclass
class NumberField(Field):
    @property
    def django_type(self):
        return models.IntegerField()

    def _serialize(self):
        return {
            '_type': 'number',
        }


@dataclass
class BooleanField(Field):
    @property
    def django_type(self):
        return models.BooleanField()

    def _serialize(self):
        return {
            '_type': 'bool',
        }


def create_dynamic_model(name: str, fields: list[Field]):
    dest_fields = {
        field.name: field.django_type
        for field in fields
    }
    dest_fields['__module__'] = 'api.models'
    return type(name, (models.Model, ), dest_fields)


def serialize_fields(fields: list[Field]) -> list[dict]:
    return [
        f.serialize()
        for f in fields
    ]


_type_to_field_cls = {
    'string': StringField,
    'number': NumberField,
    'bool': BooleanField,
}

def deserialize_fields(fields: list[dict]) -> list[Field]:
    return [
        _type_to_field_cls[f['_type']].from_dict(f)
        for f in fields
    ]


def compare_fields(fields_1: list[Field], fields_2: list[Field]):
    new_fields = []
    removed_fields = []
    changed_fields = []
    dct_fields_1 = {f.name: f for f in fields_1}
    dct_fields_2 = {f.name: f for f in fields_2}
    for field in fields_2:
        if not dct_fields_1.get(field.name):
            new_fields.append(field)
    for field in fields_1:
        if not dct_fields_2.get(field.name):
            removed_fields.append(field)
    common_field_names = set(dct_fields_1.keys()) & set(dct_fields_2.keys())
    for field_name in common_field_names:
        f1 = dct_fields_1[field_name]
        f2 = dct_fields_2[field_name]
        if type(f1) != type(f2):
            changed_fields.append((f1, f2))
    return new_fields, removed_fields, changed_fields
