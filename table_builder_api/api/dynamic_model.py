from dataclasses import dataclass

from django.db.models import Model


@dataclass
class Field:
    name: str
    f_type: str


def create_dynamic_model(name: str, fields: list[Field]):
    dest_fields = {
        field.name: None
        for field in fields
    }
    dest_fields['__module__'] = 'api.models'
    return type(name, (Model, ), dest_fields)
