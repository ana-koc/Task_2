import allure
from api_client import ApiClient
from constants import ErrorMessages
from data import LoginData


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
            response = ApiClient.login_user(login_payload)

        response_data = response.json()
        with allure.step('Проверка кода 200 и возвращаемых токенов'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user']['email'] == payload['email']
            assert response_data['user']['name'] == payload['name']
            assert 'accessToken' in response_data
            assert 'refreshToken' in response_data

    @allure.title('Ошибка при авторизации с неверным email')
    def test_login_with_wrong_email(self, registered_user):
        payload, _ = registered_user
        response = ApiClient.login_user({
            'email': LoginData.WRONG_EMAIL,
            'password': payload['password']
        })

        with allure.step('Проверка кода 401 и сообщения об ошибке'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.INCORRECT_CREDENTIALS

    @allure.title('Ошибка при авторизации с неверным паролем')
    def test_login_with_wrong_password(self, registered_user):
        payload, _ = registered_user
        response = ApiClient.login_user({
            'email': payload['email'],
            'password': LoginData.WRONG_PASSWORD
        })

        with allure.step('Проверка кода 401 и сообщения об ошибке'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.INCORRECT_CREDENTIALS

    @allure.title('Ошибка при авторизации с неверными email и паролем')
    def test_login_with_wrong_email_and_password(self):
        response = ApiClient.login_user({
            'email': LoginData.WRONG_EMAIL,
            'password': LoginData.WRONG_PASSWORD
        })

        with allure.step('Проверка кода 401 и сообщения об ошибке'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.INCORRECT_CREDENTIALS
