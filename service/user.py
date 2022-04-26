import base64
import calendar
import datetime
import hashlib  # Импортируем библиотеку для преобразования хеш суммы
import hmac

import jwt

import constants  # Импортируем константы
from dao.user import UserDAO  # Импортируем Data Access Object


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_hash(self, password):
        """
        Функция кодирования пароля в хеш-строку
        :param password: исходный пароль
        :return: кодированный пароль
        """
        try:
            hashed_password = hashlib.pbkdf2_hmac(hash_name='sha256',
                                                  password=password.encode('utf-8'),
                                                  salt=constants.PWD_HASH_SALT,
                                                  iterations=constants.PWD_HASH_ITERATIONS)
            return base64.b64encode(hashed_password)

        # Если ошибка, то печатаем исключение
        except UnicodeDecodeError as e:
            print(f'Ошибка преобразования данных: {e}')

    def create(self, user_data):
        """
        Сервис добавления данных нового пользователя в БД
        :param user_data: данные
        :return: сущность для добавления
        """
        # Хешируем пароль и пересохраняем данные
        user_data['password'] = self.get_hash(user_data['password'])
        self.dao.create(user_data)
        return user_data

    def create_tokens(self, user_data: dict, is_refresh=False):
        """
        Сервис получения токенов допуска и обновления
        :param is_refresh: Флан для функционала проверки access_token или refresh_token, default = False
        :param user_data: данные запроса пользователя с именем пользователя и паролем
        :return: dict {access_token:str, refresh_token:str}
        """
        query = self.dao.get_one_user(username=user_data.get('username'))

        # Если запрос пустой, то возвращаем словарь ошибку
        if query is None:
            return {"error": "Ошибка в имени запрашиваемой учетной записи"}, 401

        # Если не is_refresh
        if not is_refresh:
            # Проверяем на совпадение паролей
            if not hmac.compare_digest(query.password,
                                       self.get_hash(user_data['password'])):
                return {"error": f"Ошибка в паролях {query.password} { self.get_hash(user_data['password'])} запрашиваемой учетной записи"}, 401

        # Создаем данные для дальнейшего формирования полезной нагрузки
        data = {"username": user_data.get("username"),
                "password": user_data.get("password"),
                "role": user_data.get("role")}

        # Создаем токены:
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, constants.SECRET, constants.JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, constants.SECRET, constants.JWT_ALGO)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_tokens(self, token):
        """
        Функция проверяет refresh_token и если он проходит проверку, то возвращает обновленные токены
        :param token: заданный для проверки refresh_token
        :return: dict {access_token:str, refresh_token:str}
        """
        try:
            user_data = jwt.decode(token, constants.SECRET, algorithms=[constants.JWT_ALGO])

        except Exception as e:
            return {"error": "Ошибка обработки данных {e}"}, 401

        return self.create_tokens(user_data, is_refresh=True)