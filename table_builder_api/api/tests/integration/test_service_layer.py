import pytest
from django.db import connection

from api.service_layer import create_dynamic_model_table, add_dynamic_model_record, get_dynamic_model_records, update_dynamic_model_fields
from api.models import DynamicTable
from api.dynamic_model import StringField, NumberField, serialize_fields, create_dynamic_model
from api.exceptions import DynamicTableExistsError, DynamicTableNotExistsError, DynamicTableNotEmptyError


# TODO: removing automatically all created tables after each tests


class TestCreateDynamicModelTable:
    def test_create_dynamic_model_table_record(self, transactional_db):
        # given
        model_name = 'Test'
        model_fields = [
            StringField(name='col_str'),
        ]

        # when
        table_id = create_dynamic_model_table(model_name, model_fields)

        # then
        assert table_id is not None
        rec = DynamicTable.objects.get(id=table_id)
        assert rec is not None
        assert rec.name == model_name
        assert rec.fields == serialize_fields(model_fields)


    def test_create_dynamic_model_table(self, transactional_db):
        # given
        model_name = 'Test2'
        model_fields = [
            StringField(name='col_str'),
        ]

        # when
        create_dynamic_model_table(model_name, model_fields)

        # then
        with connection.cursor() as cursor:
            cursor.execute("select * from information_schema.tables")
            tables = cursor.fetchall()
            assert len([t for t in tables if t[2] == 'api_test']) == 1

    def test_raise_table_exists_if_table_already_created(self, transactional_db):
        # given
        model_name = 'Test3'
        model_fields = [
            StringField(name='col_str'),
        ]
        create_dynamic_model_table(model_name, model_fields)

        # when
        with pytest.raises(DynamicTableExistsError):
            create_dynamic_model_table(model_name, model_fields)


@pytest.fixture
def dynamic_model_params():
    model_name = 'Test4'
    model_fields = [
        StringField(name='col_str'),
        StringField(name='col_str_2'),
    ]
    return model_name, model_fields


@pytest.fixture
def dynamic_model_id(transactional_db, dynamic_model_params):
    model_name, model_fields = dynamic_model_params
    return create_dynamic_model_table(model_name, model_fields)


@pytest.fixture
def dynamic_model(transactional_db, dynamic_model_params):
    model_name, model_fields = dynamic_model_params
    model = create_dynamic_model(model_name, model_fields)

    yield model

    with connection.schema_editor() as se:
        se.delete_model(model)


class TestUpdateDynamicModelFields:
    def test_create_new_column(self, dynamic_model, dynamic_model_id, dynamic_model_params):
        # given
        _, model_fields = dynamic_model_params
        model_fields.append(NumberField(name='col_int'))

        # when
        update_dynamic_model_fields(dynamic_model_id, model_fields)

        # then
        rec = DynamicTable.objects.get(id=dynamic_model_id)
        assert rec is not None
        assert rec.fields == serialize_fields(model_fields)
        with connection.cursor() as cursor:
            cursor.execute("select * from information_schema.columns where table_name = 'api_test4'")
            columns = cursor.fetchall()
            assert len([c for c in columns if c[3] == 'col_int']) == 1

    def test_delete_column(self, dynamic_model, dynamic_model_id, dynamic_model_params):
        # given
        _, model_fields = dynamic_model_params
        model_fields.pop(-1)

        # when
        update_dynamic_model_fields(dynamic_model_id, model_fields)

        # then
        rec = DynamicTable.objects.get(id=dynamic_model_id)
        assert rec is not None
        assert rec.fields == serialize_fields(model_fields)
        with connection.cursor() as cursor:
            cursor.execute("select * from information_schema.columns where table_name = 'api_test4'")
            columns = cursor.fetchall()
            assert len([c for c in columns if c[3] == 'col_str_2']) == 0

    def test_change_column(self):
        # TODO
        pass

    def test_raise_error_when_table_not_empty(self, dynamic_model, dynamic_model_id, dynamic_model_params):
        # given
        d = dynamic_model(col_str='test', col_str_2='test2')
        d.save()

        # then
        with pytest.raises(DynamicTableNotEmptyError):
            # when
            update_dynamic_model_fields(dynamic_model_id, []) 

    def test_raise_error_when_table_not_exists(self, transactional_db):
        with pytest.raises(DynamicTableNotExistsError):
            update_dynamic_model_fields(1, []) 


class TestAddDynamicModelRecord:
    def test_add_record(self, dynamic_model, dynamic_model_id):
        # when
        record_id = add_dynamic_model_record(dynamic_model_id, {'col_str': 'test'})

        # then
        assert record_id is not None
        records = dynamic_model.objects.all()
        assert len(records) == 1
        assert records[0].id == record_id
        assert records[0].col_str == 'test'

    def test_raise_error_when_table_not_exists(self, transactional_db):
        with pytest.raises(DynamicTableNotExistsError):
            add_dynamic_model_record(1, {})


class TestGetDynamicModelRecords:
    def test_get_all(self, dynamic_model_id, dynamic_model):
        # given
        add_dynamic_model_record(dynamic_model_id, {'col_str': 'test'})
        add_dynamic_model_record(dynamic_model_id, {'col_str': 'test2'})
        add_dynamic_model_record(dynamic_model_id, {'col_str': 'test3'})
        add_dynamic_model_record(dynamic_model_id, {'col_str': 'test4'})

        # when
        rows = get_dynamic_model_records(dynamic_model_id)

        # then
        assert len(rows) == 4
        # TODO: check returned type; currently received <class 'api.models.Test4'> != <class 'api.models.Test4'>

    def test_raise_error_when_table_not_exists(self, transactional_db):
        with pytest.raises(DynamicTableNotExistsError):
            get_dynamic_model_records(1)
