import allure
import requests
from constants import Urls, ErrorMessages


@allure.epic('API Stellar Burgers')
@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа авторизованным пользователем с валидными ингредиентами')
    def test_create_order_authorized_with_ingredients_success(self, auth_headers, available_ingredients):
        ingredients = available_ingredients[:2]
        payload = {'ingredients': ingredients}

        with allure.step('Отправка POST-запроса на создание заказа с авторизацией'):
            response = requests.post(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                headers=auth_headers,
                json=payload
            )

        response_data = response.json()
        with allure.step('Проверка кода 200, success: True и наличия номера заказа'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'order' in response_data
            assert 'number' in response_data['order']

    @allure.title('Создание заказа неавторизованным пользователем с ингредиентами')
    def test_create_order_unauthorized_with_ingredients_success(self, available_ingredients):
        ingredients = available_ingredients[:2]
        payload = {'ingredients': ingredients}

        with allure.step('Отправка POST-запроса на создание заказа без авторизации'):
            response = requests.post(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                json=payload
            )

        response_data = response.json()
        with allure.step('Проверка кода 200 и успешного создания заказа'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'order' in response_data
            assert 'number' in response_data['order']

    @allure.title('Ошибка при создании заказа без ингредиентов')
    def test_create_order_without_ingredients_error(self, auth_headers):
        payload = {'ingredients': []}

        with allure.step('Отправка POST-запроса на создание заказа с пустым списком ингредиентов'):
            response = requests.post(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                headers=auth_headers,
                json=payload
            )

        response_data = response.json()
        with allure.step('Проверка кода 400 и сообщения об обязательности ингредиентов'):
            assert response.status_code == 400
            assert response_data['success'] is False
            assert response_data['message'] == ErrorMessages.INGREDIENT_IDS_REQUIRED

    @allure.title('Ошибка при создании заказа с невалидным хешем ингредиента')
    def test_create_order_invalid_ingredient_hash_error(self, auth_headers):
        payload = {'ingredients': ['invalid_ingredient_hash_99999']}

        with allure.step('Отправка POST-запроса с невалидным хешем ингредиента'):
            response = requests.post(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                headers=auth_headers,
                json=payload
            )

        # Сервер отвечает HTML-страницей, а не JSON
        with allure.step('Проверка кода 500 и текста Internal Server Error'):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text
