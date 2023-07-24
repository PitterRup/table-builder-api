import json

import pytest
from django.db import connection
from django.test import Client

from api.models import DynamicTable


@pytest.fixture
def client():
    return Client(headers={'content-type': 'application/json'})


@pytest.fixture(autouse=True)
def init_db(transactional_db):
    yield

    with connection.cursor() as cursor:
        cursor.execute("drop table if exists api_table1")


class TestAddTable:
    def test_return_status_200_on_success(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
            ]
        })

        # when
        resp = client.post('/api/table', data, content_type="application/json")

        # then
        assert resp.status_code == 200
        table_id = resp.json().get('table_id')
        assert table_id is not None
        rec = DynamicTable.objects.get(id=table_id)
        assert rec is not None
        assert rec.name == 'Table1'

    def test_return_status_409_when_table_already_exists(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
            ]
        })
        resp = client.post('/api/table', data, content_type="application/json")
        assert resp.status_code == 200

        # when
        resp = client.post('/api/table', data, content_type="application/json")

        # then
        assert resp.status_code == 409
        assert resp.json()['message'] == 'Table already exists.'


class TestUpdateTable:
    def test_return_status_200_on_success(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
            ]
        })
        resp = client.post('/api/table', data, content_type="application/json")
        assert resp.status_code == 200
        table_id = resp.json()['table_id']
        data = json.dumps({
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
                {'name': 'col_str2', 'col_type': 'string'},
            ]
        })

        # when
        resp = client.put(f'/api/table/{table_id}', data, content_type="application/json")

        # then
        assert resp.status_code == 200

    def test_return_status_404_when_table_does_not_exist(self, client):
        data = json.dumps({
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
                {'name': 'col_str2', 'col_type': 'string'},
            ]
        })

        # when
        resp = client.put(f'/api/table/10', data, content_type="application/json")

        # then
        assert resp.status_code == 404
        assert resp.json()['message'] == 'Table not found.'

    @pytest.mark.skip
    def test_return_status_409_when_table_not_empty(self, client):
        data = json.dumps({
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
                {'name': 'col_str2', 'col_type': 'string'},
            ]
        })

        # when
        resp = client.put(f'/api/table/{table_id}', data, content_type="application/json")

        # then
        assert resp.status_code == 409
        assert resp.json()['message'] == 'Cannot change table structure. Table is not empty.'


class TestAddTableRecord:
    def test_return_415_on_wrong_content_type(self, client):
        # when
        resp = client.post(f'/api/table/10/row', {}, content_type="multipart/form-data")

        # then
        assert resp.status_code == 415
        assert resp.json()['message'] == 'Unsupported content-type. Acceptable only "application/json"'

    def test_return_422_status_on_validation_error(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
                {'name': 'col_str_2', 'col_type': 'string'},
            ]
        })
        resp = client.post('/api/table', data, content_type="application/json")
        table_id = resp.json()['table_id']

        row_data = {
            'col_str': 'test',
        }

        # when
        resp = client.post(f'/api/table/{table_id}/row', row_data, content_type="application/json")

        # then
        assert resp.status_code == 422
        errors = resp.json().get('description')
        assert errors.get('col_str_2') == 'field required'

    def test_return_200_on_success(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
            ]
        })
        resp = client.post('/api/table', data, content_type="application/json")
        table_id = resp.json()['table_id']

        row_data = {
            'col_str': 'test',
        }

        # when
        resp = client.post(f'/api/table/{table_id}/row', row_data, content_type="application/json")

        # then
        assert resp.status_code == 200


class TestGetTableRecords:
    def test_return_200_on_success(self, client):
        # given
        data = json.dumps({
            'name': 'Table1',
            'fields': [
                {'name': 'col_str', 'col_type': 'string'},
            ]
        })
        resp = client.post('/api/table', data, content_type="application/json")
        assert resp.status_code == 200
        table_id = resp.json()['table_id']
        row_data = {
            'col_str': 'test',
        }
        resp = client.post(f'/api/table/{table_id}/row', row_data, content_type="application/json")
        assert resp.status_code == 200

        # when
        resp = client.get(f'/api/table/{table_id}/rows')

        # then
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0].get('col_str') == 'test'

    def test_return_404_on_missing_table(self, client):
        # when
        resp = client.get(f'/api/table/10/rows')

        # then
        assert resp.status_code == 404
        assert resp.json()['message'] == 'Table not found.'
