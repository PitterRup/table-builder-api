import json

import pytest
from django.db import connection
from django.test import Client


@pytest.fixture
def client():
    return Client(headers={'content-type': 'application/json'})


@pytest.fixture(autouse=True)
def init_db(transactional_db):
    yield

    with connection.cursor() as cursor:
        cursor.execute("drop table if exists api_table1")


class TestAddTable:
    def test_return_status_200(self, client):
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


class TestAddTableRecord:
    def test_return_200(self, client):
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
        breakpoint()

        # then
        assert resp.status_code == 200
