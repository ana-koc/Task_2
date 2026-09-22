import allure
import pytest
from api_client import ApiClient
from constants import ErrorMessages
from data import UserDataGenerator, UserFields


@allure.epic('API Stellar Burgers')
@allure.feature('Создание пользователя')
class TestCreateUser:

    @allure.title('Успешное создание уникального пользователя')
    def test_create_unique_user_success(self, created_user):
        payload, response = created_user
        response_data = response.json()

        with allure.step('Проверка статуса ответа и структуры тела'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == payload['email']
            assert response_data['user']['name'] == payload['name']
            assert 'accessToken' in response_data
            assert 'refreshToken' in response_data

    @allure.title('Ошибка при создании уже зарегистрированного пользователя')
    def test_create_existing_user_error(self, registered_user):
        payload, _ = registered_user

        with allure.step('Повторная отправка запроса на регистрацию с теми же данными'):
            response = ApiClient.register_user(payload)

        with allure.step('Проверка кода 403 и сообщения об ошибке'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title('Ошибка при создании пользователя без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', UserFields.ALL_FIELDS)
    def test_create_user_missing_required_field_error(self, missing_field):
        payload = UserDataGenerator.generate_user_payload()
        payload.pop(missing_field)

        with allure.step(f"Отправка запроса на регистрацию без поля '{missing_field}'"):
            response = ApiClient.register_user(payload)

        with allure.step('Проверка кода 403 и сообщения об обязательных полях'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.REQUIRED_FIELDS_MISSING
