from http import HTTPStatus

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
