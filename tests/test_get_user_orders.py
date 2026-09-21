import allure
import requests
from constants import Urls, ErrorMessages


@allure.epic('API Stellar Burgers')
@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:

    @allure.title('Успешное получение списка заказов авторизованного пользователя')
    def test_get_user_orders_authorized_success(self, auth_headers, available_ingredients):
        # Создаем заказ для пользователя, чтобы в списке гарантированно был заказ
        order_payload = {'ingredients': available_ingredients[:2]}
        with allure.step('Создание заказа для пользователя перед проверкой'):
            create_resp = requests.post(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                headers=auth_headers,
                json=order_payload
            )
            created_order_number = create_resp.json()['order']['number']

        with allure.step('Отправка GET-запроса на получение заказов авторизованного пользователя'):
            response = requests.get(
                f'{Urls.BASE_URL}{Urls.ORDERS_PATH}',
                headers=auth_headers
            )

        response_data = response.json()
        with allure.step('Проверка кода 200, структуры ответа и наличия созданного заказа'):
            assert response.status_code == 200
            assert response_data['success'] is True
            assert 'orders' in response_data
            assert isinstance(response_data['orders'], list)
            assert any(order['number'] == created_order_number for order in response_data['orders'])

    @allure.title('Ошибка при получении списка заказов неавторизованным пользователем')
    def test_get_user_orders_unauthorized_error(self):
        with allure.step('Отправка GET-запроса на получение заказов БЕЗ заголовка Authorization'):
            response = requests.get(f'{Urls.BASE_URL}{Urls.ORDERS_PATH}')

        response_data = response.json()
        with allure.step('Проверка кода 401 и сообщения о необходимости авторизации'):
            assert response.status_code == 401
            assert response_data['success'] is False
            assert response_data['message'] == ErrorMessages.UNAUTHORIZED
