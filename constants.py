class Urls:
    BASE_URL = 'https://stellarburgers.education-services.ru'
    REGISTER_PATH = '/api/auth/register'
    LOGIN_PATH = '/api/auth/login'
    USER_PATH = '/api/auth/user'
    ORDERS_PATH = '/api/orders'
    INGREDIENTS_PATH = '/api/ingredients'


class ErrorMessages:
    USER_ALREADY_EXISTS = 'User already exists'
    REQUIRED_FIELDS_MISSING = 'Email, password and name are required fields'
    INCORRECT_CREDENTIALS = 'email or password are incorrect'
    UNAUTHORIZED = 'You should be authorised'
    INGREDIENT_IDS_REQUIRED = 'Ingredient ids must be provided'
