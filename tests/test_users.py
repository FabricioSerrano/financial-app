from http import HTTPStatus
from uuid import uuid4

from fastapi.testclient import TestClient

from financial_app.users.models import User


def test_create_user(client: TestClient):
    response = client.post(
        '/users',
        json={
            'name': 'Test User',
            'username': 'test.user',
            'email': 'test@user.com',
            'password': 'test.password',
            'role': 'admin',
        },
    )

    assert response.status_code == HTTPStatus.CREATED


def test_create_user_with_same_username(client: TestClient, user: User):
    response = client.post(
        '/users',
        json={
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_with_same_email(client: TestClient, user: User):
    response = client.post(
        '/users',
        json={
            'name': user.name,
            'username': 'not.the.same.username',
            'email': user.email,
            'password': user.password,
            'role': user.role,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_create_user_with_wrong_role(client: TestClient):
    response = client.post(
        '/users',
        json={
            'name': 'Test User',
            'username': 'test.user',
            'email': 'test@user.com',
            'password': 'test.password',
            'role': 'wrong role',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_user_missing_field(client: TestClient):
    response = client.post(
        '/users',
        json={
            # 'name': 'Test User',
            'username': 'test.user',
            'email': 'test@user.com',
            'password': 'test.password',
            # 'role': 'wrong role',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_all_users(client: TestClient, user: User):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        ]
    }


def test_get_all_users_without_users(client: TestClient):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_user_by_id(client: TestClient, user: User):
    response = client.get('/users', params={'user_id': str(user.id)})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'role': user.role,
    }


def test_get_user_by_id_with_wrong_id(client: TestClient):
    wrong_uuid = str(uuid4())

    response = client.get('/users', params={'user_id': wrong_uuid})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_get_user_by_username(client: TestClient, user: User):
    response = client.get('/users', params={'username': user.username})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'role': user.role,
    }


def test_get_user_by_username_with_wrong_username(client: TestClient):
    wrong_username = 'some.wrong.username'

    response = client.get('/users', params={'username': wrong_username})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_get_user_by_id_with_invalid_uuid(client: TestClient):
    wrong_uuid = 'invalid.uuid'

    response = client.get('/users', params={'user_id': wrong_uuid})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'User Id is not valid'
