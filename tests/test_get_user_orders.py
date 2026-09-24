import allure
from api_client import ApiClient
from constants import ErrorMessages


@allure.epic('API Stellar Burgers')
@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:

    @allure.title('Успешное получение списка заказов авторизованного пользователя')
    def test_get_user_orders_authorized_success(self, auth_headers, available_ingredients):
        order_payload = {'ingredients': available_ingredients[:2]}
        with allure.step('Создание заказа для пользователя перед проверкой'):
            create_resp = ApiClient.create_order(order_payload, headers=auth_headers)
            created_order_number = create_resp.json()['order']['number']

        with allure.step('Отправка GET-запроса на получение заказов авторизованного пользователя'):
            response = ApiClient.get_orders(headers=auth_headers)

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
            response = ApiClient.get_orders()

        response_data = response.json()
        with allure.step('Проверка кода 401 и сообщения о необходимости авторизации'):
            assert response.status_code == 401
            assert response_data['success'] is False
            assert response_data['message'] == ErrorMessages.UNAUTHORIZED
