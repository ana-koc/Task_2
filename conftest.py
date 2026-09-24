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

    yield payload, response_data, access_token

    if access_token:
        ApiClient.delete_user(access_token)


@pytest.fixture
def user_payload():
    """Генерация данных пользователя без вызова регистрации. Удаление в teardown по токену."""
    payload = UserDataGenerator.generate_user_payload()
    token_holder = [None]

    yield payload, token_holder

    if token_holder[0]:
        ApiClient.delete_user(token_holder[0])


@pytest.fixture
def auth_headers(registered_user):
    """Заголовки авторизации с токеном зарегистрированного пользователя."""
    _, _, access_token = registered_user
    return {'Authorization': access_token}


@pytest.fixture
def available_ingredients():
    """Актуальный список id ингредиентов с сервера."""
    response = ApiClient.get_ingredients()
    ingredients = response.json().get('data', [])
    return [item['_id'] for item in ingredients]
