import pytest
from api_client import ApiClient
from data import UserDataGenerator


@pytest.fixture
def registered_user():
    """Регистрация пользователя перед тестом и удаление после, если сервер вернул токен."""
    payload = UserDataGenerator.generate_user_payload()
    response = ApiClient.register_user(payload)
    response_data = response.json()
    access_token = response_data.get('accessToken')

    yield payload, response_data

    if access_token:
        ApiClient.delete_user(access_token)


@pytest.fixture
def created_user():
    """Ответ регистрации нового пользователя. Токен удаляется после теста."""
    payload = UserDataGenerator.generate_user_payload()
    response = ApiClient.register_user(payload)
    access_token = response.json().get('accessToken')

    yield payload, response

    if access_token:
        ApiClient.delete_user(access_token)


@pytest.fixture
def auth_headers(registered_user):
    """Заголовки авторизации с токеном зарегистрированного пользователя."""
    _, response_data = registered_user
    access_token = response_data.get('accessToken')
    return {'Authorization': access_token}


@pytest.fixture
def available_ingredients():
    """Актуальный список id ингредиентов с сервера."""
    response = ApiClient.get_ingredients()
    ingredients = response.json().get('data', [])
    return [item['_id'] for item in ingredients]
