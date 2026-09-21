import allure
import pytest
import requests
from constants import Urls, ErrorMessages
from data import UserDataGenerator


@allure.epic('API Stellar Burgers')
@allure.feature('Создание пользователя')
class TestCreateUser:

    @allure.title('Успешное создание уникального пользователя')
    def test_create_unique_user_success(self):
        payload = UserDataGenerator.generate_user_payload()

        with allure.step('Отправка POST-запроса на регистрацию нового пользователя'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.REGISTER_PATH}', json=payload)

        response_data = response.json()
        access_token = response_data.get('accessToken')

        try:
            with allure.step('Проверка статуса ответа и структуры тела'):
                assert response.status_code == 200
                assert response_data['success'] is True
                assert response_data['user']['email'] == payload['email']
                assert response_data['user']['name'] == payload['name']
                assert 'accessToken' in response_data
                assert 'refreshToken' in response_data
        finally:
            if access_token:
                with allure.step('Удаление созданного пользователя в teardown'):
                    requests.delete(
                        f'{Urls.BASE_URL}{Urls.USER_PATH}',
                        headers={'Authorization': access_token}
                    )

    @allure.title('Ошибка при создании уже зарегистрированного пользователя')
    def test_create_existing_user_error(self, registered_user):
        payload, _ = registered_user

        with allure.step('Повторная отправка запроса на регистрацию с теми же данными'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.REGISTER_PATH}', json=payload)

        with allure.step('Проверка кода 403 и сообщения об ошибке'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title('Ошибка при создании пользователя без обязательного поля: {missing_field}')
    @pytest.mark.parametrize(
        'missing_field',
        ['email', 'password', 'name']
    )
    def test_create_user_missing_required_field_error(self, missing_field):
        payload = UserDataGenerator.generate_user_payload()
        del payload[missing_field]

        with allure.step(f"Отправка запроса на регистрацию без поля '{missing_field}'"):
            response = requests.post(f'{Urls.BASE_URL}{Urls.REGISTER_PATH}', json=payload)

        with allure.step('Проверка кода 403 и сообщения об обязательных полях'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.REQUIRED_FIELDS_MISSING
