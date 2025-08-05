from http import HTTPStatus

import pytest
from bs4 import BeautifulSoup
from fastapi import HTTPException
from fastapi.testclient import TestClient

from fast_zero.app import app

client = TestClient(app)


def test_root_should_return_ok_and_hello_world_json(client):
    response = client.get('/json/hello')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_root_should_return_ok_and_hello_world_html(client):
    response = client.get('/html/hello')

    soup = BeautifulSoup(response.content, 'html.parser')

    heading = soup.find('h1')

    assert response.status_code == HTTPStatus.OK
    assert soup.title.string == 'Hello World!'
    assert heading is not None
    assert heading.text == 'Hello World!'


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_get_all_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'updated name',
            'email': 'updated@example.com',
            'password': 'updated password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'updated name',
        'email': 'updated@example.com',
    }


def test_updated_user_should_throw_an_error_if_user_not_exists(client):
    with pytest.raises(HTTPException) as exc_info:
        client.put(
            '/users/0',
            json={
                'username': 'updated name',
                'email': 'updated email',
                'password': 'updated password',
            },
        )

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
