from django.db import connection
import pytest

from api.dynamic_model import create_dynamic_model, StringField


@pytest.fixture(autouse=True)
def remove_test_table(transactional_db):
    with connection.cursor() as cursor:
        cursor.execute("drop table if exists api_test")

    yield

    with connection.cursor() as cursor:
        cursor.execute("drop table if exists api_test")


@pytest.fixture
def model():
    return create_dynamic_model(
        name='Test',
        fields=[StringField(name='col_str')],
    )


def test_create_dynamic_model_in_db(transactional_db, model):
    # when
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)

    # then
    with connection.cursor() as cursor:
        cursor.execute("select * from information_Schema.tables")
        tables = cursor.fetchall()
        assert len([t for t in tables if t[2] == 'api_test']) == 1


def test_create_dynamic_model_record(transactional_db, model):
    # given
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)

    # when
    m = model(col_str='record1')
    m.save()

    # then
    with connection.cursor() as cursor:
        cursor.execute("select * from api_test")
        rows = cursor.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == 'record1'
