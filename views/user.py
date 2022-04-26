from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import user_service
from dao.model.user import UserSchema

user_ns = Namespace('users')


@user_ns.route('/')
class UserCBV(Resource):

    # Создаем вьюшку для добавления нового пользователя
    def post(self, return_data=True):

        # Получаем данные из запроса, обрабатываем и проверяем на наличие данных
        req = request.json
        user_data = UserSchema().load(req)
        username, password, role = user_data.get('username'), user_data.get('password'), user_data.get('role')

        if None in [username, password, role]:
            return abort(404)
        # Выполняем запрос
        updated_user_data = user_service.create(user_data)

        # Для тестирования! Если return_data = False, то возвращаем пустой ответ, иначе данные о пользователе
        if not return_data:
            return "" , 201, {"location": f"/users/{updated_user_data.id}"}

        else:
            return UserSchema().dump(updated_user_data), 201


