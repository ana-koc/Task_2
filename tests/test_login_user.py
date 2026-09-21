import allure
import pytest
import requests
from constants import Urls, ErrorMessages


@allure.epic('API Stellar Burgers')
@allure.feature('Авторизация пользователя')
class TestLoginUser:

    @allure.title('Успешный логин под существующим пользователем')
    def test_login_existing_user_success(self, registered_user):
        payload, _ = registered_user
        login_payload = {
            'email': payload['email'],
            'password': payload['password']
        }

        with allure.step('Отправка POST-запроса на авторизацию с валидными данными'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.LOGIN_PATH}', json=login_payload)

        response_data = response.json()
        with allure.step('Проверка кода 200 и возвращаемых токенов'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == payload['email']
            assert response_data['user']['name'] == payload['name']
            assert 'accessToken' in response_data
            assert 'refreshToken' in response_data

    @allure.title('Ошибка при авторизации с неверными данными: {scenario_name}')
    @pytest.mark.parametrize(
        'scenario_name, wrong_email, wrong_password',
        [
            ('неверный email', 'nonexistent_email_12345@test.com', 'correct_pass'),
            ('неверный пароль', None, 'wrong_password_12345'),
            ('неверный email и пароль', 'nonexistent_email_12345@test.com', 'wrong_password_12345'),
        ]
    )
    def test_login_wrong_credentials_error(self, registered_user, scenario_name, wrong_email, wrong_password):
        payload, _ = registered_user
        email = wrong_email if wrong_email is not None else payload['email']
        password = wrong_password

        login_payload = {
            'email': email,
            'password': password
        }

        with allure.step(f'Отправка запроса на логин ({scenario_name})'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.LOGIN_PATH}', json=login_payload)

        with allure.step('Проверка кода 401 и сообщения об ошибке'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.INCORRECT_CREDENTIALS
