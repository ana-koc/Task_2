import allure
import pytest
import requests
from constants import Urls, ErrorMessages
from data import UserDataGenerator


@allure.epic('API Stellar Burgers')
@allure.feature('Изменение данных пользователя')
class TestUpdateUser:

    @allure.title("Успешное изменение поля '{field_to_update}' авторизованного пользователя")
    @pytest.mark.parametrize(
        'field_to_update',
        ['email', 'name', 'password']
    )
    def test_update_user_with_auth_success(self, registered_user, auth_headers, field_to_update):
        payload, _ = registered_user
        new_data = UserDataGenerator.generate_user_payload()
        update_payload = {field_to_update: new_data[field_to_update]}

        with allure.step(f"Отправка PATCH-запроса с авторизацией на изменение поля '{field_to_update}'"):
            response = requests.patch(
                f'{Urls.BASE_URL}{Urls.USER_PATH}',
                headers=auth_headers,
                json=update_payload
            )

        response_data = response.json()
        with allure.step(f"Проверка успешного обновления поля '{field_to_update}'"):
            assert response.status_code == 200
            assert response_data['success'] is True
            if field_to_update in ['email', 'name']:
                assert response_data['user'][field_to_update] == update_payload[field_to_update]
            elif field_to_update == 'password':
                # Проверяем, что под новым паролем можно авторизоваться
                login_response = requests.post(
                    f'{Urls.BASE_URL}{Urls.LOGIN_PATH}',
                    json={'email': payload['email'], 'password': update_payload['password']}
                )
                assert login_response.status_code == 200
                assert login_response.json()['success'] is True

    @allure.title("Ошибка при попытке изменения поля '{field_to_update}' без авторизации")
    @pytest.mark.parametrize(
        'field_to_update',
        ['email', 'name', 'password']
    )
    def test_update_user_without_auth_error(self, field_to_update):
        new_data = UserDataGenerator.generate_user_payload()
        update_payload = {field_to_update: new_data[field_to_update]}

        with allure.step(f"Отправка PATCH-запроса БЕЗ заголовка Authorization для поля '{field_to_update}'"):
            response = requests.patch(
                f'{Urls.BASE_URL}{Urls.USER_PATH}',
                json=update_payload
            )

        with allure.step('Проверка кода 401 и сообщения о необходимости авторизации'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == ErrorMessages.UNAUTHORIZED
