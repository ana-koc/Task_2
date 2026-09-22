import time
import uuid
from faker import Faker

fake = Faker()


class UserDataGenerator:

    @staticmethod
    def generate_user_payload():
        """Генерация гарантированно уникального набора данных пользователя: email, password, name."""
        unique_id = f'{int(time.time() * 1000)}_{uuid.uuid4().hex[:5]}'
        return {
            'email': f'qa_burger_{unique_id}@yandex.ru',
            'password': fake.password(length=10),
            'name': f'{fake.first_name()}_{unique_id[:4]}'
        }


class LoginData:
    WRONG_EMAIL = 'nonexistent_email_12345@test.com'
    WRONG_PASSWORD = 'wrong_password_12345'


class UserFields:
    PROFILE_FIELDS = ['email', 'name']
    ALL_FIELDS = ['email', 'name', 'password']


class OrderData:
    INVALID_INGREDIENT_HASH = 'invalid_ingredient_hash_99999'
