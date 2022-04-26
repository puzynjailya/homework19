import jwt
from flask import request, abort

import constants


# Декоратор для ограничения по админке
def admin_required(func):
    # Создаем обертку
    def wrapper(*args, **kwargs):
        # Если в заголовках нет нужного нам поля, то возвращаем ошибку
        if 'Authorization' not in request.headers:
            abort(401, 'Попытка несанкционированного доступа')

        # Получаем данные из заголовка
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        # Получаем декодированные данные (если все ок, а иначе ошибку)
        try:
            user_data = jwt.decode(token, constants.SECRET, algorithms=[constants.JWT_ALGO])
        except Exception as e:
            abort(401, 'Упс! Что-то пошло не так!')

        # Получаем роль и сравниваем ее с необходимой нам ролью
        user_role = user_data.get('role')
        if user_role != 'admin':
            abort(403, 'Доступ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕН!')

        return func(*args, **kwargs)

    return wrapper


# Декоратор для ограничения по авторизации
def authorization_required(func):
    # Создаем обертку
    def wrapper(*args, **kwargs):
        # Проверяем наличие авторазации в заголовках
        if 'Authorization' not in request.headers:
            abort(401, 'Нельзя попасть в систему без авторизации')

        # Получаем данные
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]

        # Преобразовываем токен
        try:
            jwt.decode(token, constants.SECRET, algorithms=[constants.JWT_ALGO])
        except Exception as e:
            abort(401, f'Упс, что-то пошло совсем не так \n {e}')

        return func(*args, **kwargs)

    return wrapper
