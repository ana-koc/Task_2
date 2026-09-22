import requests
from constants import Urls


class ApiClient:
    """Единая точка HTTP-запросов к API Stellar Burgers."""

    @staticmethod
    def _url(path):
        return f'{Urls.BASE_URL}{path}'

    @staticmethod
    def register_user(payload):
        return requests.post(ApiClient._url(Urls.REGISTER_PATH), json=payload)

    @staticmethod
    def delete_user(token):
        return requests.delete(
            ApiClient._url(Urls.USER_PATH),
            headers={'Authorization': token}
        )

    @staticmethod
    def login_user(payload):
        return requests.post(ApiClient._url(Urls.LOGIN_PATH), json=payload)

    @staticmethod
    def update_user(payload, headers=None):
        return requests.patch(ApiClient._url(Urls.USER_PATH), json=payload, headers=headers)

    @staticmethod
    def create_order(payload, headers=None):
        return requests.post(ApiClient._url(Urls.ORDERS_PATH), json=payload, headers=headers)

    @staticmethod
    def get_orders(headers=None):
        return requests.get(ApiClient._url(Urls.ORDERS_PATH), headers=headers)

    @staticmethod
    def get_ingredients():
        return requests.get(ApiClient._url(Urls.INGREDIENTS_PATH))
