from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service

from marshmallow.exceptions import MarshmallowError

from utils import admin_required, authorization_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    @authorization_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        """
        API загрузки данных
        :return: загруженные данные и код 201
        """
        data = request.json
        try:
            serialized_data = GenreSchema.load(data)
        except MarshmallowError as e:
            return f'Ошибка {e}', 500
        except TypeError as e:
            return f'Ошибка загрузки данных {e}', 500

        entity = genre_service.create(serialized_data)
        return entity, 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):

    @authorization_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        genre_data = request.json
        genre_service.update(gid, genre_data)
        return '', 201

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return '', 201
