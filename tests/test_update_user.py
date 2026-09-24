import allure
import pytest
from api_client import ApiClient
from constants import ErrorMessages
from data import UserDataGenerator, UserFields


@allure.epic('API Stellar Burgers')
@allure.feature('Изменение данных пользователя')
class TestUpdateUser:

    @allure.title("Успешное изменение поля '{field_to_update}' авторизованного пользователя")
    @pytest.mark.parametrize('field_to_update', UserFields.PROFILE_FIELDS)
    def test_update_profile_field_with_auth(self, auth_headers, field_to_update):
        new_data = UserDataGenerator.generate_user_payload()
        update_payload = {field_to_update: new_data[field_to_update]}

        with allure.step(f"Отправка PATCH-запроса с авторизацией на изменение поля '{field_to_update}'"):
            response = ApiClient.update_user(update_payload, headers=auth_headers)

        response_data = response.json()
        with allure.step(f"Проверка успешного обновления поля '{field_to_update}'"):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert response_data['user'][field_to_update] == update_payload[field_to_update]

    @allure.title('Успешное изменение пароля авторизованного пользователя')
    def test_update_password_with_auth(self, registered_user, auth_headers):
        payload, _, _ = registered_user
        new_data = UserDataGenerator.generate_user_payload()
        update_payload = {'password': new_data['password']}

        with allure.step('Отправка PATCH-запроса с авторизацией на изменение пароля'):
            ApiClient.update_user(update_payload, headers=auth_headers)

        with allure.step('Вход с новым паролем'):
            login_response = ApiClient.login_user({
                'email': payload['email'],
                'password': update_payload['password']
            })

        with allure.step('Проверка, что вход с новым паролем успешен'):
            assert login_response.status_code == 200
            assert login_response.json()['success'] is True

    @allure.title("Ошибка при попытке изменения поля '{field_to_update}' без авторизации")
    @pytest.mark.parametrize('field_to_update', UserFields.ALL_FIELDS)
    def test_update_user_without_auth_error(self, field_to_update):
        new_data = UserDataGenerator.generate_user_payload()
        update_payload = {field_to_update: new_data[field_to_update]}

        with allure.step(f"Отправка PATCH-запроса БЕЗ заголовка Authorization для поля '{field_to_update}'"):
            response = ApiClient.update_user(update_payload)

        with allure.step('Проверка кода 401 и сообщения о необходимости авторизации'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.UNAUTHORIZED
