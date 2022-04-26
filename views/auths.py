from flask import request, abort
from flask_restx import Resource, Namespace
from marshmallow.exceptions import MarshmallowError

from dao.model.user import UserSchema
from implemented import *

auth_ns = Namespace('auths')


@auth_ns.route('/')
class AuthCBV(Resource):
    def post(self):
        """
        Принимает данные о пользователе, сравнивает их c данными в БД и возвращает access_token и resfresh_token,
        а может вернуть ошибку, если данные не сойдутся
        :return: output: dict - словарь с токенами
        """
        try:
            # Получаем и обрабатываем запрос json
            req = request.json
            data = UserSchema().load(req)
            # Достаем из запроса нужные нам данные
            username = data.get('username')
            password = data.get('password')

            if None in [username, password]:
                return abort(404)

            output = user_service.create_tokens(data)

            return output, 201

        except MarshmallowError as e:
            return f'Ошибка {e}', 500
        except TypeError as e:
            return f'Ошибка загрузки данных {e}', 500

    def put(self):
        """
        Вьюшка обновления refresh_token
        :return: пару access_token, refresh_token в виде словаря
        """
        req = request.json
        token = req.get('refresh_token')
        if token is None:
            abort(400, 'Ошибка! Отсутствует refresh_token ')

        # Получаем новую пару токенов
        tokens = user_service.approve_refresh_tokens(token)

        return tokens, 201



