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
