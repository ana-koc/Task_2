import pytest
import requests
from constants import Urls
from data import UserDataGenerator


@pytest.fixture
def registered_user():
    """
    Регистрация тестового пользователя перед тестом
    и гарантированное удаление через DELETE /api/auth/user в teardown.
    """
    payload = UserDataGenerator.generate_user_payload()
    response = requests.post(f'{Urls.BASE_URL}{Urls.REGISTER_PATH}', json=payload)
    assert response.status_code == 200, f'Failed to register test user: {response.text}'
    response_data = response.json()
    access_token = response_data.get('accessToken')

    yield payload, response_data

    if access_token:
        requests.delete(
            f'{Urls.BASE_URL}{Urls.USER_PATH}',
            headers={'Authorization': access_token}
        )


@pytest.fixture
def auth_headers(registered_user):
    """Заголовки авторизации с токеном зарегистрированного пользователя."""
    _, response_data = registered_user
    access_token = response_data.get('accessToken')
    return {'Authorization': access_token}


@pytest.fixture
def available_ingredients():
    """Получение актуального списка ингредиентов с сервера для тестов заказов."""
    response = requests.get(f'{Urls.BASE_URL}{Urls.INGREDIENTS_PATH}')
    ingredients = response.json().get('data', [])
    return [item['_id'] for item in ingredients]
